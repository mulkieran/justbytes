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

""" Tests for operations on Range objects. """

import copy

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
    @settings(max_examples=50)
    def testRepr(self, value):
        """ Test that repr looks right. """
        self.assertEqual("%r" % value, "Range(%r)" % value.magnitude)

    def testDeepCopy(self):
        """ Test that deepcopy is different but equal. """
        s1 = Range(0)
        s2 = copy.deepcopy(s1)
        self.assertEqual(s1, s2)
        s1._magnitude += 1
        self.assertNotEqual(s1, s2)
