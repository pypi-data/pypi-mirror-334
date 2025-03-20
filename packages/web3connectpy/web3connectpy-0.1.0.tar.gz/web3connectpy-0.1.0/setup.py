from setuptools import setup, find_packages

setup(
    name="web3connectpy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],  
    author="BakeNeko",
    author_email="bakeneko666@gmail.com",
    description="A simple library to connect to web3 provider",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
