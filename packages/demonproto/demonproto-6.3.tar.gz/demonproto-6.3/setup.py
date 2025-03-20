# setup.py
from setuptools import setup, find_packages

setup(
    name="demonproto",
    version="6.3",
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'DoubleRatchet',
    ],
    description="End-to-end encryption chat protocol",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="ALfisene Keita",
    author_email="info@infopeklo.cz",
    url="https://github.com/certikpolik1/thecryptoxprotox",
)
