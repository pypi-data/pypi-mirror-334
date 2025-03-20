# setup.py
from setuptools import setup, find_packages

setup(
    name="demonproto_x",
    version="0.9",
    packages=find_packages(),
    install_requires=[
        'cryptography',
    ],
    description="End-to-end encryption chat protocol",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="ALfisene Keita",
    author_email="info@infopeklo.cz",
    url="https://github.com/certikpolik1/thecryptoxprotox",
)
