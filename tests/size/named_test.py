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

""" Tests for named methods of Range objects. """

from fractions import Fraction

import string
import unittest

from hypothesis import assume
from hypothesis import example
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbytes import Range
from justbytes import B
from justbytes import ROUND_DOWN
from justbytes import ROUND_HALF_DOWN
from justbytes import ROUND_HALF_UP
from justbytes import ROUND_TO_ZERO
from justbytes import ROUND_UP
from justbytes import ROUNDING_METHODS
from justbytes import BaseConfig
from justbytes import Config
from justbytes import DigitsConfig
from justbytes import DisplayConfig
from justbytes import StringConfig
from justbytes import StripConfig
from justbytes import ValueConfig

from justbytes._constants import BinaryUnits
from justbytes._constants import DecimalUnits
from justbytes._constants import UNITS

from justbytes._errors import RangeValueError

from tests.utils import SIZE_STRATEGY

class ConversionTestCase(unittest.TestCase):
    """ Test conversion methods. """

    def testException(self):
        """ Test exceptions. """
        with self.assertRaises(RangeValueError):
            Range(0).convertTo(-2)
        with self.assertRaises(RangeValueError):
            Range(0).convertTo(0)
        with self.assertRaises(RangeValueError):
            Range(512).convertTo(1.4)

    @given(
       strategies.builds(Range, strategies.integers()),
       strategies.one_of(
           strategies.none(),
           strategies.sampled_from(UNITS()),
           strategies.builds(Range, strategies.integers(min_value=1))
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
          ValueConfig,
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


class DisplayConfigTestCase(unittest.TestCase):
    """
    Test some aspects of the getString() method.
    """

    @given(
       SIZE_STRATEGY,
       strategies.builds(
          DisplayConfig,
          show_approx_str=strategies.booleans(),
          base_config=strategies.just(BaseConfig()),
          digits_config=strategies.just(DigitsConfig(use_letters=False)),
          strip_config=strategies.just(StripConfig())
       ),
       strategies.integers(min_value=2, max_value=16)
    )
    @settings(max_examples=100)
    def testConfig(self, a_size, config, base):
        """
        Test properties of configuration.
        """
        result = a_size.getString(
           StringConfig(
              ValueConfig(base=base),
              config,
              Config.STRING_CONFIG.DISPLAY_IMPL_CLASS
           )
        )

        if config.base_config.use_prefix and base == 16:
            self.assertNotEqual(result.find('0x'), -1)

class DigitsConfigTestCase(unittest.TestCase):
    """
    Test digits config.
    """

    @given(
       SIZE_STRATEGY,
       strategies.builds(
          DigitsConfig,
          separator=strategies.text(alphabet='-/*j:', max_size=1),
          use_caps=strategies.booleans(),
          use_letters=strategies.booleans()
       )
    )
    @settings(max_examples=50)
    def testConfig(self, a_size, config):
        """
        Test some basic configurations.
        """
        result = a_size.getString(
           StringConfig(
              Config.STRING_CONFIG.VALUE_CONFIG,
              DisplayConfig(digits_config=config),
              Config.STRING_CONFIG.DISPLAY_IMPL_CLASS
           )
        )
        if config.use_letters:
            (number, _, _) = result.partition(' ')
            letters = [r for r in number if r in string.ascii_letters]
            if config.use_caps:
                self.assertTrue(
                   all(r in string.ascii_uppercase for r in letters)
                )
            else:
                self.assertTrue(
                   all(r in string.ascii_lowercase for r in letters)
                )

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(RangeValueError):
            Range(0).getString(
               StringConfig(
                  ValueConfig(base=100),
                  Config.STRING_CONFIG.DISPLAY_CONFIG,
                  Config.STRING_CONFIG.DISPLAY_IMPL_CLASS
               )
            )


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
    @example(Range(32), Range(0), ROUND_DOWN)
    def testResults(self, s, unit, rounding):
        """ Test roundTo results. """
        # pylint: disable=too-many-branches
        rounded = s.roundTo(unit, rounding)

        if (isinstance(unit, Range) and unit.magnitude == 0) or \
           (not isinstance(unit, Range) and int(unit) == 0):
            self.assertEqual(rounded, Range(0))
            return

        converted = s.convertTo(unit)
        if converted.denominator == 1:
            self.assertEqual(rounded, s)
            return

        factor = getattr(unit, 'magnitude', None) or int(unit)
        (q, r) = divmod(converted.numerator, converted.denominator)
        ceiling = Range((q + 1) * factor)
        floor = Range(q * factor)
        if rounding is ROUND_UP:
            self.assertEqual(rounded, ceiling)
            return

        if rounding is ROUND_DOWN:
            self.assertEqual(rounded, floor)
            return

        if rounding is ROUND_TO_ZERO:
            if s > Range(0):
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
                if s > Range(0):
                    self.assertEqual(rounded, floor)
                else:
                    self.assertEqual(rounded, ceiling)

    def testExceptions(self):
        """ Test raising exceptions when rounding. """
        with self.assertRaises(RangeValueError):
            Range(0).roundTo(Range(-1, B), rounding=ROUND_HALF_UP)
        with self.assertRaises(RangeValueError):
            Range(512).roundTo(1.4, rounding=ROUND_HALF_UP)
        with self.assertRaises(RangeValueError):
            s = Range(512)
            s.roundTo(512, rounding=ROUND_HALF_UP, bounds=(Range(0), Range(-1)))
