from setuptools import setup
from io import open

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, OSError):
    long_description = open('README.md').read()

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
