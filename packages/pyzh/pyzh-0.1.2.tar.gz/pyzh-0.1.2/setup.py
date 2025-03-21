# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyzh",  # 包名，在PyPI上唯一
    version="0.1.2",  # 版本号
    author="Tech-Six",  # 作者
    author_email="contact@techsix.org",  # 更新为更专业的邮箱
    description="Python中文编程包，让中文用户使用自然语法进行Python编程",  # 优化简短描述
    long_description=long_description,  # 长描述
    long_description_content_type="text/markdown",  # 长描述的内容类型
    url="https://github.com/Tech-Six/Pyzh",  # 更新为更合适的项目主页
    packages=find_packages(),
    install_requires=['jieba>=0.42.1'],  # 添加中文分词依赖
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",  # Python版本要求
    keywords="chinese, programming, education, learning, python, pyzh, y中文模块,中文编程, 编程教育, 计算机教育, 编程入门, 中文函数,", 
    project_urls={
        "Bug Tracker": "https://github.com/Tech-Six/Pyzh",
        "Documentation": "https://github.com/Tech-Six/Pyzh",
        "Source Code": "https://github.com/Tech-Six/Pyzh",
        "Homepage": "https://github.com/Tech-Six/Pyzh",  # 添加主页链接
    },
    include_package_data=True,  # 包含package_data中的数据文件
    zip_safe=False,  # 确保安装后可以正常访问包中的数据文件
)