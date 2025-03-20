from setuptools import setup, find_packages

setup(
    name="XMAItest",  # 包名（pip install XMAItest）
    version="0.1.0",  # 初始版本号
    author="pydevelopment",  # 作者
    author_email="hekai@xiaoma.cn",  # 邮箱
    description="Small code King AI related library",  # 简短描述
    long_description=open("README.md", encoding="utf-8").read(),  # 详细描述
    long_description_content_type="text/markdown",  # 描述格式
    url="https://github.com/Tonykai88/XMAI.git",  # GitHub 链接
    packages=find_packages(),  # 自动发现子包
    include_package_data=True,  # 包括非代码文件
    install_requires=[
        "requests>=2.32.3",  # 依赖包
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.0',  # 支持的 Python 版本
)
