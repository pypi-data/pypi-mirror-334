#!/usr/bin/python3
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

from clipboard_text_correction.about import __version__
from clipboard_text_correction.about import __author__
from clipboard_text_correction.about import __email__
from clipboard_text_correction.about import __description__
from clipboard_text_correction.about import __url_source__
from clipboard_text_correction.about import __url_funding__
from clipboard_text_correction.about import __url_bugs__

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8");

setup(
    name="clipboard_text_correction",
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    url=__url_source__,
    keywords="writing, spelling",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        'deep-consultation',
        'textstat'
    ],
    entry_points={
        'console_scripts': [
            'clipboard-text-correction-indicator=clipboard_text_correction.indicator:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    package_data={
        'clipboard_text_correction': ['icons/logo.png'],
    },
    include_package_data=True, 
    project_urls={  # Optional
        "Bug Reports": __url_bugs__,
        "Funding": __url_funding__,
        "Source": __url_source__,
    },
)
