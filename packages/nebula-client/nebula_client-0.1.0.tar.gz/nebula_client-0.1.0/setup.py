from setuptools import setup, find_packages

setup(
    name="nebula-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Nebula Team",
    author_email="support@nebula-app.com",
    description="Python client for the Nebula file system API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nebula/nebula-client-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 