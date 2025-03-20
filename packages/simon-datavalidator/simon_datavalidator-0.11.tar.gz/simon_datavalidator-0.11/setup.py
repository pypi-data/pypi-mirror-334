from setuptools import setup, find_packages

setup(
    name='simon-datavalidator',
    version='0.11',
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    author='Simon Dickson',
    author_email='simonoche987@gmail.com',
    description='A simple data validation package',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Data-Epic/data-validator-Simon-Dickson.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ]
)
