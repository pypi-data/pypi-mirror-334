# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="AGKit",  # 库的名称，必须唯一
    version='0.19',  # 库的版本号
    author="LiZhun",
    author_email="914525405@qq.com",
    description="python工具基础库",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",  # 许可证（如 MIT, Apache, GPL 等）
    packages=find_packages(),  # 自动发现包
    install_requires=[
        # 依赖包列表
        "requests>=2.25.1",
        "colorlog>=6.8.2",
        "Pillow==11.1.0",
        "xlrd>=2.0.1",
        "pyinstaller==6.10.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # 支持的 Python 版本
)
