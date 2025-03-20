from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='applepylog',
    packages=find_packages(include=['applepylog']),
    version='0.1.5',
    description='A simple logger for basic projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChrisYeomans/ApplePyLog",
    author='Chris Yeomans',
    author_email='chris.shorelinetech@gmail.com',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest~=8.2.2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)