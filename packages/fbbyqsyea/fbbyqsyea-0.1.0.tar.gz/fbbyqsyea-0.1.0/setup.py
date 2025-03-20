from setuptools import setup, find_packages

setup(
    name="fbbyqsyea",
    version="0.1.0",
    author="fbbyqsyea",
    author_email="fbbyqsyea@163.com",
    description="A simple Python utility package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fbbyqsyea/fbbyqsyea",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
