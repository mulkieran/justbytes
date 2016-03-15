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

""" Tests for operations on Size objects. """

import copy
from decimal import Decimal
from fractions import Fraction

import unittest

from hypothesis import given
from hypothesis import settings

from justbytes import Size
from justbytes import B
from justbytes import MiB
from justbytes import GiB
from justbytes import TiB

from justbytes._errors import SizeNonsensicalBinOpError
from justbytes._errors import SizeNonsensicalBinOpValueError
from justbytes._errors import SizePowerResultError

from tests.utils import NUMBERS_STRATEGY
from tests.utils import SIZE_STRATEGY

class UtilityMethodsTestCase(unittest.TestCase):
    """ Test operator methods and other methods with an '_'. """

    def testBinaryOperatorsSize(self):
        """ Test binary operators with a possible Size result. """
        s = Size(2, GiB)

        # **
        with self.assertRaises(SizeNonsensicalBinOpError):
            s ** Size(2) # pylint: disable=expression-not-assigned, pointless-statement
        with self.assertRaises(SizePowerResultError):
            s ** 2 # pylint: disable=pointless-statement
        with self.assertRaises(SizeNonsensicalBinOpError):
            2 ** Size(0) # pylint: disable=expression-not-assigned, pointless-statement

    def testBinaryOperatorsBoolean(self):
        """ Test binary operators with a boolean result. """

        # <
        self.assertTrue(Size(0, MiB) < Size(32))
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(0) < 1 # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            # pylint: disable=misplaced-comparison-constant
            1 < Size(32, TiB) # pylint: disable=expression-not-assigned

        # <=
        self.assertTrue(Size(0, MiB) <= Size(32))
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(0) <= 1 # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            # pylint: disable=misplaced-comparison-constant
            1 <= Size(32, TiB) # pylint: disable=expression-not-assigned

        # >
        self.assertTrue(Size(32, MiB) > Size(32))
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(32) > 1 # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            # pylint: disable=misplaced-comparison-constant
            1 > Size(0, TiB) # pylint: disable=expression-not-assigned

        # >=
        self.assertTrue(Size(32, MiB) >= Size(32))
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(32) >= 1 # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            # pylint: disable=misplaced-comparison-constant
            1 >= Size(0, TiB) # pylint: disable=expression-not-assigned

        # !=
        self.assertTrue(Size(32, MiB) != Size(32, GiB))

        # boolean properties
        self.assertEqual(Size(0) and True, Size(0))
        self.assertEqual(True and Size(0), Size(0))
        self.assertEqual(Size(1) or True, Size(1))
        self.assertEqual(False or Size(5, MiB), Size(5, MiB))

    def testUnaryOperators(self):
        """ Test unary operators. """
        s = Size(2, GiB)

        # unary +/-
        self.assertEqual(-(Size(32)), Size(-32))
        self.assertEqual(+(Size(32)), Size(32))
        self.assertEqual(+(Size(-32)), Size(-32))

        # abs
        self.assertEqual(abs(s), s)
        self.assertEqual(abs(Size(-32, TiB)), Size(32, TiB))

    def testOtherMethods(self):
        """ Test miscellaneous non-operator methods. """


        self.assertEqual(repr(Size(0)), "Size(0)")
        self.assertEqual(repr(Size(1024)), "Size(1024)")
        self.assertEqual(repr(Size("1024.1")), ">Size(1024)")


