import codecs
from os import path
from i3_quickterm.version import __version__

from setuptools import setup, find_packages

# from https://packaging.python.org/guides/single-sourcing-package-version/
here = path.abspath(path.dirname(__file__))


def read(*parts):
    with codecs.open(path.join(here, *parts), "r") as fp:
        return fp.read()


with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="i3-qt",
    version=__version__,
    description="A small drop-down terminal for i3 and sway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laur89/i3-quickterm",
    author="laur89",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment",
        "Topic :: Terminals :: Terminal Emulators/X Terminals",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="i3 i3wm extensions add-ons",
    packages=find_packages(where="."),
    license='MIT',
    python_requires=">=3.8",
    install_requires=["i3ipc>=2.0.1", "tendo"],
    # extras_require={
        # "dev": ["coverage", "mypy", "pytest", "ruff"],
    # },
    entry_points={
        "console_scripts": [
            "i3-quickterm=i3_quickterm.i3_quickterm:main",
            "i3-qt=i3_quickterm.i3_quickterm:main",
            "i3qt=i3_quickterm.i3_quickterm:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/laur89/i3-quickterm/issues",
        "Source": "https://github.com/laur89/i3-quickterm",
    },
)
