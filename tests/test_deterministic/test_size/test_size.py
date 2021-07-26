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

""" Tests for behavior of Range objects. """

# isort: STDLIB
import unittest
from fractions import Fraction

# isort: LOCAL
from justbytes import (
    KB,
    B,
    DisplayConfig,
    GiB,
    KiB,
    MiB,
    Range,
    StripConfig,
    TiB,
    ValueConfig,
)
from justbytes._config import Config
from justbytes._errors import RangeFractionalResultError, RangeValueError


class ConstructionTestCase(unittest.TestCase):
    """ Test construction of Range objects. """

    def test_zero(self):
        """ Test construction with 0 as decimal. """
        zero = Range(0)
        self.assertEqual(zero, Range("0.0"))

    def test_negative(self):
        """ Test construction of negative sizes. """
        size = Range(-500, MiB)
        self.assertEqual(size.components(), (Fraction(-500, 1), MiB))
        self.assertEqual(size.convertTo(B), -524288000)

    def test_constructor(self):
        """ Test error checking in constructo. """
        with self.assertRaises(RangeValueError):
            Range("1.1.1", KiB)
        self.assertEqual(Range(Range(0)), Range(0))
        with self.assertRaises(RangeValueError):
            Range(Range(0), KiB)
        with self.assertRaises(RangeValueError):
            Range(B)

    def test_no_units_in_string(self):
        """ Test construction w/ no units specified. """
        self.assertEqual(Range("1024"), Range(1, KiB))

    def test_fraction(self):
        """ Test creating Range with Fraction. """
        self.assertEqual(Range(Fraction(1024, 2), KiB), Range(Fraction(1, 2), MiB))


class DisplayTestCase(unittest.TestCase):
    """ Test formatting Range for display. """

    def test_str(self):
        """ Test construction of display components. """
        size = Range("12.68", TiB)
        self.assertEqual(str(size), "12.68 TiB")

        size = Range("26.55", MiB)
        self.assertEqual(str(size), "26.55 MiB")

        size = Range("12.687", TiB)
        self.assertEqual(str(size), "< 12.69 TiB")

    def test_min_value(self):
        """ Test behavior on min_value parameter. """
        size = Range(9, MiB)
        self.assertEqual(size.components(), (Fraction(9, 1), MiB))
        self.assertEqual(
            size.components(ValueConfig(min_value=10)), (Fraction(9216, 1), KiB)
        )

        size = Range("0.5", GiB)
        self.assertEqual(
            size.components(ValueConfig(min_value=1)), (Fraction(512, 1), MiB)
        )
        self.assertEqual(
            size.components(ValueConfig(min_value=Fraction(1, 10))),
            (Fraction(1, 2), GiB),
        )
        self.assertEqual(
            size.components(ValueConfig(min_value=1)), (Fraction(512, 1), MiB)
        )

        # when min_value is 10 and single digit on left of decimal, display
        # with smaller unit.
        size = Range("7.18", KiB)
        self.assertEqual(size.components(ValueConfig(min_value=10))[1], B)
        size = Range("9.68", TiB)
        self.assertEqual(size.components(ValueConfig(min_value=10))[1], GiB)
        size = Range("4.29", MiB)
        self.assertEqual(size.components(ValueConfig(min_value=10))[1], KiB)

        # when min value is 100 and two digits on left of decimal
        size = Range("14", MiB)
        self.assertEqual(
            size.components(ValueConfig(min_value=100)), (Fraction(14 * 1024, 1), KiB)
        )

    def test_exception_values(self):
        """ Test that exceptions are properly raised on bad params. """
        size = Range(500)
        with self.assertRaises(RangeValueError):
            size.components(ValueConfig(min_value=-1))

    def test_rounding_to_bytes(self):
        """ Test that second part is B when rounding to bytes. """
        size = Range(500)
        self.assertEqual(size.components()[1], B)

    def test_si_units(self):
        """ Test binary_units param. """
        size = Range(1000)
        self.assertEqual(size.components(ValueConfig(binary_units=False)), (1, KB))


