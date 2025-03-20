from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="simple-mongo",
    version="0.0.9",
    packages=find_packages(include=['simple_mongo']),
    author="Marjon Godito",
    description="A simple MongoDB module with less configuration",
    install_requires=[
        'pymongo',
        'python-dotenv'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)