import versioneer
from setuptools import setup, find_packages
import os

DESCRIPTION = "Inference of transcription factor motif activity from single cell RNA-seq data."

with open("README.md") as f:
    long_description = f.read()

setup(
    name="pananse",
    version=versioneer.get_version(),
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    description=DESCRIPTION,
    author="Quan Xu",
    author_email="qxuchn@gmail.com",
    url="https://github.com/qxuchn/PANANSE/",
    license="MIT",
    packages=find_packages(),
    scripts=["scripts/pananse"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    install_requires=[
        
    ],
)
