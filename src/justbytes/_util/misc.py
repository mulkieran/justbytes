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

import justbases


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

    (radix_num, relation) = \
       justbases.Radices.from_rational(
          magnitude,
          10,
          places,
          justbases.RoundingMethods.ROUND_HALF_DOWN
       )
    return (
       relation == 0,
       1 if radix_num.positive else -1,
       ''.join(str(x) for x in radix_num.integer_part),
       ''.join(str(x) for x in radix_num.non_repeating_part)
    )
