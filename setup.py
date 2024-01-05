#!/usr/bin/env python
from setuptools import setup, find_packages, Extension
from codecs import open
import glob
import os

data_files = []
directories = glob.glob('noble_tls/dependencies/')
for directory in directories:
    files = glob.glob(directory+'*')
    data_files.append(('noble_tls/dependencies', files))

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "noble_tls", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    description=about["__description__"],
    license=about["__license__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*'],
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ]
)