# setup.py

from setuptools import setup, find_packages

setup(
    name="greetlib",
    version="0.2.0",
    author="Ola",
    author_email="akindele.ok@gmail.com",
    description="A simple package for generating greetings in different languages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OlaAkindele/greeting-package.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
