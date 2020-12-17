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

    def testZero(self):
        """ Test construction with 0 as decimal. """
        zero = Range(0)
        self.assertEqual(zero, Range("0.0"))

    def testNegative(self):
        """ Test construction of negative sizes. """
        s = Range(-500, MiB)
        self.assertEqual(s.components(), (Fraction(-500, 1), MiB))
        self.assertEqual(s.convertTo(B), -524288000)

    def testConstructor(self):
        """ Test error checking in constructo. """
        with self.assertRaises(RangeValueError):
            Range("1.1.1", KiB)
        self.assertEqual(Range(Range(0)), Range(0))
        with self.assertRaises(RangeValueError):
            Range(Range(0), KiB)
        with self.assertRaises(RangeValueError):
            Range(B)

    def testNoUnitsInString(self):
        """ Test construction w/ no units specified. """
        self.assertEqual(Range("1024"), Range(1, KiB))

    def testFraction(self):
        """ Test creating Range with Fraction. """
        self.assertEqual(Range(Fraction(1024, 2), KiB), Range(Fraction(1, 2), MiB))


class DisplayTestCase(unittest.TestCase):
    """ Test formatting Range for display. """

    def testStr(self):
        """ Test construction of display components. """
        s = Range("12.68", TiB)
        self.assertEqual(str(s), "12.68 TiB")

        s = Range("26.55", MiB)
        self.assertEqual(str(s), "26.55 MiB")

        s = Range("12.687", TiB)
        self.assertEqual(str(s), "< 12.69 TiB")

    def testMinValue(self):
        """ Test behavior on min_value parameter. """
        s = Range(9, MiB)
        self.assertEqual(s.components(), (Fraction(9, 1), MiB))
        self.assertEqual(
            s.components(ValueConfig(min_value=10)), (Fraction(9216, 1), KiB)
        )

        s = Range("0.5", GiB)
        self.assertEqual(
            s.components(ValueConfig(min_value=1)), (Fraction(512, 1), MiB)
        )
        self.assertEqual(
            s.components(ValueConfig(min_value=Fraction(1, 10))), (Fraction(1, 2), GiB)
        )
        self.assertEqual(
            s.components(ValueConfig(min_value=1)), (Fraction(512, 1), MiB)
        )

        # when min_value is 10 and single digit on left of decimal, display
        # with smaller unit.
        s = Range("7.18", KiB)
        self.assertEqual(s.components(ValueConfig(min_value=10))[1], B)
        s = Range("9.68", TiB)
        self.assertEqual(s.components(ValueConfig(min_value=10))[1], GiB)
        s = Range("4.29", MiB)
        self.assertEqual(s.components(ValueConfig(min_value=10))[1], KiB)

        # when min value is 100 and two digits on left of decimal
        s = Range("14", MiB)
        self.assertEqual(
            s.components(ValueConfig(min_value=100)), (Fraction(14 * 1024, 1), KiB)
        )

    def testExceptionValues(self):
        """ Test that exceptions are properly raised on bad params. """
        s = Range(500)
        with self.assertRaises(RangeValueError):
            s.components(ValueConfig(min_value=-1))

    def testRoundingToBytes(self):
        """ Test that second part is B when rounding to bytes. """
        s = Range(500)
        self.assertEqual(s.components()[1], B)

    def testSIUnits(self):
        """ Test binary_units param. """
        s = Range(1000)
        self.assertEqual(s.components(ValueConfig(binary_units=False)), (1, KB))


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

    def testValueConfigs(self):
        """ Test str with various configuration options. """
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))

        # exactly 4 Pi
        s = Range(0x10000000000000)
        self.assertEqual(str(s), "4 PiB")

        s = Range(300, MiB)
        self.assertEqual(str(s), "300 MiB")

        s = Range("12.6998", TiB)
        self.assertEqual(str(s), "< 12.7 TiB")

        # byte values close to multiples of 2 are shown without trailing zeros
        s = Range(0xFF)
        self.assertEqual(str(s), "255 B")

        # a fractional quantity is shown if the value deviates
        # from the whole number of units by more than 1%
        s = Range(16384 - (Fraction(1024) / 100 + 1))
        self.assertEqual(str(s), "< 15.99 KiB")

        # test a very large quantity with no associated abbreviation or prefix
        s = Range(1024 ** 9)
        self.assertEqual(str(s), "1024 YiB")
        s = Range(1024 ** 9 - 1)
        self.assertEqual(str(s), "< 1024 YiB")
        s = Range(1024 ** 10)
        self.assertEqual(str(s), "1048576 YiB")

        s = Range(0xFFFFFFFFFFFFF)
        self.assertEqual(str(s), "< 4 PiB")

        s = Range(0xFFFF)
        # value is not exactly 64 KiB, but w/ 2 places, value is 64.00 KiB
        # so the trailing 0s are stripped.
        self.assertEqual(str(s), "< 64 KiB")

        Config.set_value_config(ValueConfig(max_places=3))
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))
        s = Range("23.7874", TiB)
        self.assertEqual(str(s), "> 23.787 TiB")

        Config.set_value_config(ValueConfig(min_value=10))
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))
        s = Range(8193)
        self.assertEqual(str(s), ("8193 B"))

        # if max_places is set to None, all digits are displayed
        Config.set_value_config(ValueConfig(max_places=None))
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))
        s = Range(0xFFFFFFFFFFFFF)
        self.assertEqual(
            str(s), "3.99999999999999911182158029987476766109466552734375 PiB"
        )
        s = Range(0x10000)
        self.assertEqual(str(s), ("64 KiB"))
        s = Range(0x10001)
        self.assertEqual(str(s), "64.0009765625 KiB")

        Config.set_value_config(ValueConfig(max_places=2))
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=False)))
        s = Range(1024 ** 9 + 1)
        self.assertEqual(str(s), "> 1024.00 YiB")

        s = Range(0xFFFFF)
        self.assertEqual(str(s), "< 1024.00 KiB")

    def testStrWithSmallDeviations(self):
        """ Behavior when deviation from whole value is small. """
        Config.set_display_config(DisplayConfig(strip_config=StripConfig(strip=True)))

        eps = 1024 * Fraction(1, 100) * Fraction(1, 2)

        # deviation is less than 1/2 of 1% of 1024
        s = Range(16384 - (eps - 1))
        self.assertEqual(str(s), "< 16 KiB")

        # deviation is greater than 1/2 of 1% of 1024
        s = Range(16384 - (eps + 1))
        self.assertEqual(str(s), "> 15.99 KiB")

        # deviation is less than 1/2 of 1% of 1024
        s = Range(16384 + (eps - 1))
        self.assertEqual(str(s), "> 16 KiB")

        # deviation is greater than 1/2 of 1% of 1024
        s = Range(16384 + (eps + 1))
        self.assertEqual(str(s), "< 16.01 KiB")


class ComputationTestCase(unittest.TestCase):
    """ Test setting configuration for computation. """

    def setUp(self):
        """ Get current config. """
        self.strict = Config.STRICT

    def tearDown(self):
        """ Reset configuration to default. """
        Config.STRICT = self.strict

    def testFractionalBytes(self):
        """
        Test that error is raised on fractional bytes when EXACT is True.
        """
        Config.STRICT = True
        with self.assertRaises(RangeFractionalResultError):
            Range(Fraction(1, 2))
