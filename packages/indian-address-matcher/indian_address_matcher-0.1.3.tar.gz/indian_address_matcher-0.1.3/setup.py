from setuptools import setup, find_packages
import os

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get requirements from file if it exists
try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    # Fallback requirements if file is missing
    requirements = [
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
    ]

setup(
    name="indian-address-matcher",
    version="0.1.3",
    description="A tool for matching Indian addresses to determine if they refer to the same location",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Karan Choudhary",
    author_email="kchoudhary510199@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "address-matcher=address_matcher.cli:main",
        ],
    },
    url="https://github.com/Karan-Choudhary/indian-address-matcher",
    project_urls={
        "Bug Tracker": "https://github.com/Karan-Choudhary/indian-address-matcher/issues",
        "Documentation": "https://github.com/Karan-Choudhary/indian-address-matcher#readme",
        "Source Code": "https://github.com/Karan-Choudhary/indian-address-matcher",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 