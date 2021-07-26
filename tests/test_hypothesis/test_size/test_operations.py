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
    def test_addition(self, size_1, size_2):
        """ Test addition. """
        self.assertEqual(size_1 + size_2, Range(size_1.magnitude + size_2.magnitude))


class DivmodTestCase(unittest.TestCase):
    """ Test divmod. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Range(0)))
    @settings(max_examples=10)
    def test_divmod_with_range(self, size_1, size_2):
        """ Test divmod with a size. """
        (div, rem) = divmod(size_1.magnitude, size_2.magnitude)
        self.assertEqual(divmod(size_1, size_2), (div, Range(rem)))

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def test_divmod_with_number(self, size_1, size_2):
        """ Test divmod with a number. """
        (div, rem) = divmod(size_1.magnitude, Fraction(size_2))
        self.assertEqual(divmod(size_1, size_2), (Range(div), Range(rem)))


class FloordivTestCase(unittest.TestCase):
    """ Test floordiv. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Range(0)))
    @settings(max_examples=10)
    def test_floordiv_with_range(self, size_1, size_2):
        """ Test floordiv with a size. """
        self.assertEqual(size_1 // size_2, size_1.magnitude // size_2.magnitude)

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def test_floordiv_with_number(self, size_1, size_2):
        """ Test floordiv with a number. """
        self.assertEqual(size_1 // size_2, Range(size_1.magnitude // Fraction(size_2)))


class ModTestCase(unittest.TestCase):
    """ Test mod. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Range(0)))
    @settings(max_examples=10)
    def test_mod_with_range(self, size_1, size_2):
        """ Test mod with a size. """
        self.assertEqual(size_1 % size_2, Range(size_1.magnitude % size_2.magnitude))

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    @settings(max_examples=10)
    def test_mod_with_number(self, size_1, size_2):
        """ Test mod with a number. """
        self.assertEqual(size_1 % size_2, Range(size_1.magnitude % Fraction(size_2)))


class MultiplicationTestCase(unittest.TestCase):
    """ Test multiplication. """

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY)
    @settings(max_examples=10)
    def test_multiplication(self, size, num):
        """ Test multiplication. """
        self.assertEqual(size * num, Range(Fraction(num) * size.magnitude))


class RdivmodTestCase(unittest.TestCase):
    """ Test rdivmod. """

    @given(SIZE_STRATEGY.filter(lambda x: x != Range(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def test_rdivmod_with_range(self, size_1, size_2):
        """ Test divmod with a size. """
        (div, rem) = divmod(size_2.magnitude, size_1.magnitude)
        self.assertEqual(size_1.__rdivmod__(size_2), (div, Range(rem)))


class RfloordivTestCase(unittest.TestCase):
    """ Test rfloordiv. """

    @given(SIZE_STRATEGY.filter(lambda x: x != Range(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def test_ffloordiv_with_range(self, size_1, size_2):
        """ Test floordiv with a size. """
        self.assertEqual(
            size_1.__rfloordiv__(size_2), size_2.magnitude // size_1.magnitude
        )


class RmodTestCase(unittest.TestCase):
    """ Test rmod. """

    @given(SIZE_STRATEGY.filter(lambda x: x != Range(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def test_rmod_with_range(self, size_1, size_2):
        """ Test rmod with a size. """
        self.assertEqual(
            size_1.__rmod__(size_2), Range(size_2.magnitude % size_1.magnitude)
        )


class RsubTestCase(unittest.TestCase):
    """ Test rsub. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def test_rsub(self, size_1, size_2):
        """ Test __rsub__. """
        self.assertEqual(
            size_1.__rsub__(size_2), Range(size_2.magnitude - size_1.magnitude)
        )


class RtruedivTestCase(unittest.TestCase):
    """ Test rtruediv. """

    @given(SIZE_STRATEGY.filter(lambda x: x != Range(0)), SIZE_STRATEGY)
    @settings(max_examples=10)
    def test_truediv_with_range(self, size_1, size_2):
        """ Test truediv with a size. """
        self.assertEqual(
            size_1.__rtruediv__(size_2), size_2.magnitude / size_1.magnitude
        )


class SubtractionTestCase(unittest.TestCase):
    """ Test subtraction. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    def test_subtraction(self, size_1, size_2):
        """ Test subtraction. """
        self.assertEqual(size_1 - size_2, Range(size_1.magnitude - size_2.magnitude))


class TruedivTestCase(unittest.TestCase):
    """ Test truediv. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY.filter(lambda x: x != Range(0)))
    @settings(max_examples=10)
    def test_truediv_with_range(self, size_1, size_2):
        """ Test truediv with a size. """
        self.assertEqual(size_1 / size_2, size_1.magnitude / size_2.magnitude)

    @given(SIZE_STRATEGY, NUMBERS_STRATEGY.filter(lambda x: x != 0))
    def test_truediv_with_number(self, size_1, size_2):
        """ Test truediv with a number. """
        self.assertEqual(size_1 / size_2, Range(size_1.magnitude / Fraction(size_2)))


class UnaryOperatorsTestCase(unittest.TestCase):
    """ Test unary operators. """

    @given(SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=5)
    def test_hash(self, size_1, size_2):
        """ Test that hash has the necessary property for hash table lookup. """
        size_3 = copy.deepcopy(size_1)
        self.assertTrue(hash(size_1) == hash(size_3))
        self.assertTrue(size_1 != size_2 or hash(size_1) == hash(size_2))

    @given(SIZE_STRATEGY)
    @settings(max_examples=5)
    def test_abs(self, size):
        """ Test absolute value. """
        self.assertEqual(abs(size), Range(abs(size.magnitude)))

    @given(SIZE_STRATEGY)
    @settings(max_examples=5)
    def test_neg(self, size):
        """ Test negation. """
        self.assertEqual(-size, Range(-size.magnitude))

    @given(SIZE_STRATEGY)
    @settings(max_examples=5)
    def test_pos(self, size):
        """ Test positive. """
        self.assertEqual(+size, size)


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
    # pylint: disable=invalid-name
    def test_distributivity1(self, s, n, m):
        """
        Assert distributivity across numbers.
        """
        self.assertEqual((n + m) * s, n * s + m * s)

    @given(SIZE_STRATEGY, SIZE_STRATEGY, NUMBERS_STRATEGY)
    @settings(max_examples=10)
    # pylint: disable=invalid-name
    def test_distributivity2(self, p, q, n):
        """
        Assert distributivity across sizes.
        """
        self.assertEqual((p + q) * n, p * n + q * n)

    @given(SIZE_STRATEGY, SIZE_STRATEGY, SIZE_STRATEGY)
    @settings(max_examples=10)
    # pylint: disable=invalid-name
    def test_associativity(self, p, q, r):
        """
        Assert associativity across sizes.
        """
        self.assertEqual((p + q) + r, p + (r + q))
