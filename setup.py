from setuptools import setup, find_packages

setup(
	name='assignment2',
	version='1.0',
	author='Abhishek Kothari',
	author_email='b.kothari@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)