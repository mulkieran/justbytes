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

""" Tiny classes used by some methods to pack up their results. """

import justbases


Radix = justbases.Radix


class Repr(object):
    """
    Representation of a Size object.
    """
    # pylint: disable=too-few-public-methods

    def __init__( # pylint: disable=too-many-arguments
       self,
       approximate,
       positive,
       integer_part,
       fractional_part,
       unit,
       base=10
    ):
        """
        Initializer.

        :param bool approximate: True if the value is approximate
        :param bool positive: True if the value is positive (or 0)
        :param integer_part: the integer part
        :type integer_part: list of int
        :param fractional_part: the fractional part
        :type fractional_part: list of int
        :param unit: the unit (of UNITS)
        :param int base: the base of the representation (default 10)
        """
        self.approximate = approximate
        self.positive = positive
        self.integer_part = integer_part
        self.fractional_part = fractional_part
        self.unit = unit
        self.base = base


class RadixNumber(object):
    """ Represents a class with a radix and possibly repeating digits. """
    # pylint: disable=too-few-public-methods

    def __init__(self, sign, left, non_repeating, repeating):
        """
        Initializer.

        :param int sign: -1 for negative, 1 for positive
        :param int left: the number to the left of the point
        :param non_repeating: non-repeating numbers to the right of the point
        :param repeating: repeating numbers to the right of the point
        """
        self.sign = sign
        self.left = left
        self.non_repeating = non_repeating
        self.repeating = repeating
