from distutils.core import setup

from io import open
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, OSError):
    long_description = open('README.md').read()

setup(
  name='sagalogger',
  version='0.2.1',
  author='Augustin Borsu',
  author_email='dev@sagacify.com',
  packages=['sagalogger'],
  license='LICENSE',
  description='Saga python logger',
  url='https://www.github.com/Sagacify/logger-py',
  long_description=long_description
)
