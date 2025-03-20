from setuptools import setup, find_packages

setup(
    name="pretty-cli-logger", 
    version='1.0.4' ,
    author="Oscar Harvey",
    author_email="<oscar.harvey371@gmail.com>",
    description='Zero-dependency colorful CLI logger',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',

    packages=find_packages(),
    install_requires=[],

    include = ["LICENSE", "README.md"],
    license = "Apache-2.0",

    keywords=['logger', 'pretty', 'cli-logger', 'pretty-cli-logger'],
    classifiers = [
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
