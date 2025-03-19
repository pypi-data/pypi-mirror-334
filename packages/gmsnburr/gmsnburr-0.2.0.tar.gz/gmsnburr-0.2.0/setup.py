from setuptools import setup, find_packages

setup(
    name="gmsnburr",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "pymc",
        "pytensor",
        "arviz",
        "scipy",
        "matplotlib",
    ],
    author="Ezra Zia Izdihara",
    author_email="ezrazia05@gmail.com",
    description="Distribusi GMSN-Burr dengan PyMC",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/gmsnburr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
