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

""" Tests for Range initialization. """

# isort: STDLIB
import unittest
from decimal import Decimal

# isort: LOCAL
from justbytes import B, Range
from justbytes._errors import RangeValueError


class InitializerTestCase(unittest.TestCase):
    """ Test conversions. """

    def testExceptions(self):
        """ Test exceptions. """
        with self.assertRaises(RangeValueError):
            Range(1.23)
        with self.assertRaises(RangeValueError):
            Range("1.2.3")
        with self.assertRaises(RangeValueError):
            Range(Decimal("NaN"))

        s = Range(0)
        with self.assertRaises(RangeValueError):
            Range(s, B)

        with self.assertRaises(RangeValueError):
            Range(1, 1.2)

        with self.assertRaises(RangeValueError):
            Range(1, Decimal("NaN"))
