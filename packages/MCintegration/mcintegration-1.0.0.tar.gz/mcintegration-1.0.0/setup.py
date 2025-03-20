from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = "1.0.0"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs]

setup(
    name="MCintegration",
    version=__version__,
    description="PyTorch implementation of Monte Carlo integration with support for the Vegas algorithm",
    keywords="Monte Carlo, integration, Vegas, PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/numericalEFT/MCintegration.py",
    download_url="https://github.com/numericalEFT/MCintegration.py/archive/refs/heads/master.zip",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["docs", "examples", "*_test.py"]),
    include_package_data=True,
    author="Kun Chen, Pengcheng Hou, Tao Wang and Caiyu Fan",
    author_email="chenkun0228@gmail.com, houpc96@gmail.com, taowang@umass.edu, fancaiyu24@mails.ucas.ac.cn",
    install_requires=install_requires,
    extras_require={
        "docs": ["mkdocs","mkdocstrings[python]","mkdocs-jupyter"]
    },
)
