from setuptools import setup, find_packages

setup(
    name='flat_data',
    version='1.0.0', 
    description='A Python library which provides a seamless solution for converting unstructured data into structured format, making data easier to process, analyze, and store. By organizing nested or inconsistent data into a standardized format, this library simplifies data handling for various applications.', 
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rohan Raut',
    author_email='rohanraut124@gmail.com',
    url='https://github.com/rohan-raut/flat-data', 
    packages=find_packages(),
    install_requires=[],
)
