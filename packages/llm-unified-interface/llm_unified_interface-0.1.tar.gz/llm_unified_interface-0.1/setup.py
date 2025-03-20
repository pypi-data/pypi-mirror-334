# setup.py
from setuptools import setup, find_packages

setup(
    name="llm_unified_interface",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",  # 依赖的第三方包
    ],
    author="丁雨虹",
    description="适配国内主流大语言模型的统一访问接口",
)