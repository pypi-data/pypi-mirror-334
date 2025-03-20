from setuptools import setup, find_packages

setup(
    name="slg-script-helpers",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
    ],
    author="Steven Gotting",
    author_email="sgotting21@gmail.com",  # Replace with your email
    description="Helper functions for Python scripts including standardized config handling",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/slgotting/script-helpers",  # Replace with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)