from setuptools import setup
from io import open
import os

if not os.path.isfile('README.rst') and os.path.isfile('README.md'):
    with open('README.rst', 'w', encoding='utf-8') as readme:
        import pypandoc
        readme.write(pypandoc.convert('README.md', 'rst'))

long_description = open('README.rst').read()

setup(
    name='sagalogger',
    packages=['sagalogger'],
    package_dir={'sagalogger': 'src'},
    version='0.2.1',
    author='Sagacify',
    author_email='dev@sagacify.com',
    license='LICENSE',
    description='Saga python logger',
    url='https://www.github.com/Sagacify/logger-py',
    long_description=long_description
)
