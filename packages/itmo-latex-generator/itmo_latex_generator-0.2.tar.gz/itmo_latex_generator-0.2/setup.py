from setuptools import setup, find_packages

setup(
    name="itmo_latex_generator",
    version="0.2",
    packages=find_packages(),
    install_requires=[],
    author="Anastasiya Valueva",
    author_email="valueva200211@gmail.com",
    description="ITMO 2025. A simple LaTeX generator for tables and images",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VoLuIcHiK/latex_generator_itmo",
)