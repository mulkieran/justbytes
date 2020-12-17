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

# isort: STDLIB
import unittest

# isort: THIRDPARTY
from hypothesis import given, settings, strategies

# isort: LOCAL
from justbytes import UNITS, Range


class ConversionTestCase(unittest.TestCase):
    """ Test conversions. """

    @given(strategies.integers(), strategies.sampled_from(UNITS()))
    @settings(max_examples=5)
    def testInt(self, s, u):
        """ Test integer conversions. """
        self.assertEqual(int(Range(s, u)), s * int(u))

    @given(
        strategies.builds(
            Range, strategies.integers(), strategies.sampled_from(UNITS())
        )
    )
    @settings(max_examples=50)
    def testRepr(self, value):
        """ Test that repr looks right. """
        self.assertEqual("%r" % value, "Range(%r)" % value.magnitude)
