from setuptools import setup, find_packages

setup(
    name="testneo-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="gururajhm",
    author_email="gururajhm@gmail.com",
    description="A sample Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
