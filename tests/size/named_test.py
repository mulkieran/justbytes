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

from hypothesis import assume
from hypothesis import example
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbytes import Size
from justbytes import B
from justbytes import ROUND_DOWN
from justbytes import ROUND_HALF_DOWN
from justbytes import ROUND_HALF_UP
from justbytes import ROUND_TO_ZERO
from justbytes import ROUND_UP
from justbytes import ROUNDING_METHODS
from justbytes import StrConfig

from justbytes._constants import BinaryUnits
from justbytes._constants import DecimalUnits
from justbytes._constants import UNITS

from justbytes._errors import SizeValueError

from tests.utils import SIZE_STRATEGY

class ConversionTestCase(unittest.TestCase):
    """ Test conversion methods. """

    def testException(self):
        """ Test exceptions. """
        with self.assertRaises(SizeValueError):
            Size(0).convertTo(-2)
        with self.assertRaises(SizeValueError):
            Size(0).convertTo(0)
        with self.assertRaises(SizeValueError):
            Size(512).convertTo(1.4)

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
          max_places=strategies.integers(min_value=0, max_value=5),
          unit=strategies.sampled_from(UNITS() + [None])
       )
    )
    @settings(max_examples=200)
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


class RoundingTestCase(unittest.TestCase):
    """ Test rounding methods. """

    @given(
       SIZE_STRATEGY,
       strategies.one_of(
          SIZE_STRATEGY.filter(lambda x: x.magnitude >= 0),
          strategies.sampled_from(UNITS())
       ),
       strategies.sampled_from(ROUNDING_METHODS()),
       strategies.tuples(
          strategies.one_of(strategies.none(), SIZE_STRATEGY),
          strategies.one_of(strategies.none(), SIZE_STRATEGY)
       )
    )
    def testBounds(self, s, unit, rounding, bounds):
        """
        Test that result is between the specified bounds,
        assuming that the bounds are legal.
        """
        (lower, upper) = bounds
        assume(lower is None or upper is None or lower <= upper)
        rounded = s.roundTo(unit, rounding, bounds)
        self.assertTrue(lower is None or lower <= rounded)
        self.assertTrue(upper is None or upper >= rounded)

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
        # pylint: disable=too-many-branches
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

        if rounding is ROUND_TO_ZERO:
            if s > Size(0):
                self.assertEqual(rounded, floor)
            else:
                self.assertEqual(rounded, ceiling)
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
            elif rounding is ROUND_HALF_DOWN:
                self.assertEqual(rounded, floor)
            else:
                if s > Size(0):
                    self.assertEqual(rounded, floor)
                else:
                    self.assertEqual(rounded, ceiling)

    def testExceptions(self):
        """ Test raising exceptions when rounding. """
        with self.assertRaises(SizeValueError):
            Size(0).roundTo(Size(-1, B), rounding=ROUND_HALF_UP)
        with self.assertRaises(SizeValueError):
            Size(512).roundTo(1.4, rounding=ROUND_HALF_UP)
        with self.assertRaises(SizeValueError):
            s = Size(512)
            s.roundTo(512, rounding=ROUND_HALF_UP, bounds=(Size(0), Size(-1)))
