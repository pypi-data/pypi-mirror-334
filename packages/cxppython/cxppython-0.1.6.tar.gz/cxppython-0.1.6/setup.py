from setuptools import setup, find_packages

setup(
    name="cxppython",              # 包名
    version="0.1.6",                # 版本号
    packages=find_packages(exclude=["tests", "tests.*"]),       # 自动找到所有包
    description="A python utils package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="cxp",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my_package",  # 项目主页（可选）
    license="MIT",
    install_requires=[
        "pymysql==1.1.1",
        "python-dotenv==1.0.0",
        "requests==2.32.3",
        "colorama~=0.4.6",
        "python-statemachine~=2.1",
        "munch~=2.5.0",
        "mysql-connector-python==9.2.0",
        "SQLAlchemy==2.0.29",
        "asyncio==3.4.3"
    ],  # 依赖（可选）
    classifiers=[                   # 元数据
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",        # 支持的 Python 版本
)