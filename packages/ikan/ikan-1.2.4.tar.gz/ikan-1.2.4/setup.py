from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os
import sys

class CustomInstall(install):
    def run(self):
        # 先安装主包
        install.run(self)
        
        # 安装 rational_kat_cu 子模块
        submodule_path = os.path.join("ikan", "groupkan", "rational_kat_cu")
        if os.path.exists(submodule_path):
            subprocess.check_call([sys.executable, "setup.py", "install"], cwd=submodule_path)

setup(
    name="ikan",  # 包名称，用作 pip install 的名字
    version="1.2.4",  # 包版本
    author="Guoying LIAO",  # 作者姓名
    author_email="lgy112112@gmail.com",  # 作者邮箱
    description="An efficient KAN implementation in Chinese.",  # 简要描述
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",  # README 文件格式
    url="https://github.com/lgy112112/Efficient-KAN-in-Chinese",  # 仓库地址
    packages=find_packages(include=["ikan", "ikan.*", "kat_rational*"]),  # 自动发现所有子包
    install_requires=[
        "torch>=1.9.0",
        "torchinfo",
        "numpy",
        "scikit-learn",
        "timm==1.0.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    cmdclass={
        'install': CustomInstall,
    },
    include_package_data=True,
)
