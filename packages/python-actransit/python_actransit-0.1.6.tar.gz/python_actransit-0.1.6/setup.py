"""Setup for the actransit package."""

import setuptools


with open("README.md") as f:
    README = f.read()

setuptools.setup(
    author="Ira Horecka",
    author_email="ira89@icloud.com",
    name="python-actransit",
    license="MIT",
    description="Simple Alameda-Contra Costa Transit District (AC Transit) API wrapper",
    version="v0.1.6",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/irahorecka/python-actransit",
    packages=["actransit"],
    python_requires=">=3.8",
    install_requires=["gtfs-realtime-bindings", "protobuf3-to-dict", "requests"],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
)
