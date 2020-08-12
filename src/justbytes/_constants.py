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

""" Constants used by the justbytes package.

    Categories of constants:
     * Rounding methods
     * Size units, e.g., Ki, Mi
"""

# isort: STDLIB
import abc
from numbers import Rational

# isort: FIRSTPARTY
import justbases

from ._errors import RangeValueError

RoundingMethods = justbases.RoundingMethods


class Unit:
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
    abbr = property(lambda s: s._abbr, doc="abbreviation for unit, precedes 'B'")
    prefix = property(lambda s: s._prefix, doc="prefix for 'bytes'")

    def __int__(self):
        return self.factor


B = Unit(1, "", "")
""" The universal unit, bytes. """


class Units(metaclass=abc.ABCMeta):
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
            raise RangeValueError(exponent, "exponent", "no corresponding unit")
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

PRECISE_NUMERIC_TYPES = (int, Rational)

UNIT_TYPES = tuple(list(PRECISE_NUMERIC_TYPES) + [Unit])
