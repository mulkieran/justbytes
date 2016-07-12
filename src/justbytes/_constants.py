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

""" Constants used by the justbytes package.

    Categories of constants:
     * Rounding methods
     * Size units, e.g., Ki, Mi
"""

import abc

from numbers import Rational

import six

import justbases

from ._errors import RangeValueError

RoundingMethods = justbases.RoundingMethods


class Unit(object):
    """ Class to encapsulate unit information. """
    # pylint: disable=too-few-public-methods

    def __init__(self, factor, prefix, abbr):
        self._factor = factor
        self._prefix = prefix
        self._abbr = abbr

    def __str__(self):
        return self.abbr + "B"
    __repr__ = __str__

    # pylint: disable=protected-access
    factor = property(lambda s: s._factor, doc="numeric multiple of bytes")
    abbr = property(
       lambda s: s._abbr,
       doc="abbreviation for unit, precedes 'B'"
    )
    prefix = property(lambda s: s._prefix, doc="prefix for 'bytes'")

    def __int__(self):
        return self.factor

B = Unit(1, "", "")
""" The universal unit, bytes. """


@six.add_metaclass(abc.ABCMeta)
class Units(object):
    """
    Generic class for units.
    """
    # pylint: disable=too-few-public-methods

    FACTOR = abc.abstractproperty(doc="factor for each unit")

    _UNITS = abc.abstractproperty(doc="ordered list of units")

    _MAX_EXPONENT = None

    @classmethod
    def UNITS(cls):
        """
        Units of this class.
        """
        return cls._UNITS[:]

    @classmethod
    def unit_for_exp(cls, exponent):
        """
        Get the unit for the given exponent.

        :param int exponent: the exponent, 0 <= exponent < len(UNITS())
        """
        if exponent < 0 or exponent > cls.max_exponent():
            raise RangeValueError(
                exponent,
                "exponent",
                "no corresponding unit"
            )
        if exponent == 0:
            return B

        return cls._UNITS[exponent - 1]

    @classmethod
    def max_exponent(cls):
        """
        The maximum exponent for which there is a unit.

        :returns: the maximum exponent
        :rtype: int
        """
        if cls._MAX_EXPONENT is None:
            cls._MAX_EXPONENT = len(cls._UNITS)
        return cls._MAX_EXPONENT


class DecimalUnits(Units):
    """ Class to store decimal unit constants. """
    # pylint: disable=invalid-name
    # pylint: disable=too-few-public-methods

    FACTOR = 10 ** 3

    KB = Unit(FACTOR ** 1, "kilo", "k")
    MB = Unit(FACTOR ** 2, "mega", "M")
    GB = Unit(FACTOR ** 3, "giga", "G")
    TB = Unit(FACTOR ** 4, "tera", "T")
    PB = Unit(FACTOR ** 5, "peta", "P")
    EB = Unit(FACTOR ** 6, "exa", "E")
    ZB = Unit(FACTOR ** 7, "zetta", "Z")
    YB = Unit(FACTOR ** 8, "yotta", "Y")

    _UNITS = [KB, MB, GB, TB, PB, EB, ZB, YB]


class BinaryUnits(Units):
    """ Class to store binary unit constants. """
    # pylint: disable=too-few-public-methods

    FACTOR = 2 ** 10

    KiB = Unit(FACTOR ** 1, "kibi", "Ki")
    MiB = Unit(FACTOR ** 2, "mebi", "Mi")
    GiB = Unit(FACTOR ** 3, "gibi", "Gi")
    TiB = Unit(FACTOR ** 4, "tebi", "Ti")
    PiB = Unit(FACTOR ** 5, "pebi", "Pi")
    EiB = Unit(FACTOR ** 6, "exbi", "Ei")
    ZiB = Unit(FACTOR ** 7, "zebi", "Zi")
    YiB = Unit(FACTOR ** 8, "yobi", "Yi")

    _UNITS = [KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB]


def UNITS():
    """ All unit constants. """
    return [B] + BinaryUnits.UNITS() + DecimalUnits.UNITS()

ROUNDING_METHODS = RoundingMethods.METHODS

PRECISE_NUMERIC_TYPES = tuple(list(six.integer_types) + [Rational])

UNIT_TYPES = tuple(list(PRECISE_NUMERIC_TYPES) + [Unit])
