#!/usr/bin/env python
import os
from setuptools import setup, find_packages
#### from version import __version__

##from setuptools_scm import get_version

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

### exec(open('version.py').read())
import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="nuphy2",
    description="NUclear PHYsics python package - try #2",
    url="http://gitlab.com/jaromrax/nuphy2",
    author="JM",
    author_email="jaromrax@gmail.com",
    licence="GPL2",
    version=get_version("nuphy2/version.py"),
#    version=__version__,
#    packages=find_packages(),
    packages=['nuphy2'],
    package_data={'nuphy2': ['data/*', 'data/decay/*', 'data/ensdf/*', 'data/pdf_summary/*', 'data/tendl21/*', 'data/tunl/*']},
#    packagedata={'nuphy2': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/nuphy2', 'bin/sriminst.sh'],
    install_requires = ['fire','importlib_resources','pandas','xvfbwrapper','matplotlib','scipy','bs4','lxml', 'pdf2image'],
)
#
#   To Access Data in Python: :
#   DATA_PATH = pkg_resources.resource_filename('nuphy2', 'data/')
#   DB_FILE =   pkg_resources.resource_filename('nuphy2', 'data/file')
