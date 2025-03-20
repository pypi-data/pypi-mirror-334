#!/usr/bin/env python
# filepath: setup.py

from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xlang-script",
    version="0.1.1-0",
    author="sjrsjz@github",
    author_email="sjrsjz@gmail.com",
    description="XLang - Lightweight programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sjrsjz/XLang",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "xlang=xlang.xlang.cli:main",
        ],
    },
    include_package_data=True,
    install_requires=[
        "prompt_toolkit>=3.0.0",  # 添加prompt_toolkit依赖
    ],
    keywords="programming language, interpreter, compiler",
    project_urls={
        "Source": "https://github.com/sjrsjz/XLang",
    },
)