class ConfigurationTestCase(unittest.TestCase):
    """ Test setting configuration for display. """

    def setUp(self):
        """ Get current config. """
        self.str_config = Config.STRING_CONFIG.VALUE_CONFIG
        self.display_config = Config.STRING_CONFIG.DISPLAY_CONFIG

    def tearDown(self):
        """ Reset configuration to default. """
        Config.set_value_config(self.str_config)
        Config.set_display_config(self.display_config)

    def test_value_configs(self):
        """ Test str with various configuration options. """
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))

        # exactly 4 Pi
        size = Range(0x10000000000000)
        self.assertEqual(str(size), "4 PiB")

        size = Range(300, MiB)
        self.assertEqual(str(size), "300 MiB")

        size = Range("12.6998", TiB)
        self.assertEqual(str(size), "< 12.7 TiB")

        # byte values close to multiples of 2 are shown without trailing zeros
        size = Range(0xFF)
        self.assertEqual(str(size), "255 B")

        # a fractional quantity is shown if the value deviates
        # from the whole number of units by more than 1%
        size = Range(16384 - (Fraction(1024) / 100 + 1))
        self.assertEqual(str(size), "< 15.99 KiB")

        # test a very large quantity with no associated abbreviation or prefix
        size = Range(1024 ** 9)
        self.assertEqual(str(size), "1024 YiB")
        size = Range(1024 ** 9 - 1)
        self.assertEqual(str(size), "< 1024 YiB")
        size = Range(1024 ** 10)
        self.assertEqual(str(size), "1048576 YiB")

        size = Range(0xFFFFFFFFFFFFF)
        self.assertEqual(str(size), "< 4 PiB")

        size = Range(0xFFFF)
        # value is not exactly 64 KiB, but w/ 2 places, value is 64.00 KiB
        # so the trailing 0s are stripped.
        self.assertEqual(str(size), "< 64 KiB")

        Config.set_value_config(ValueConfig(max_places=3))
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))
        size = Range("23.7874", TiB)
        self.assertEqual(str(size), "> 23.787 TiB")

        Config.set_value_config(ValueConfig(min_value=10))
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))
        size = Range(8193)
        self.assertEqual(str(size), ("8193 B"))

        # if max_places is set to None, all digits are displayed
        Config.set_value_config(ValueConfig(max_places=None))
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))
        size = Range(0xFFFFFFFFFFFFF)
        self.assertEqual(
            str(size), "3.99999999999999911182158029987476766109466552734375 PiB"
        )
        size = Range(0x10000)
        self.assertEqual(str(size), ("64 KiB"))
        size = Range(0x10001)
        self.assertEqual(str(size), "64.0009765625 KiB")

        Config.set_value_config(ValueConfig(max_places=2))
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=False)))
        size = Range(1024 ** 9 + 1)
        self.assertEqual(str(size), "> 1024.00 YiB")

        size = Range(0xFFFFF)
        self.assertEqual(str(size), "< 1024.00 KiB")

    def test_str_with_small_deviations(self):
        """ Behavior when deviation from whole value is small. """
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))

        eps = 1024 * Fraction(1, 100) * Fraction(1, 2)

        # deviation is less than 1/2 of 1% of 1024
        size = Range(16384 - (eps - 1))
        self.assertEqual(str(size), "< 16 KiB")

        # deviation is greater than 1/2 of 1% of 1024
        size = Range(16384 - (eps + 1))
        self.assertEqual(str(size), "> 15.99 KiB")

        # deviation is less than 1/2 of 1% of 1024
        size = Range(16384 + (eps - 1))
        self.assertEqual(str(size), "> 16 KiB")

        # deviation is greater than 1/2 of 1% of 1024
        size = Range(16384 + (eps + 1))
        self.assertEqual(str(size), "< 16.01 KiB")


class ComputationTestCase(unittest.TestCase):
    """ Test setting configuration for computation. """

    def setUp(self):
        """ Get current config. """
        self.strict = Config.STRICT

    def tearDown(self):
        """ Reset configuration to default. """
        Config.STRICT = self.strict

    def test_fractional_bytes(self):
        """
        Test that error is raised on fractional bytes when EXACT is True.
        """
        Config.STRICT = True
        with self.assertRaises(RangeFractionalResultError):
            Range(Fraction(1, 2))
