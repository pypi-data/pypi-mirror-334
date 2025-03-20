from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="selenium_chrome_pool",
    version="0.1.0",  # 遵循语义化版本
    author="meihuabo",
    author_email="meihuabo@163.com",
    description="A Python library for managing Selenium Chrome connections.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meihuabo/selenium_chrome_pool", # 你的 GitHub 仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "selenium",
        # 声明你的库依赖的其他库
    ],
    python_requires='>=3.6', # 指定 Python 版本
)