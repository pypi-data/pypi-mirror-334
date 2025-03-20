from setuptools import setup, find_packages

setup(
    name="TomatoPy",
    version="0.1.1",
    author="Tal Gluck",
    # author_email="your.email@example.com",
    description="Make pizza with Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/talagluck/tomatopy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)