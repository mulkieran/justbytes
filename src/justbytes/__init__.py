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

""" The public interface of the justbytes package.

    Contents:

    * Unit constants in SI and binary units
       - Universal:
          * B

       - SI:
          * KB
          * MB
          * GB
          * TB
          * PB
          * EB
          * ZB
          * YB

       - Binary:
          * KiB
          * MiB
          * GiB
          * TiB
          * PiB
          * EiB
          * ZiB
          * YiB

       - UNITS: :func:`._constants.UNITS`

    * Rounding constants, with meaning as for the Python decimal module:
       - ROUND_DOWN
       - ROUND_HALF_DOWN
       - ROUND_HALF_UP
       - ROUND_UP

       - ROUNDING_METHODS

    * Configuration classes:
       - StrConfig: :class:`._config.StrConfig`

    * Exception classes:
       - RangeError: :class:`._errors.RangeError`
       - RangeValueError: :class:`._errors.RangeValueError`

    * Range classes:
       - Range: :class:`._size.Range`
       - AI: :class:`._sizes.AI`

    All parts of the public interface of justbytes must be imported directly
    from the top-level justbytes module, as::

        from justbytes import Range
        from justbytes import KiB
        from justbytes import RangeError

        s = Range(24, KiB)
        try:
            s + 32
        except RangeError as e:
            raise e
"""
# pylint: disable=invalid-name
# pylint: disable=wrong-import-position

# CONFIGURATION
from ._config import (
    BaseConfig,
    Config,
    DigitsConfig,
    DisplayConfig,
    StringConfig,
    StripConfig,
    ValueConfig,
)

# ROUNDING CONSTANTS
# UNIT CONSTANTS
from ._constants import ROUNDING_METHODS, UNITS, B
from ._constants import BinaryUnits as _BinaryUnits
from ._constants import DecimalUnits as _DecimalUnits
from ._constants import RoundingMethods as _RoundingMethods

# EXCEPTIONS
from ._errors import RangeError, RangeValueError

# SIZE
from ._size import Range
from ._sizes import AI

# VERSION
from .version import __version__

KB = _DecimalUnits.KB
MB = _DecimalUnits.MB
GB = _DecimalUnits.GB
TB = _DecimalUnits.TB
PB = _DecimalUnits.PB
EB = _DecimalUnits.EB
ZB = _DecimalUnits.ZB
YB = _DecimalUnits.YB

KiB = _BinaryUnits.KiB
MiB = _BinaryUnits.MiB
GiB = _BinaryUnits.GiB
TiB = _BinaryUnits.TiB
PiB = _BinaryUnits.PiB
EiB = _BinaryUnits.EiB
ZiB = _BinaryUnits.ZiB
YiB = _BinaryUnits.YiB


ROUND_DOWN = _RoundingMethods.ROUND_DOWN
ROUND_HALF_DOWN = _RoundingMethods.ROUND_HALF_DOWN
ROUND_HALF_UP = _RoundingMethods.ROUND_HALF_UP
ROUND_HALF_ZERO = _RoundingMethods.ROUND_HALF_ZERO
ROUND_TO_ZERO = _RoundingMethods.ROUND_TO_ZERO
ROUND_UP = _RoundingMethods.ROUND_UP
