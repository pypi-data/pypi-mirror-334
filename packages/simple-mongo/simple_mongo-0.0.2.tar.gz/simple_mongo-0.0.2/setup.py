from setuptools import setup, find_packages


setup(
    name="simple-mongo",
    version="0.0.2",
    packages=find_packages(include=['lib']),
    author="Marjon Godito",
    description="A simple MongoDB module with less configuration",
    install_requires=[
        'pymongo',
        'python-dotenv',
        'pydantic'
    ]
)