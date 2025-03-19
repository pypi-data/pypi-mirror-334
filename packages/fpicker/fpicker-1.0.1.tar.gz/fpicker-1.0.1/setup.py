# SPDX-License-Identifier: Apache-2.0
# Author: Sekiraw

from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

module = Extension(
    "fpicker",
    sources=["main.c"],
    libraries=['shell32', 'user32', 'comdlg32', 'ole32']
)

setup(
    name="fpicker",
    version="1.0.1",
    description="fpicker description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sekiraw",
    author_email="v2020.bohus.peter@gmail.com",
    url = 'https://github.com/Sekiraw/FPicker',
    keywords=["FILE", "PICKER", "WINDOWS"],
    license="Apache-2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    ext_modules=[module],
)
