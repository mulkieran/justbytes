# -*- coding: utf-8 -*-
# Copyright (C) 2015 - 2019 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <http://www.gnu.org/licenses/>.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

"""
Python packaging file for setup tools.
"""

# isort: STDLIB
import os

# isort: THIRDPARTY
import setuptools


def local_file(name):
    """
    Function to obtain the relative path of a filename.
    """
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


README = local_file("README.rst")

with open(local_file("src/justbytes/version.py")) as o:
    exec(o.read())  # pylint: disable=exec-used

setuptools.setup(
    name="justbytes",
    version=__version__,  # pylint: disable=undefined-variable
    url="http://pythonhosted.org/justbytes/",
    author="Anne Mulhern",
    author_email="amulhern@redhat.com",
    description="computing with and displaying bytes",
    long_description=open(README, encoding="utf-8").read(),
    long_description_content_type="text/x-rst",
    platforms=["Linux"],
    license="LGPLv2+",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "Topic :: System :: Operating System Kernels :: Linux",
    ],
    install_requires=["justbases>=0.13"],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
)
