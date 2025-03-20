from setuptools import setup, find_packages

setup(
    name="toosimplelogging",  # 模块名称
    version="0.1.0",  # 版本号
    author="0x6768",  # 作者姓名
    author_email="admin@yang325.eu.org",  # 作者邮箱
    description="A lightweight logging utility with terminal color support and file output capabilities.",  # 简短描述
    long_description=open("README.md").read(),  # 从 README.md 读取长描述
    long_description_content_type="text/markdown",  # 长描述内容类型
    url="https://github.com/0x6768/toosimplelogging",  # 项目主页
    packages=find_packages(),  # 自动查找包
    install_requires=["rich"],  # 依赖项
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3.6",  # 支持的 Python 版本
)