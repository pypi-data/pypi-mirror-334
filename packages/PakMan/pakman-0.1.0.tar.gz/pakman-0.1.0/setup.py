# setup.py
from setuptools import setup, find_packages

setup(
    name="PakMan",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Swig4",
    author_email="swigistoshort@gmail.com",
    description="A simple Python package for managing installations with pip.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Swig4/PakMan",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
