from setuptools import setup, find_packages

setup(
    name="DataScouter",
    version="1.1.0",
    author="Arun M",
    author_email="arunpappulli@gmail.com",
    description="An AI-powered dataset search engine across Hugging Face, Kaggle, and Google Dataset Search",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arun6832/DataScouter",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "transformers",
        "torch",
        "numpy",
        "fuzzywuzzy",
        "scipy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