class AdditionTestCase(unittest.TestCase):
    """ Test addition. """

    def testExceptions(self):
        """ Any non-size other raises an exception. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            2 + Size(0)
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(0) + 2

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def testAddition(self, s1, s2):
        """ Test addition. """
        self.assertEqual(s1 + s2, Size(s1.magnitude + s2.magnitude))


class DivmodTestCase(unittest.TestCase):
    """ Test divmod. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            divmod(2048, Size(12, B))
        with self.assertRaises(SizeNonsensicalBinOpError):
            divmod(Size(12), "str")
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            divmod(Size(12), Size(0))
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            divmod(Size(12), 0)
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            divmod(Size(12), Decimal('NaN'))

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Size(0)))
    @settings(max_examples=10)
    def testDivmodWithSize(self, s1, s2):
        """ Test divmod with a size. """
        (div, rem) = divmod(s1.magnitude, s2.magnitude)
        self.assertEqual(divmod(s1, s2), (div, Size(rem)))

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def testDivmodWithNumber(self, s1, s2):
        """ Test divmod with a number. """
        (div, rem) = divmod(s1.magnitude, Fraction(s2))
        self.assertEqual(divmod(s1, s2), (Size(div), Size(rem)))


class FloordivTestCase(unittest.TestCase):
    """ Test floordiv. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            2048 // Size(12, B)
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12) // "str"
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) // Size(0)
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) // 0
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) // Decimal('NaN')

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Size(0)))
    @settings(max_examples=10)
    def testFloordivWithSize(self, s1, s2):
        """ Test floordiv with a size. """
        self.assertEqual(s1 // s2, s1.magnitude // s2.magnitude)

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def testFloordivWithNumber(self, s1, s2):
        """ Test floordiv with a number. """
        self.assertEqual(s1 // s2, Size(s1.magnitude // Fraction(s2)))


class ModTestCase(unittest.TestCase):
    """ Test mod. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            2048 % Size(12, B)
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12) % "str"
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) % Size(0)
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) % 0
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) % Decimal('NaN')

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Size(0)))
    @settings(max_examples=10)
    def testModWithSize(self, s1, s2):
        """ Test mod with a size. """
        self.assertEqual(s1 % s2, Size(s1.magnitude % s2.magnitude))

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def testModWithNumber(self, s1, s2):
        """ Test mod with a number. """
        self.assertEqual(s1 % s2, Size(s1.magnitude % Fraction(s2)))


