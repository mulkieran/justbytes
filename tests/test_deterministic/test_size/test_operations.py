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

""" Tests for operations on Range objects. """

# isort: STDLIB
import unittest
from decimal import Decimal

# isort: LOCAL
from justbytes import B, GiB, MiB, Range, TiB
from justbytes._errors import (
    RangeNonsensicalBinOpError,
    RangeNonsensicalBinOpValueError,
    RangePowerResultError,
)


class UtilityMethodsTestCase(unittest.TestCase):
    """ Test operator methods and other methods with an '_'. """

    def testBinaryOperatorsRange(self):
        """ Test binary operators with a possible Range result. """
        s = Range(2, GiB)

        # **
        with self.assertRaises(RangeNonsensicalBinOpError):
            # pylint: disable=expression-not-assigned, pointless-statement
            s ** Range(2)
        with self.assertRaises(RangePowerResultError):
            s ** 2  # pylint: disable=pointless-statement
        with self.assertRaises(RangeNonsensicalBinOpError):
            # pylint: disable=expression-not-assigned, pointless-statement
            2 ** Range(0)

    def testBinaryOperatorsBoolean(self):
        """ Test binary operators with a boolean result. """

        # <
        self.assertTrue(Range(0, MiB) < Range(32))
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(0) < 1  # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            # pylint: disable=misplaced-comparison-constant
            1 < Range(32, TiB)  # pylint: disable=expression-not-assigned

        # <=
        self.assertTrue(Range(0, MiB) <= Range(32))
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(0) <= 1  # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            # pylint: disable=misplaced-comparison-constant
            1 <= Range(32, TiB)  # pylint: disable=expression-not-assigned

        # >
        self.assertTrue(Range(32, MiB) > Range(32))
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(32) > 1  # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            # pylint: disable=misplaced-comparison-constant
            1 > Range(0, TiB)  # pylint: disable=expression-not-assigned

        # >=
        self.assertTrue(Range(32, MiB) >= Range(32))
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(32) >= 1  # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            # pylint: disable=misplaced-comparison-constant
            1 >= Range(0, TiB)  # pylint: disable=expression-not-assigned

        # !=
        self.assertTrue(Range(32, MiB) != Range(32, GiB))

        # boolean properties
        self.assertEqual(Range(0) and True, Range(0))
        self.assertEqual(True and Range(0), Range(0))
        self.assertEqual(Range(1) or True, Range(1))
        self.assertEqual(False or Range(5, MiB), Range(5, MiB))

    def testUnaryOperators(self):
        """ Test unary operators. """
        s = Range(2, GiB)

        # unary +/-
        self.assertEqual(-(Range(32)), Range(-32))
        self.assertEqual(+(Range(32)), Range(32))
        self.assertEqual(+(Range(-32)), Range(-32))

        # abs
        self.assertEqual(abs(s), s)
        self.assertEqual(abs(Range(-32, TiB)), Range(32, TiB))


class AdditionTestCase(unittest.TestCase):
    """ Test addition. """

    def testExceptions(self):
        """ Any non-size other raises an exception. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            2 + Range(0)
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(0) + 2


class DivmodTestCase(unittest.TestCase):
    """ Test divmod. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            divmod(2048, Range(12, B))
        with self.assertRaises(RangeNonsensicalBinOpError):
            divmod(Range(12), "str")
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            divmod(Range(12), Range(0))
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            divmod(Range(12), 0)
        with self.assertRaises(RangeNonsensicalBinOpError):
            divmod(Range(12), Decimal("NaN"))


class FloordivTestCase(unittest.TestCase):
    """ Test floordiv. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            2048 // Range(12, B)
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12) // "str"
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(12) // Range(0)
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(12) // 0
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12) // Decimal("NaN")


class ModTestCase(unittest.TestCase):
    """ Test mod. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            2048 % Range(12, B)
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12) % "str"
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(12) % Range(0)
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(12) % 0
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12) % Decimal("NaN")


class MultiplicationTestCase(unittest.TestCase):
    """ Test multiplication. """

    def testExceptions(self):
        """ Range others are unrepresentable. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangePowerResultError):
            Range(0) * Range(0)
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(0) * Decimal("NaN")
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(0) * "str"


class RdivmodTestCase(unittest.TestCase):
    """ Test rdivmod. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12).__rdivmod__(str)
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(0).__rdivmod__(Range(12))
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12).__rdivmod__(32)


class RfloordivTestCase(unittest.TestCase):
    """ Test rfloordiv. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12, B).__rfloordiv__(1024)
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(0).__rfloordiv__(Range(12))
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12).__rfloordiv__(Decimal("NaN"))


class RmodTestCase(unittest.TestCase):
    """ Test rmod. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12, B).__rmod__(1024)
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12).__rmod__("str")
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(0).__rmod__(Range(12))
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12).__rmod__(Decimal("NaN"))


class RsubTestCase(unittest.TestCase):
    """ Test rsub. """

    def testExceptions(self):
        """ Any non-size other raises an exception. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(0).__rsub__(2)


class RtruedivTestCase(unittest.TestCase):
    """ Test rtruediv. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12, B).__rtruediv__(1024)
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12).__rtruediv__("str")
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(0).__rtruediv__(Range(12))
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12).__rtruediv__(Decimal("NaN"))


class SubtractionTestCase(unittest.TestCase):
    """ Test subtraction. """

    def testExceptions(self):
        """ Any non-size other raises an exception. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            2 - Range(0)
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(0) - 2


class TruedivTestCase(unittest.TestCase):
    """ Test truediv. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(RangeNonsensicalBinOpError):
            2048 / Range(12, B)
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12) / "str"
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(12) / Range(0)
        with self.assertRaises(RangeNonsensicalBinOpValueError):
            Range(12) / 0
        with self.assertRaises(RangeNonsensicalBinOpError):
            Range(12) / Decimal("NaN")
