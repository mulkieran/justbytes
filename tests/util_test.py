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

""" Test for utility functions. """
from decimal import Decimal
from fractions import Fraction

import unittest

from hypothesis import given
from hypothesis import strategies
from hypothesis import Settings

from justbytes._constants import RoundingMethods
from justbytes._errors import SizeValueError
from justbytes._util.math_util import get_repeating_fraction
from justbytes._util.math_util import round_fraction
from justbytes._util.misc import get_string_info
from justbytes._util.misc import long_decimal_division

from .utils import NUMBERS_STRATEGY


class FormatTestCase(unittest.TestCase):
    """ Test formatting. """

    def testException(self):
        """ Raises exception on bad input. """
        with self.assertRaises(SizeValueError):
            get_string_info(Decimal(200), places=-1)
        with self.assertRaises(SizeValueError):
            get_string_info(0.1, places=0)

    @given(
       strategies.integers(min_value=1),
       strategies.integers(),
       strategies.integers(min_value=0, max_value=5),
       strategies.integers(min_value=0, max_value=5),
       settings=Settings(max_examples=10)
    )
    def testExactness(self, p, q, n, m):
        """ When max_places is not specified and the denominator of
            the value is 2^n * 5^m the result is exact.
        """
        x = Fraction(p * q, p * (2**n * 5**m))
        (exact, sign, left, right) = get_string_info(x, places=None)
        self.assertEqual(sign * Fraction("%s.%s" % (left, right)), x)
        self.assertTrue(exact)


class RoundingTestCase(unittest.TestCase):
    """ Test rounding of fraction. """
    # pylint: disable=too-few-public-methods

    def testExceptions(self):
        """ Raises exception on bad input. """
        with self.assertRaises(SizeValueError):
            round_fraction(Fraction(13, 32), "a string")
        with self.assertRaises(SizeValueError):
            round_fraction(Fraction(16, 32), "a string")

    @given(
       strategies.integers(min_value=1, max_value=9),
       settings=Settings(max_examples=20)
    )
    def testRounding(self, i):
        """ Rounding various values according to various methods. """
        f = Fraction(i, 10)
        self.assertEqual(round_fraction(f, RoundingMethods.ROUND_DOWN), 0)
        self.assertEqual(round_fraction(f, RoundingMethods.ROUND_UP), 1)

        r = round_fraction(f, RoundingMethods.ROUND_HALF_UP)
        if i < 5:
            self.assertEqual(r, 0)
        else:
            self.assertEqual(r, 1)

        r = round_fraction(f, RoundingMethods.ROUND_HALF_DOWN)
        if i > 5:
            self.assertEqual(r, 1)
        else:
            self.assertEqual(r, 0)

class LongDecimalDivisionTestCase(unittest.TestCase):
    """
    Test long decimal division.
    """

    def testException(self):
        """
        Test exceptions.
        """
        with self.assertRaises(SizeValueError):
            long_decimal_division(1.2, 1)
        with self.assertRaises(SizeValueError):
            long_decimal_division(1, 1.2)
        with self.assertRaises(SizeValueError):
            long_decimal_division(0, 1)

    @given(
       NUMBERS_STRATEGY.filter(lambda x: x != 0),
       strategies.integers().filter(lambda x: x > 0),
       settings=Settings(max_examples=20)
    )
    def testExact(self, divisor, multiplier):
        """
        A divisor that divides the dividend has no decimal part.
        """
        dividend = Fraction(divisor) * multiplier
        res = long_decimal_division(divisor, dividend)
        self.assertEqual(res[3], [])
        self.assertEqual(res[2], [])
        self.assertEqual(res[1], multiplier)
        self.assertEqual(res[0], 1)

    @given(
       NUMBERS_STRATEGY.filter(lambda x: x != 0),
       strategies.integers().filter(lambda x: x > 0),
       settings=Settings(max_examples=20)
    )
    def testNonRepeatingDecimal(self, divisor, multiplier):
        """
        Should always end in .5.
        """
        dividend = Fraction(divisor) * (multiplier + Fraction(1, 2))
        res = long_decimal_division(divisor, dividend)
        self.assertEqual(res[3], [])
        self.assertEqual(res[2], [5])
        self.assertEqual(res[1], multiplier)
        self.assertEqual(res[0], 1)

    @given(
       NUMBERS_STRATEGY.filter(lambda x: x != 0),
       strategies.integers().filter(lambda x: x > 0),
       settings=Settings(max_examples=20)
    )
    def testRepeatingDecimal(self, divisor, multiplier):
        """
        Should always end in .33333.....
        """
        dividend = Fraction(divisor) * (multiplier + Fraction(1, 3))
        res = long_decimal_division(divisor, dividend)
        self.assertEqual(res[3], [3])
        self.assertEqual(res[2], [])
        self.assertEqual(res[1], multiplier)
        self.assertEqual(res[0], 1)

    @given(
       NUMBERS_STRATEGY.filter(lambda x: x != 0),
       strategies.integers().filter(lambda x: x > 0),
       settings=Settings(max_examples=20)
    )
    def testComplexRepeatingDecimal(self, divisor, multiplier):
        """
        Should always end in .16666.....
        """
        dividend = Fraction(divisor) * (multiplier + Fraction(1, 6))
        res = long_decimal_division(divisor, dividend)
        self.assertEqual(res[3], [6])
        self.assertEqual(res[2], [1])
        self.assertEqual(res[1], multiplier)
        self.assertEqual(res[0], 1)

    @given(
       NUMBERS_STRATEGY.filter(lambda x: x != 0),
       strategies.integers().filter(lambda x: x > 0),
       settings=Settings(max_examples=20)
    )
    def testMoreComplexRepeatingDecimal(self, divisor, multiplier):
        """
        Should always end in .142857142857....
        """
        dividend = Fraction(divisor) * (multiplier + Fraction(1, 7))
        res = long_decimal_division(divisor, dividend)
        self.assertEqual(res[3], [1, 4, 2, 8, 5, 7])
        self.assertEqual(res[2], [])
        self.assertEqual(res[1], multiplier)
        self.assertEqual(res[0], 1)


class GetRepeatingFractionTestCase(unittest.TestCase):
    """
    Test get_repeating_fraction.
    """

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(SizeValueError):
            get_repeating_fraction(1, 0)
        with self.assertRaises(SizeValueError):
            get_repeating_fraction(-1, 1)
        with self.assertRaises(SizeValueError):
            get_repeating_fraction(3, 2)
