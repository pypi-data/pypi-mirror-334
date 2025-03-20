try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='jsparser',
    version='2.7.3',
    packages=['jsparser'],
    install_requires=[],
    license='MIT',
    author='Arden Ward',
    author_email='wardarden@gmail.com',
    description='Fast javascript parser (based on esprima.js)',
    long_description='Fast javascript parser (based on esprima.js). Python 3 fork of pyjsparser'
)
