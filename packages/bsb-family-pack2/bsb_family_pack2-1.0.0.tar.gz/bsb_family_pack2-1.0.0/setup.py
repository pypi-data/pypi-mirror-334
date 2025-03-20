# setup.py
from setuptools import setup, find_packages

setup(
    name="bsb_family_pack2",
    version="1.0.0",
    description="A secure family connection and monitoring tool via Telegram.",
    author="Shawpon Sp",
    author_email="shawponsp6@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "bsb = bsb_family_pack2.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
