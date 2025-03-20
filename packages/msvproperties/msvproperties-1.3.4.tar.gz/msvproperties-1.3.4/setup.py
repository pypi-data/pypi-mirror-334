from setuptools import setup, find_packages
import os

def read_requirements():
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.exists(req_file):
        return []
    with open(req_file) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="msvproperties",
    version="1.3.4",
    packages=find_packages(),
    license="MIT",
    install_requires=read_requirements(),
    python_requires="<4",
    description="A Library for using in our CRM",
    author="Alireza",
    author_email="alireza@msvproperties.net",
    url="https://github.com/alireza-msvproperties/msvproperties/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
    ],
)
