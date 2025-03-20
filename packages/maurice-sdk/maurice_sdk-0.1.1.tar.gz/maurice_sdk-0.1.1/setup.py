from setuptools import setup, find_packages

setup(
    name="maurice_sdk",
    version="0.1.1",
    description="A Python SDK for controlling the Maurice robot arm and drive system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Innate Inc",
    author_email="vignesh@innate.bot",
    url="https://github.com/innate-inc/maurice_sdk.git",
    packages=find_packages(),
    install_requires=[
        "dynamixel_sdk",
        "numpy",
        "pyserial",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
