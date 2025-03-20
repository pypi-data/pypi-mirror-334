import os
from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="divr-benchmark",
    packages=find_packages(),
    package_data={
        "divr_benchmark": ["tasks/*/*.yml", "tasks/README.md"],
    },
    version=os.environ["RELEASE_VERSION"],
    license="MIT",
    description="Toolkit to work with disordered voice databases",
    author="Computational Audio Research Lab",
    url="https://github.com/ComputationalAudioResearchLab/divr-benchmark",
    keywords=[
        "ML Audio Features",
        "ML",
        "Disordered Voice Features",
        "Research",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "aiofiles>=23.1.0",
        "aiohttp>=3.8.4",
        "class-argparse>=0.1.3",
        "divr-diagnosis>=0.1.2",
        "librosa>=0.10.0.post2",
        "matplotlib>=3.7.1",
        "nspfile>=0.1.4",
        "openpyxl>=3.1.2",
        "pandas>=2.0.1",
        "PyYAML>=6.0.1",
        "svd-downloader>=0.1.1",
        "wfdb>=4.1.2",
        "xlrd>=2.0.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
)
