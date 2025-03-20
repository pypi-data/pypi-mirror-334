from setuptools import setup, find_packages

setup(
    name="r-mutex",
    version="1.1.0",
    author="JadoreThompson",
    description="A simple Redis based lock",
    long_description=open("README.md").read(),
    url="https://github.com/JadoreThompson/r-mutex",
    packages=find_packages(),
    install_requires=["redis"],
    python_requires=">=3.12",
)