class MultiplicationTestCase(unittest.TestCase):
    """ Test multiplication. """

    def testExceptions(self):
        """ Size others are unrepresentable. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizePowerResultError):
            Size(0) * Size(0)
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(0) * Decimal("NaN")
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(0) * 'str'

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY)
    @settings(max_examples=10)
    def testMultiplication(self, s, n):
        """ Test multiplication. """
        self.assertEqual(s * n, Size(Fraction(n) * s.magnitude))


class RdivmodTestCase(unittest.TestCase):
    """ Test rdivmod. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12).__rdivmod__(str)
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(0).__rdivmod__(Size(12))
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12).__rdivmod__(32)

    @given(SIZE_STRATEGY.filter(lambda x: x != Size(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def testRdivmodWithSize(self, s1, s2):
        """ Test divmod with a size. """
        (div, rem) = divmod(s2.magnitude, s1.magnitude)
        self.assertEqual(s1.__rdivmod__(s2), (div, Size(rem)))


class RfloordivTestCase(unittest.TestCase):
    """ Test rfloordiv. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12, B).__rfloordiv__(1024)
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(0).__rfloordiv__(Size(12))
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12).__rfloordiv__(Decimal('NaN'))

    @given(SIZE_STRATEGY.filter(lambda x: x != Size(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def testRfloordivWithSize(self, s1, s2):
        """ Test floordiv with a size. """
        self.assertEqual(s1.__rfloordiv__(s2), s2.magnitude // s1.magnitude)


class RmodTestCase(unittest.TestCase):
    """ Test rmod. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12, B).__rmod__(1024)
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12).__rmod__("str")
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(0).__rmod__(Size(12))
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12).__rmod__(Decimal('NaN'))

    @given(SIZE_STRATEGY.filter(lambda x: x != Size(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def testRmodWithSize(self, s1, s2):
        """ Test rmod with a size. """
        self.assertEqual(s1.__rmod__(s2), Size(s2.magnitude % s1.magnitude))


class RsubTestCase(unittest.TestCase):
    """ Test rsub. """

    def testExceptions(self):
        """ Any non-size other raises an exception. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(0).__rsub__(2)

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def testRsub(self, s1, s2):
        """ Test __rsub__. """
        self.assertEqual(s1.__rsub__(s2), Size(s2.magnitude - s1.magnitude))


class RtruedivTestCase(unittest.TestCase):
    """ Test rtruediv. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12, B).__rtruediv__(1024)
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12).__rtruediv__("str")
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(0).__rtruediv__(Size(12))
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12).__rtruediv__(Decimal('NaN'))

    @given(SIZE_STRATEGY.filter(lambda x: x != Size(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def testTruedivWithSize(self, s1, s2):
        """ Test truediv with a size. """
        self.assertEqual(s1.__rtruediv__(s2), s2.magnitude / s1.magnitude)


class SubtractionTestCase(unittest.TestCase):
    """ Test subtraction. """

    def testExceptions(self):
        """ Any non-size other raises an exception. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            2 - Size(0)
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(0) - 2

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def testSubtraction(self, s1, s2):
        """ Test subtraction. """
        self.assertEqual(s1 - s2, Size(s1.magnitude - s2.magnitude))


class TruedivTestCase(unittest.TestCase):
    """ Test truediv. """

    def testExceptions(self):
        """ Test that exceptions are thrown. """
        # pylint: disable=expression-not-assigned
        with self.assertRaises(SizeNonsensicalBinOpError):
            2048 / Size(12, B)
        with self.assertRaises(SizeNonsensicalBinOpError):
            Size(12) / "str"
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) / Size(0)
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) / 0
        with self.assertRaises(SizeNonsensicalBinOpValueError):
            Size(12) / Decimal('NaN')

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Size(0)))
    @settings(max_examples=10)
    def testTruedivWithSize(self, s1, s2):
        """ Test truediv with a size. """
        self.assertEqual(s1 / s2, s1.magnitude / s2.magnitude)

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    def testTruedivWithNumber(self, s1, s2):
        """ Test truediv with a number. """
        self.assertEqual(s1 / s2, Size(s1.magnitude / Fraction(s2)))


class UnaryOperatorsTestCase(unittest.TestCase):
    """ Test unary operators. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=5)
    def testHash(self, s1, s2):
        """ Test that hash has the necessary property for hash table lookup. """
        s3 = copy.deepcopy(s1)
        self.assertTrue(hash(s1) == hash(s3))
        self.assertTrue(s1 != s2 or hash(s1) == hash(s2))

    @given(SIZE_STRATEGY)
    @settings(max_examples=5)
    def testAbs(self, s):
        """ Test absolute value. """
        self.assertEqual(abs(s), Size(abs(s.magnitude)))

    @given(SIZE_STRATEGY)
    @settings(max_examples=5)
    def testNeg(self, s):
        """ Test negation. """
        self.assertEqual(-s, Size(-s.magnitude))

    @given(SIZE_STRATEGY)
    @settings(max_examples=5)
    def testPos(self, s):
        """ Test positive. """
        self.assertEqual(+s, s)


class ArithmeticPropertiesTestCase(unittest.TestCase):
    """
    Verify that distributive property holds.
    """

    @given(
       SIZE_STRATEGY,
       NUMBERS_STRATEGY.filter(lambda n: not isinstance(n, Decimal)),
       NUMBERS_STRATEGY.filter(lambda n: not isinstance(n, Decimal))
    )
    @settings(max_examples=10)
    def testDistributivity1(self, s, n, m):
        """
        Assert distributivity across numbers.
        """
        self.assertEqual((n + m) * s, n * s + m * s)

    @given(SIZE_STRATEGY, SIZE_STRATEGY, NUMBERS_STRATEGY)
    @settings(max_examples=10)
    def testDistributivity2(self, p, q, n):
        """
        Assert distributivity across sizes.
        """
        self.assertEqual((p + q) * n, p * n + q * n)

    @given(SIZE_STRATEGY, SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def testAssociativity(self, p, q, r):
        """
        Assert associativity across sizes.
        """
        self.assertEqual((p + q) + r, p + (r + q))
