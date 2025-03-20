from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
import threading
import queue
import time
import logging
import atexit

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SeleniumChromePool:
    """
    Selenium Chrome 连接池，管理 Chrome 实例，防止页面过多卡死。
    """

    def __init__(self, max_connections=30,  max_idle_time=300,max_timeout_time=10, headless=True, chrome_options=None, remote_url=None, proxy=None):
        """
        初始化连接池。

        Args:
            max_connections (int): 连接池最大连接数。
            max_idle_time (int):  空闲连接的最大保持时间（秒）。  超过这个时间会被销毁重建.
            max_itimeout_time (int):  已使用的连接的最大运行时间（秒）。  超过这个时间会被销毁. 防止任务时间过长占用连接
            headless (bool): 是否以无头模式运行 Chrome。
            chrome_options (Options):  自定义 Chrome 选项。如果指定，会覆盖 headless 设置。
            remote_url (str):  Selenium Grid 或 standalone-chrome 的远程 URL。 默认为 None，表示使用本地 ChromeDriver。 例如： "http://192.168.1.100:4444/wd/hub"
            proxy (str): 代理服务器地址。例如："http://proxy.example.com:8080" 或者 "socks5://proxy.example.com:1080"
        """
        self.max_connections = max_connections
        self.max_idle_time = max_idle_time
        self.max_timeout_time = max_timeout_time
        self.headless = headless
        self.chrome_options = chrome_options
        self.remote_url = remote_url # 新增：远程 Selenium Grid 的 URL
        self.proxy = proxy  # 新增：代理服务器地址
        self.available_connections = queue.Queue(maxsize=max_connections)
        self.busy_connections = {}  # {driver: last_used_time}
        self._lock = threading.Lock()
        self._initialize_pool()
        atexit.register(self.close_all_connections) # 注册退出函数

    def _create_driver(self):
        """创建新的 Chrome Driver 实例."""
        options = self.chrome_options if self.chrome_options else Options()

        if self.chrome_options is None:  # only set headless if custom options aren't provided
            if self.headless:
                options.add_argument("--headless=new")  # 最新版本的 Chrome 使用 new

        options.add_argument("--disable-gpu")  # 禁用 GPU 加速，降低资源占用
        options.add_argument("--disable-extensions") # 禁用扩展
        options.add_argument("--no-sandbox")  # 在容器中使用时需要
        options.add_argument("--disable-dev-shm-usage") # 解决内存问题

        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}') # 配置代理

        try:
            if self.remote_url:
                # 使用远程 WebDriver
                driver = webdriver.Remote(command_executor=self.remote_url, options=options)
                logging.info(f"创建连接到远程 URL: {self.remote_url} 的 Chrome Driver 实例")
            else:
                # 使用本地 ChromeDriver
                driver = webdriver.Chrome(options=options) # 默认查找本地chromedriver
                # 如果 chromedriver不在PATH中，或者要指定不同的chromedriver版本
                # driver = webdriver.Chrome(executable_path="/path/to/chromedriver", options=options)
                logging.info("创建本地 Chrome Driver 实例")
            return driver
        except Exception as e:
            logging.error(f"创建 Chrome Driver 实例失败: {e}")
            return None

    def _initialize_pool(self):
        """初始化连接池，创建初始连接."""
        for _ in range(self.max_connections):
            driver = self._create_driver()
            if driver:
                self.available_connections.put(driver)
            else:
                logging.warning("连接池初始化时创建 Driver 失败，连接池容量可能不足.")

    def get_connection(self, timeout=60):
        """
        从连接池获取一个 Chrome Driver 实例。

        Args:
            timeout (int):  等待连接可用的最大时间（秒）。

        Returns:
            webdriver.Chrome: Chrome Driver 实例。
        """
        try:
            driver = self.available_connections.get(timeout=timeout)
            with self._lock:
                self.busy_connections[driver] = time.time()
            logging.info(f"获取连接: 剩余可用连接数: {self.available_connections.qsize()}, 当前活跃连接数: {len(self.busy_connections)}")
            return driver
        except queue.Empty:
            logging.warning("连接池已满，等待超时.")
            return None

    def release_connection(self, driver):
        """
        将 Chrome Driver 实例释放回连接池。

        Args:
            driver (webdriver.Chrome): 要释放的 Chrome Driver 实例。
        """
        with self._lock:
            if driver in self.busy_connections:
                del self.busy_connections[driver]
                self.available_connections.put(driver)
                logging.info(f"释放连接: 剩余可用连接数: {self.available_connections.qsize()}, 当前活跃连接数: {len(self.busy_connections)}")
            else:
                logging.warning("尝试释放未管理的连接.")

    def close_connection(self, driver):
        """关闭并销毁一个 Chrome Driver 实例."""
        try:
            driver.quit()
            logging.info("关闭并销毁了一个 Chrome Driver 实例")
        except Exception as e:
            # logging.error(f"关闭 Chrome Driver 实例失败: {e}")
            username = 0


    def cleanup_idle_connections(self):
        """清理空闲连接，定期运行，释放长时间未使用的连接."""
        while True:
            time.sleep(self.max_idle_time)  # 定期检查，避免一次性清理太多
            with self._lock:
                # 清理没使用的  超过一定时间的
                total = 0
                try:
                    for i in range(10000):
                        driver = self.available_connections.get(timeout=1)
                        total = total + 1
                        self.close_connection(driver)
                except Exception as e:
                    # logging.error(f"清理空闲连接时发生错误1: {e}")
                    username = 0
                if total > 0:
                    for i in range(total):
                        # 创建一个新的连接来补充连接池
                        new_driver = self._create_driver()
                        if new_driver:
                            self.available_connections.put(new_driver)
                            logging.info("已创建新的连接补充连接池。")
                        else:
                            logging.warning("创建新的连接失败，无法补充连接池。")
    def cleanup_timeout_connections(self):
        """清理超时连接，定期运行，释放长时间未结束的连接."""
        while True:
            time.sleep(self.max_timeout_time)  # 定期检查，避免一次性清理太多
            with self._lock:
                now = time.time()
                idle_drivers = []
                
                for driver, last_used in self.busy_connections.items():
                    if (now - last_used) > self.max_timeout_time:
                        idle_drivers.append(driver)

                for driver in idle_drivers:
                    logging.info(f"清理空闲连接: 连接已空闲超过 {self.max_timeout_time} 秒.")
                    try:
                        del self.busy_connections[driver]
                        self.close_connection(driver)

                        # 创建一个新的连接来补充连接池
                        new_driver = self._create_driver()
                        if new_driver:
                            self.available_connections.put(new_driver)
                            logging.info("已创建新的连接补充连接池。")
                        else:
                            logging.warning("创建新的连接失败，无法补充连接池。")

                    except KeyError:
                        #  在循环过程中可能已经被其他线程释放了
                        pass
                    except Exception as e:
                        logging.error(f"清理空闲连接时发生错误: {e}")
    def close_all_connections(self):
        """关闭所有连接池中的连接."""
        with self._lock:
            # 关闭忙碌连接
            for driver in list(self.busy_connections.keys()):  # 避免在迭代过程中修改字典
                try:
                    self.close_connection(driver)
                    del self.busy_connections[driver]
                except Exception as e:
                    logging.error(f"关闭 busy 连接时发生错误: {e}")

            # 关闭空闲连接
            while not self.available_connections.empty():
                try:
                    driver = self.available_connections.get_nowait()
                    self.close_connection(driver)
                except queue.Empty:
                    break  # should not happen
                except Exception as e:
                    logging.error(f"关闭 idle 连接时发生错误: {e}")

        logging.info("所有连接已关闭.")

    def start_cleanup_thread(self):
        """启动清理空闲连接的线程."""
        self.cleanup_thread = threading.Thread(target=self.cleanup_idle_connections, daemon=True)  # daemon=True: 主线程退出时，子线程也退出
        self.cleanup_timeout_thread = threading.Thread(target=self.cleanup_timeout_connections, daemon=True)  # daemon=True: 主线程退出时，子线程也退出
        self.cleanup_thread.start()
        self.cleanup_timeout_thread.start()
        logging.info("空闲连接清理线程已启动.")