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

""" Miscellaneous utilities. """

from fractions import Fraction

import six

from .._errors import SizeValueError

from .._types import RadixNumber

from .math_util import long_decimal_division


def get_decimal_info(value):
    """
    Get the full representation of the decimal value.

    :param value: the value, a precise numeric quantity
    :returns: a decimal representation of the value
    :rtype: RadixNumber
    """
    if isinstance(value, float):
        raise SizeValueError(
           value,
           "value",
           "must not be a float"
        )

    value = Fraction(value)
    (sign, left, non_repeating, repeating) = long_decimal_division(
       value.denominator,
       value.numerator
    )

    return RadixNumber(sign, left, non_repeating, repeating)

def convert_magnitude(left, non_repeating, repeating, places=2):
    """ Convert magnitude to a decimal string.

        :param int left: the left side
        :param non_repeating: the non repeating part after the radix
        :type non_repeating: list of int
        :param repeating: the repeating part
        :type repeating: list of int
        :param places: number of decimal places to use, default is 2
        :type places: an integer type or NoneType

        :returns: a representation of the value
        :rtype: tuple of str * str

        Components of the result are:
        1. a string representing the value to the left of the decimal
        2. a string representing the value to the right of the decimal

        Since a rational number may be a non-terminating decimal
        quantity, this representation is not guaranteed to be exact, regardless
        of the value of places.

        Even in the case of a terminating decimal representation, the
        representation may be inexact if the number of significant digits
        is too large for the precision of the Decimal operations as
        specified by the context.
    """
    if places is not None and \
       (places < 0 or not isinstance(places, six.integer_types)):
        raise SizeValueError(
           places,
           "places",
           "must be None or a non-negative integer value"
        )

    places = len(non_repeating) + len(repeating) if places is None else places

    right_side = non_repeating[:]
    if len(repeating) > 0:
        while len(right_side) <= places:
            right_side += repeating

    if len(right_side) > places:
        right = right_side[:places]
        next_digits = right_side[places:]
        decider = next((d for d in next_digits if d != 5), None)
        if decider is not None:
            if decider > 5:
                right = str(int("".join(str(x) for x in right) or "0") + 1)
                right = [l for l in right]
        if len(right) > places:
            left = left + int(right[0])
            right = right[1:]
        elif len(right) < places:
            right = [0 for _ in range(places - len(right))] + right
    else:
        right = right_side[:] + [0 for _ in range(places - len(right_side))]

    return (str(left), "".join(str(x) for x in right))

def get_string_info(magnitude, places):
    """
    Get information about the string that represents this magnitude.

    :param Fraction magnitude: the magnitude
    :param int places: the number of places after the decimal pt
    :returns: a tuple with string information
    :rtypes: tuple of bool * int * str * str

    Components of result are:
    1. True if the value is exact, otherwise False
    2. -1 if the value is negative, otherwise 1
    3. the string representing the numbers to the left of the radix
    4. the string representing the numbers to the right of the radix
    """

    radix_num = get_decimal_info(magnitude)
    (left, right) = convert_magnitude(
       radix_num.left,
       radix_num.non_repeating,
       radix_num.repeating,
       places=places
    )
    exact = \
       Fraction(radix_num.sign * Fraction("%s.%s" % (left, right))) == magnitude
    return (exact, radix_num.sign, left, right)
