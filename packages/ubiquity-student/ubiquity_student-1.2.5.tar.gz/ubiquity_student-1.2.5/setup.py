"""module allowing the creation of a pypi package"""
#      ubiquity
#      Copyright (C) 2022  INSA Rouen Normandie - CIP
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

from setuptools import setup, find_packages
from ubiquitysoftware import __version__


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md'), "r", encoding="utf8") as readme:
    long_description = readme.read()

setup(
    name='ubiquity-student',
    version=__version__,

    packages=find_packages(where="src"),
    package_dir={"":"src"},
    include_package_data=True,

    classifiers=[
        'Topic :: Education',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Natural Language :: French',
    ],

    url='https://gitlab.insa-rouen.fr/cip/ubiquity',
    download_url='https://gitlab.insa-rouen.fr/cip/ubiquity/-/tags',
    project_urls={
        'Documentation': 'https://gitlab.insa-rouen.fr/cip/ubiquity/-/wikis/home',
        'Bug Tracker': 'https://gitlab.insa-rouen.fr/cip/ubiquity/-/issues',
    },

    description='Ubiquity permet le suivi de TP de développement informatique',
    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=["requests"],

    entry_points={
        "console_scripts": [
            'ubiquity-student = ubiquitysoftware.ubiquity_student:main'
        ]
    },
    python_requires=">=3.7",
)
