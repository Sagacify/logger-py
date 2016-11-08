from setuptools import setup
from io import open
import os

root = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(root, 'src', '__about__.py'), encoding='utf8') as f:
    about = {}
    exec(f.read(), about)


rst_file = os.path.join(root, 'README.rst')
if not os.path.isfile(rst_file):
    with open(rst_file, 'w', encoding='utf-8') as readme:
        import pypandoc
        readme.write(pypandoc.convert(os.path.join(root, 'README.md'), 'rst'))


long_description = open(rst_file, encoding='utf-8').read()


setup(
    name=about['__title__'],
    packages=[about['__title__']],
    package_dir={about['__title__']: 'src'},
    description=about['__summary__'],
    long_description=long_description,
    author=about['__author__'],
    author_email=about['__email__'],
    version=about['__version__'],
    url=about['__uri__'],
    license=about['__license__']
)
