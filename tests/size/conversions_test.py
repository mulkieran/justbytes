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

""" Tests for operations on Range objects. """

import copy
import re

import unittest

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbytes import Range
from justbytes import UNITS

class ConversionTestCase(unittest.TestCase):
    """ Test conversions. """

    def testBool(self):
        """ Test conversion to bool.

            Note that bool calls __bool__() in Python 3, __nonzero__ in Python2.
        """
        self.assertFalse(bool(Range(0)))
        self.assertFalse(Range(0).__bool__())

        self.assertTrue(bool(Range(1)))
        self.assertTrue(Range(1).__bool__())

    @given(
       strategies.integers(),
       strategies.sampled_from(UNITS())
    )
    @settings(max_examples=5)
    def testInt(self, s, u):
        """ Test integer conversions. """
        self.assertEqual(int(Range(s, u)), s * int(u))

    def testFloat(self):
        """ Test float conversion.

            Converting a Range to a float should require some effort.
        """
        with self.assertRaises(TypeError):
            float(Range(0))

    @given(
       strategies.builds(
          Range,
          strategies.integers(),
          strategies.sampled_from(UNITS())
       )
    )
    @settings(max_examples=5)
    def testRepr(self, value):
        """ Test that repr looks right. """
        regex = re.compile(r"Range\((?P<val>-?[0-9]+)\)")
        match = re.match(regex, "%r" % value)
        self.assertIsNotNone(match)
        self.assertEqual(int(match.group('val')), int(value))

    def testDeepCopy(self):
        """ Test that deepcopy is different but equal. """
        s1 = Range(0)
        s2 = copy.deepcopy(s1)
        self.assertEqual(s1, s2)
        s1._magnitude += 1
        self.assertNotEqual(s1, s2)
