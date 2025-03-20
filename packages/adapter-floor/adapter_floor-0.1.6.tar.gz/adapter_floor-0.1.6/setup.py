from setuptools import setup, find_packages

setup(
    name="adapter_floor",
    version="0.1.6",
    description="A lightweight Python library for precise number flooring and formatting. Includes adaptive decimal precision based on the fractional magnitude.",
    long_description="**⚠️ This package is deprecated. Please install [`adaptive-floor`](https://pypi.org/project/adaptive-floor/) instead.**",
    long_description_content_type="text/markdown",
    author="Nam Tran",
    author_email="namtran4194@gmail.com",
    url="https://github.com/tnam0x/adaptive_floor",
    packages=find_packages(),
    install_requires=[],  # No external dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
