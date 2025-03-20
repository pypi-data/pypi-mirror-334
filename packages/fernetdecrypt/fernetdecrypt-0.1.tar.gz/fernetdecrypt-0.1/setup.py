from setuptools import setup, find_packages

setup(
    name="fernetdecrypt",  
    version="0.1",
    packages=find_packages(), 
    install_requires=[],  
    author="Your Name",
    author_email="fernet@company.com",
    description="Easily decrypt a fernet.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Fernet/Decrypt",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
