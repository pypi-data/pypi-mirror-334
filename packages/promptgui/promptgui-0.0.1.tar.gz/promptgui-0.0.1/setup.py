from setuptools import setup, find_packages


setup(
name='promptgui',
version='0.0.1',
author='Joseph Ferrara',
description='A Dash interface for Prompt Management and Iterative Development',
long_description=open("README.md").read(),
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
