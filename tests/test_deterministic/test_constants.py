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

""" Test for constants classes. """
# isort: STDLIB
import unittest

# isort: LOCAL
from justbytes._constants import UNITS, B, BinaryUnits, DecimalUnits, RoundingMethods
from justbytes._errors import RangeValueError


class ConstantsTestCase(unittest.TestCase):
    """ Exercise methods of constants classes. """

    def testRoundingObjects(self):
        """ Miscellaneous tests for rounding constants. """
        self.assertIsInstance(str(RoundingMethods.ROUND_DOWN), str)

    def testUnitsObjects(self):
        """ Miscellaneous tests for units constants. """
        self.assertIsInstance(str(DecimalUnits.KB), str)
        self.assertIsNotNone(DecimalUnits.KB.prefix)

    def testUnitsMethod(self):
        """ Test that all units constansts are in UNITS(). """
        self.assertTrue(set(DecimalUnits.UNITS()).issubset(set(UNITS())))
        self.assertTrue(set(BinaryUnits.UNITS()).issubset(set(UNITS())))
        self.assertTrue(B in UNITS())

    def testExpExceptions(self):
        """
        Test that exceptions are properly raised.
        """
        with self.assertRaises(RangeValueError):
            DecimalUnits.unit_for_exp(-1)
