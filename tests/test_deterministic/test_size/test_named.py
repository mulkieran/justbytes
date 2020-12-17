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

""" Tests for named methods of Range objects. """

# isort: STDLIB
import unittest

# isort: LOCAL
from justbytes import ROUND_HALF_UP, B, Config, Range, StringConfig, ValueConfig
from justbytes._errors import RangeValueError


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


class DigitsConfigTestCase(unittest.TestCase):
    """
    Test digits config.
    """

    def testExceptions(self):
        """
        Test exceptions.
        """
        with self.assertRaises(RangeValueError):
            Range(0).getString(
                StringConfig(
                    ValueConfig(base=100),
                    Config.STRING_CONFIG.DISPLAY_CONFIG,
                    Config.STRING_CONFIG.DISPLAY_IMPL_CLASS,
                )
            )


class RoundingTestCase(unittest.TestCase):
    """ Test rounding methods. """

    def testExceptions(self):
        """ Test raising exceptions when rounding. """
        with self.assertRaises(RangeValueError):
            Range(0).roundTo(Range(-1, B), rounding=ROUND_HALF_UP)
        with self.assertRaises(RangeValueError):
            Range(512).roundTo(1.4, rounding=ROUND_HALF_UP)
        with self.assertRaises(RangeValueError):
            s = Range(512)
            s.roundTo(512, rounding=ROUND_HALF_UP, bounds=(Range(0), Range(-1)))
