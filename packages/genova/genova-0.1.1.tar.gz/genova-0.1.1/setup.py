from setuptools import find_packages, setup

setup(
    name='genova',
    packages=find_packages(include=['genova']),
    version='0.1.1',
    description='My first Python library and it does nothing!',
    author='Ege Güvener',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)