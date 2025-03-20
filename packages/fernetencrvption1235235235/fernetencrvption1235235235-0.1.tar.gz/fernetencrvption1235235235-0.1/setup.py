# setup.py
from setuptools import setup, find_packages

setup(
    name="fernetencrvption1235235235", 
    version="0.1",
    packages=find_packages(),  
    install_requires=["requests", "cryptography"],  
    author="Your Name",
    author_email="fernetdec@decrypt.com",
    description="Easily envrypt fernet.",
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",
    url="https://github.com/fernet/fernetencrypt",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
