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
import copy
import unittest
from decimal import Decimal
from fractions import Fraction

# isort: THIRDPARTY
from hypothesis import given, settings

# isort: LOCAL
from justbytes import Range

from tests.test_hypothesis.test_size.utils import NUMBERS_STRATEGY  # isort:skip
from tests.test_hypothesis.test_size.utils import SIZE_STRATEGY  # isort:skip


class AdditionTestCase(unittest.TestCase):
    """ Test addition. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def testAddition(self, s1, s2):
        """ Test addition. """
        self.assertEqual(s1 + s2, Range(s1.magnitude + s2.magnitude))


class DivmodTestCase(unittest.TestCase):
    """ Test divmod. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Range(0)))
    @settings(max_examples=10)
    def testDivmodWithRange(self, s1, s2):
        """ Test divmod with a size. """
        (div, rem) = divmod(s1.magnitude, s2.magnitude)
        self.assertEqual(divmod(s1, s2), (div, Range(rem)))

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def testDivmodWithNumber(self, s1, s2):
        """ Test divmod with a number. """
        (div, rem) = divmod(s1.magnitude, Fraction(s2))
        self.assertEqual(divmod(s1, s2), (Range(div), Range(rem)))


class FloordivTestCase(unittest.TestCase):
    """ Test floordiv. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Range(0)))
    @settings(max_examples=10)
    def testFloordivWithRange(self, s1, s2):
        """ Test floordiv with a size. """
        self.assertEqual(s1 // s2, s1.magnitude // s2.magnitude)

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def testFloordivWithNumber(self, s1, s2):
        """ Test floordiv with a number. """
        self.assertEqual(s1 // s2, Range(s1.magnitude // Fraction(s2)))


class ModTestCase(unittest.TestCase):
    """ Test mod. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Range(0)))
    @settings(max_examples=10)
    def testModWithRange(self, s1, s2):
        """ Test mod with a size. """
        self.assertEqual(s1 % s2, Range(s1.magnitude % s2.magnitude))

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def testModWithNumber(self, s1, s2):
        """ Test mod with a number. """
        self.assertEqual(s1 % s2, Range(s1.magnitude % Fraction(s2)))


class MultiplicationTestCase(unittest.TestCase):
    """ Test multiplication. """

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY)
    @settings(max_examples=10)
    def testMultiplication(self, s, n):
        """ Test multiplication. """
        self.assertEqual(s * n, Range(Fraction(n) * s.magnitude))


class RdivmodTestCase(unittest.TestCase):
    """ Test rdivmod. """

    @given(SIZE_STRATEGY.filter(lambda x: x != Range(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def testRdivmodWithRange(self, s1, s2):
        """ Test divmod with a size. """
        (div, rem) = divmod(s2.magnitude, s1.magnitude)
        self.assertEqual(s1.__rdivmod__(s2), (div, Range(rem)))


class RfloordivTestCase(unittest.TestCase):
    """ Test rfloordiv. """

    @given(SIZE_STRATEGY.filter(lambda x: x != Range(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def testRfloordivWithRange(self, s1, s2):
        """ Test floordiv with a size. """
        self.assertEqual(s1.__rfloordiv__(s2), s2.magnitude // s1.magnitude)


class RmodTestCase(unittest.TestCase):
    """ Test rmod. """

    @given(SIZE_STRATEGY.filter(lambda x: x != Range(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def testRmodWithRange(self, s1, s2):
        """ Test rmod with a size. """
        self.assertEqual(s1.__rmod__(s2), Range(s2.magnitude % s1.magnitude))


class RsubTestCase(unittest.TestCase):
    """ Test rsub. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def testRsub(self, s1, s2):
        """ Test __rsub__. """
        self.assertEqual(s1.__rsub__(s2), Range(s2.magnitude - s1.magnitude))


class RtruedivTestCase(unittest.TestCase):
    """ Test rtruediv. """

    @given(SIZE_STRATEGY.filter(lambda x: x != Range(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def testTruedivWithRange(self, s1, s2):
        """ Test truediv with a size. """
        self.assertEqual(s1.__rtruediv__(s2), s2.magnitude / s1.magnitude)


class SubtractionTestCase(unittest.TestCase):
    """ Test subtraction. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def testSubtraction(self, s1, s2):
        """ Test subtraction. """
        self.assertEqual(s1 - s2, Range(s1.magnitude - s2.magnitude))


class TruedivTestCase(unittest.TestCase):
    """ Test truediv. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Range(0)))
    @settings(max_examples=10)
    def testTruedivWithRange(self, s1, s2):
        """ Test truediv with a size. """
        self.assertEqual(s1 / s2, s1.magnitude / s2.magnitude)

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    def testTruedivWithNumber(self, s1, s2):
        """ Test truediv with a number. """
        self.assertEqual(s1 / s2, Range(s1.magnitude / Fraction(s2)))


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
        self.assertEqual(abs(s), Range(abs(s.magnitude)))

    @given(SIZE_STRATEGY)
    @settings(max_examples=5)
    def testNeg(self, s):
        """ Test negation. """
        self.assertEqual(-s, Range(-s.magnitude))

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
        NUMBERS_STRATEGY.filter(lambda n: not isinstance(n, Decimal)),
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
