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
import unittest

from hypothesis import given
from hypothesis import strategies

from justbytes._constants import B
from justbytes._constants import BinaryUnits
from justbytes._constants import DecimalUnits
from justbytes._constants import RoundingMethods
from justbytes._constants import UNITS

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

    @given(
       strategies.integers(
          min_value=0,
          max_value=BinaryUnits.max_exponent()
       ),
       strategies.integers(
          min_value=0,
          max_value=DecimalUnits.max_exponent()
       )
    )
    def testExpMethod(self, bexp, dexp):
        """ Test extracting unit for a given exponent. """
        self.assertEqual(
           BinaryUnits.unit_for_exp(bexp).factor,
           BinaryUnits.FACTOR ** bexp
        )
        self.assertEqual(
           DecimalUnits.unit_for_exp(dexp).factor,
           DecimalUnits.FACTOR ** dexp
        )

    def testExpExceptions(self):
        """
        Test that exceptions are properly raised.
        """
        with self.assertRaises(RangeValueError):
            DecimalUnits.unit_for_exp(-1)
