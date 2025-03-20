from setuptools import setup, find_packages

setup(
    name="luziapi",  
    version="0.1.0",  
    packages=find_packages(),
    install_requires=[], 
    author="luzi inc",  
    author_email="help@luzitool.ct.ws",  
    description="Luzi API - Geliştiriciler için araçlar",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/luzih/luziapi", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
