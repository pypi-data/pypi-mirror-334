from setuptools import setup, find_packages

setup(
    name="chandler-banner",  # 包名称
    version="1.0",
    packages=find_packages(),  # 自动查找所有模块
    install_requires=[
        "pyfiglet",
        "termcolor",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "chandler-banner=chandler_banner.chandler:banner1",
        ]
    },
    author="chandler Liu",
    author_email="vhbzhl1234@gmail.com",
    description="一个终端彩色 ASCII 文字chandler liu12138的 Python 包",
    long_description=open("江湖夜雨十年灯.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/1433223123/chandler_banner",  # GitHub 地址
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
