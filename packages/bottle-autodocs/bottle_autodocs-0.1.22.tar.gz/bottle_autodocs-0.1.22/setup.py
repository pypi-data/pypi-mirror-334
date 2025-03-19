from setuptools import setup, find_packages

setup(
    name="bottle-autodocs",
    version="0.1.22",
    description="Automated OpenAPI 3.1.0 documentation for Bottle",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Naveen",
    author_email="naveen.ayyakannan@gmail.com",
    url="https://github.com/hizinberg/bottle-autodocs",
    license="MIT",
    packages=find_packages(),
    install_requires=["bottle>=0.12"],
    python_requires=">=3.7",
)
