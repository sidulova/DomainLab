"""
run python setup.py install to install DomainLab into system
"""
import os
from setuptools import find_packages, setup

def copy_dir():
    dir_path = 'data'
    base_dir = os.path.join(os.path.normpath('.'), dir_path)
    for (dirpath, dirnames, files) in os.walk(base_dir):
        for f in files:
            path = os.path.join(dirpath.split('/', 1)[1], f)
            print(path)
            yield path

setup(
    name='domainlab',
    packages=find_packages(),
    data_files = {
            '.' : [f for f in copy_dir()]
            },
    version='0.1.9',
    description='Library of Domain Generalization',
    url='https://github.com/marrlab/DomainLab',
    author='Xudong Sun, et.al.',
    license='MIT',
)
