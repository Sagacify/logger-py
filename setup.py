from setuptools import find_packages
from distutils.core import setup

from io import open
try:
  import pypandoc
  long_description = pypandoc.convert('README.md', 'rst')
  long_description += pypandoc.convert('CHANGELOG.md', 'rst')
except(IOError, ImportError, OSError):
  long_description = open('README.md').read()
  long_description += open('CHANGELOG.md').read()

setup(
  name = 'bunyan',
  version = '0.1.2',
  author = 'Jorge Alpedrinha Ramos',
  author_email = 'python@uphold.com',
  packages = find_packages(),
  package_data = { '': ['*.yml']},
  license = 'LICENSE',
  description = 'Bunyan python logger',
  url = 'https://www.github.com/uphold/python-bunyan/',
  long_description = long_description
)
