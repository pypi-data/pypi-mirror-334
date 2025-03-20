from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='genova',
    packages=find_packages(include=['genova', 'numpy']),
    version='1.1.4',
    description='Genova is a versatile Python library that offers a collection of powerful tools for various domains including mathematics, artificial intelligence, finance, and more.',
    author='Ege Güvener',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    long_description=long_description,
    long_description_content_type='text/markdown',
)