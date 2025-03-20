# setup.py
import os
from setuptools import setup, find_packages

setup(
    name="luzigpt",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[],
    author="luzi tool",
    description="LuziGPT: Önceden belirlenmiş soru-cevapları döndüren Python modülü",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)