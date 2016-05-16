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

""" Tests for behavior of Range objects. """

import unittest

from decimal import Decimal
from fractions import Fraction

from justbytes import Range
from justbytes import B
from justbytes import KiB
from justbytes import MiB
from justbytes import GiB
from justbytes import TiB
from justbytes import KB
from justbytes import DisplayConfig
from justbytes import ValueConfig
from justbytes import StripConfig

from justbytes._config import Config

from justbytes._errors import RangeFractionalResultError
from justbytes._errors import RangeValueError


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
        self.assertEqual(
           Range(Fraction(1024, 2), KiB),
           Range(Fraction(1, 2), MiB)
        )

class DisplayTestCase(unittest.TestCase):
    """ Test formatting Range for display. """

    def testStr(self):
        """ Test construction of display components. """
        s = Range("12.68", TiB)
        self.assertEqual(str(s), "12.68 TiB")

        s = Range("26.55", MiB)
        self.assertEqual(str(s), "26.55 MiB")

        s = Range('12.687', TiB)
        self.assertEqual(str(s), "< 12.69 TiB")

    def testMinValue(self):
        """ Test behavior on min_value parameter. """
        s = Range(9, MiB)
        self.assertEqual(s.components(), (Fraction(9, 1), MiB))
        self.assertEqual(
           s.components(ValueConfig(min_value=10)),
           (Fraction(9216, 1), KiB)
        )

        s = Range("0.5", GiB)
        self.assertEqual(
           s.components(ValueConfig(min_value=1)),
           (Fraction(512, 1), MiB)
        )
        self.assertEqual(
           s.components(ValueConfig(min_value=Decimal("0.1"))),
           (Fraction(1, 2), GiB)
        )
        self.assertEqual(
           s.components(ValueConfig(min_value=Decimal(1))),
           (Fraction(512, 1), MiB)
        )

        # when min_value is 10 and single digit on left of decimal, display
        # with smaller unit.
        s = Range('7.18', KiB)
        self.assertEqual(s.components(ValueConfig(min_value=10))[1], B)
        s = Range('9.68', TiB)
        self.assertEqual(s.components(ValueConfig(min_value=10))[1], GiB)
        s = Range('4.29', MiB)
        self.assertEqual(s.components(ValueConfig(min_value=10))[1], KiB)

        # when min value is 100 and two digits on left of decimal
        s = Range('14', MiB)
        self.assertEqual(
           s.components(ValueConfig(min_value=100)),
           (Fraction(14 * 1024, 1), KiB)
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
        Config.set_display_config(
           DisplayConfig(
              strip_config=StripConfig(strip=True)
           )
        )

        # exactly 4 Pi
        s = Range(0x10000000000000)
        self.assertEqual(str(s), "4 PiB")

        s = Range(300, MiB)
        self.assertEqual(str(s), "300 MiB")

        s = Range('12.6998', TiB)
        self.assertEqual(str(s), "< 12.7 TiB")

        # byte values close to multiples of 2 are shown without trailing zeros
        s = Range(0xff)
        self.assertEqual(str(s), "255 B")

        # a fractional quantity is shown if the value deviates
        # from the whole number of units by more than 1%
        s = Range(16384 - (Decimal(1024)/100 + 1))
        self.assertEqual(str(s), "< 15.99 KiB")

        # test a very large quantity with no associated abbreviation or prefix
        s = Range(1024**9)
        self.assertEqual(str(s), "1024 YiB")
        s = Range(1024**9 - 1)
        self.assertEqual(str(s), "< 1024 YiB")
        s = Range(1024**10)
        self.assertEqual(str(s), "1048576 YiB")

        s = Range(0xfffffffffffff)
        self.assertEqual(str(s), "< 4 PiB")

        s = Range(0xffff)
        # value is not exactly 64 KiB, but w/ 2 places, value is 64.00 KiB
        # so the trailing 0s are stripped.
        self.assertEqual(str(s), "< 64 KiB")

        Config.set_value_config(ValueConfig(max_places=3))
        Config.set_display_config(
           DisplayConfig(
              strip_config=StripConfig(strip=True)
           )
        )
        s = Range('23.7874', TiB)
        self.assertEqual(str(s), "> 23.787 TiB")

        Config.set_value_config(ValueConfig(min_value=10))
        Config.set_display_config(
           DisplayConfig(
              strip_config=StripConfig(strip=True)
           )
        )
        s = Range(8193)
        self.assertEqual(str(s), ("8193 B"))

        # if max_places is set to None, all digits are displayed
        Config.set_value_config(ValueConfig(max_places=None))
        Config.set_display_config(
           DisplayConfig(
              strip_config=StripConfig(strip=True)
           )
        )
        s = Range(0xfffffffffffff)
        self.assertEqual(
           str(s),
           "3.99999999999999911182158029987476766109466552734375 PiB"
        )
        s = Range(0x10000)
        self.assertEqual(str(s), ("64 KiB"))
        s = Range(0x10001)
        self.assertEqual(str(s), "64.0009765625 KiB")

        Config.set_value_config(ValueConfig(max_places=2))
        Config.set_display_config(
           DisplayConfig(
              strip_config=StripConfig(strip=False)
           )
        )
        s = Range(1024**9 + 1)
        self.assertEqual(str(s), "> 1024.00 YiB")

        s = Range(0xfffff)
        self.assertEqual(str(s), "< 1024.00 KiB")

    def testStrWithSmallDeviations(self):
        """ Behavior when deviation from whole value is small. """
        Config.set_display_config(
           DisplayConfig(
              strip_config=StripConfig(strip=True)
           )
        )

        eps = Decimal(1024)/100/2 # 1/2 of 1% of 1024

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
