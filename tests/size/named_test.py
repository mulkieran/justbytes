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

""" Tests for named methods of Size objects. """

from fractions import Fraction

import unittest

from hypothesis import example
from hypothesis import given
from hypothesis import strategies
from hypothesis import Settings

from justbytes import Size
from justbytes import B
from justbytes import ROUND_DOWN
from justbytes import ROUND_HALF_UP
from justbytes import ROUND_UP
from justbytes import ROUNDING_METHODS
from justbytes import StrConfig

from justbytes._constants import BinaryUnits
from justbytes._constants import DecimalUnits
from justbytes._constants import UNITS

from justbytes._errors import SizeValueError

from justbytes._util.misc import get_string_info

from tests.utils import SIZE_STRATEGY

class ConversionTestCase(unittest.TestCase):
    """ Test conversion methods. """

    def testException(self):
        """ Test exceptions. """
        with self.assertRaises(SizeValueError):
            Size(0).convertTo(-2)
        with self.assertRaises(SizeValueError):
            Size(0).convertTo(0)

    @given(
       strategies.builds(Size, strategies.integers()),
       strategies.one_of(
           strategies.none(),
           strategies.sampled_from(UNITS()),
           strategies.builds(Size, strategies.integers(min_value=1))
       )
    )
    def testPrecision(self, s, u):
        """ Test precision of conversion. """
        factor = (u and int(u)) or int(B)
        self.assertEqual(s.convertTo(u) * factor, int(s))

class ComponentsTestCase(unittest.TestCase):
    """ Test components method. """

    @given(
       SIZE_STRATEGY,
       strategies.builds(
          StrConfig,
          min_value=strategies.fractions().filter(lambda x: x >= 0),
          binary_units=strategies.booleans(),
          exact_value=strategies.booleans(),
          max_places=strategies.integers().filter(lambda x: x >= 0 and x < 64),
          unit=strategies.sampled_from(UNITS() + [None])
       ),
       settings=Settings(max_examples=100)
    )
    def testResults(self, s, config):
        """ Test component results. """
        (m, u) = s.components(config)
        self.assertEqual(m * int(u), s.magnitude)
        if u == B:
            return

        if config.unit is None:
            if config.binary_units:
                self.assertIn(u, BinaryUnits.UNITS())
            else:
                self.assertIn(u, DecimalUnits.UNITS())
            self.assertTrue(abs(m) >= config.min_value)
        else:
            self.assertEqual(u, config.unit)


        (exact, sign, left, right) = get_string_info(
           m,
           places=config.max_places
        )
        value = sign * Fraction("%s.%s" % (left, right))
        if config.exact_value and config.unit is None:
            self.assertTrue(exact)
            self.assertTrue(Fraction(value) * int(u) == s.magnitude)
        if not exact:
            self.assertFalse(Fraction(value) * int(u) == s.magnitude)

class RoundingTestCase(unittest.TestCase):
    """ Test rounding methods. """

    @given(
       SIZE_STRATEGY,
       strategies.one_of(
          SIZE_STRATEGY.filter(lambda x: x.magnitude >= 0),
          strategies.sampled_from(UNITS())
       ),
       strategies.sampled_from(ROUNDING_METHODS())
    )
    @example(Size(32), Size(0), ROUND_DOWN)
    def testResults(self, s, unit, rounding):
        """ Test roundTo results. """
        rounded = s.roundTo(unit, rounding)

        if (isinstance(unit, Size) and unit.magnitude == 0) or \
           (not isinstance(unit, Size) and int(unit) == 0):
            self.assertEqual(rounded, Size(0))
            return

        converted = s.convertTo(unit)
        if converted.denominator == 1:
            self.assertEqual(rounded, s)
            return

        factor = getattr(unit, 'magnitude', None) or int(unit)
        (q, r) = divmod(converted.numerator, converted.denominator)
        ceiling = Size((q + 1) * factor)
        floor = Size(q * factor)
        if rounding is ROUND_UP:
            self.assertEqual(rounded, ceiling)
            return

        if rounding is ROUND_DOWN:
            self.assertEqual(rounded, floor)
            return

        remainder = abs(Fraction(r, converted.denominator))
        half = Fraction(1, 2)
        if remainder > half:
            self.assertEqual(rounded, ceiling)
        elif remainder < half:
            self.assertEqual(rounded, floor)
        else:
            if rounding is ROUND_HALF_UP:
                self.assertEqual(rounded, ceiling)
            else:
                self.assertEqual(rounded, floor)

    def testExceptions(self):
        """ Test raising exceptions when rounding. """
        with self.assertRaises(SizeValueError):
            Size(0).roundTo(Size(-1, B), rounding=ROUND_HALF_UP)


class DecimalInfoTestCase(unittest.TestCase):
    """
    Test calculation of decimal info.
    """

    @given(
       SIZE_STRATEGY,
       settings=Settings(max_examples=30)
    )
    def testEquivalence(self, s):
        """
        Verify that decimal info and corresponding string are same.
        """
        config = StrConfig(max_places=None)
        (sign, left, non_repeating, repeating, units) = s.getDecimalInfo(config)
        (approx, new_sign, new_left, right, new_units) = s.getStringInfo(config)

        self.assertEqual(sign, new_sign)
        self.assertEqual(str(left), new_left)
        self.assertEqual(units, new_units)
        if not approx:
            self.assertEqual(repeating, [])
            self.assertEqual(
               s,
               Size(new_sign * Fraction("%s.%s" % (new_left, right)), units)
            )
            non_repeating = "".join(str(x) for x in non_repeating)
            self.assertEqual(
               s,
               Size(sign * Fraction("%s.%s" % (left, non_repeating)), units)
            )
