from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="geo_convert_util",
    version="0.0.1",
    author="paulosergiocf",
    author_email="paulosergiocf.dev@gmail.com",
    description="Conversões de áreas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulosergiocf/geoutil",
    packages=find_packages(),   
    install_requires=requirements,  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  python_requires='>=3.7',
)