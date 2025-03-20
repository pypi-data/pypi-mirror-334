from setuptools import setup, find_packages

setup(
    name="adapter_floor",
    version="0.1.0",
    description="A Python library for precise number flooring with adaptive decimal precision.",
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
