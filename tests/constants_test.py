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
