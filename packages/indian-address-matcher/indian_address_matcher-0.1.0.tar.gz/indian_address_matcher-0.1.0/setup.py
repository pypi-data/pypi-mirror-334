from setuptools import setup, find_packages

setup(
    name="indian-address-matcher",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fuzzywuzzy>=0.18.0",
        "python-Levenshtein>=0.12.2",
        "rapidfuzz>=2.13.7",
        "jellyfish>=0.9.0",
        "nltk>=3.7",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.3",
        "pandas>=2.0.2",
        "geopandas>=0.13.2",
        "geopy>=2.3.0",
    ],
    entry_points={
        "console_scripts": [
            "address-matcher=address_matcher.cli:main",
        ],
    },
    author="Karan",
    author_email="your.email@example.com",
    description="A tool for matching Indian addresses to determine if they refer to the same location",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-github-username/indian-address-matcher",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 