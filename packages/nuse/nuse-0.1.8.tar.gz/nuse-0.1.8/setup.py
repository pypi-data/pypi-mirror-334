from setuptools import setup, find_packages
import os

# Read the README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nuse",
    version="0.1.8",
    author='Jacob Molin Nielsen',
    author_email='jacob.molin@me.com',
    description='A simple resource monitoring tool for SLURM jobs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MolinDiscovery/nuse',  
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "nuse = nuse.nuse:main",
        ],
    },
)