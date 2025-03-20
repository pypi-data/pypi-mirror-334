from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="logax",
    version="3.2",
    author="",  
    author_email="", 
    description="A Python library to log output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/logax/logax", 
    project_urls={
        "Bug Tracker": "https://github.com/logax/logax/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",  
    python_requires=">=3",
    install_requires=["requests", "pybase64"],
)