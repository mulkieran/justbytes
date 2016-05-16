# -*- coding: utf-8 -*-
# Copyright (C) 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

import os
import sys
import setuptools
if sys.version_info[0] < 3:
    from codecs import open

def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))

README = local_file("README.rst")

with open(local_file("src/justbytes/version.py")) as o:
        exec(o.read())

setuptools.setup(
    name='justbytes',
    version=__version__,
    url='http://pythonhosted.org/justbytes/',
    author='Anne Mulhern',
    author_email='amulhern@redhat.com',
    description='computing with and displaying bytes',
    long_description=open(README, encoding='utf-8').read(),
    platforms=['Linux'],
    license='GPL 2+',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'Topic :: System :: Operating System Kernels :: Linux',
    ],
    install_requires = [
        'justbases>0.07',
        'six'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    )
