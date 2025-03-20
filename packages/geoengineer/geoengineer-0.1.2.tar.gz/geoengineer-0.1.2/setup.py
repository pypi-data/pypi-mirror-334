from setuptools import setup, find_packages
import os
import re

# Read version from version.py
with open(os.path.join('geoengineer', 'version.py'), 'r') as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string in version.py")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geoengineer",
    version=version,
    author="GeoEngineer Contributors",
    author_email="geoengineerai@gmail.com",
    description="A simple GeoEngineer AI package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geoengineer-ai/geoengineer-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.6",
    license="MIT",
) 