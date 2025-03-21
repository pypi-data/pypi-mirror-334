from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os
import sys

class CustomInstall(install):
    def run(self):
        install.run(self) # 先运行标准的安装

        submodule_path = os.path.join("ikan", "groupkan", "rational_kat_cu")
        if os.path.exists(submodule_path):
            print(f"Running setup.py for submodule in: {submodule_path}")
            try:
                # 确保在子模块目录下执行 setup.py
                subprocess.check_call([sys.executable, "setup.py", "install"], cwd=submodule_path)
                print(f"Submodule setup.py ran successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error running submodule setup.py: {e}")
                sys.exit(1) # 安装失败时退出

setup(
    name="ikan",
    version="1.2.7", # 递增版本号
    author="Guoying LIAO",
    author_email="lgy112112@gmail.com",
    description="An efficient KAN implementation in Chinese.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lgy112112/Efficient-KAN-in-Chinese",
    packages=find_packages(include=["ikan", "ikan.*"]), # 只查找 ikan 包
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
        'install': CustomInstall, # 使用自定义安装命令
    },
    include_package_data=True,
)
