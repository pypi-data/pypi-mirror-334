from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flatforge",
    version="0.3.0",
    author="Akram Zaki",
    author_email="azpythonprojects@gmail.com",
    description="A library for validating and transforming flat files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akram0zaki/flatforge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.0.0",
        "tqdm>=4.64.0",
    ],
    entry_points={
        "console_scripts": [
            "flatforge=flatforge.cli.__init__:cli",
        ],
    },
) 