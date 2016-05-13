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

""" Range class, for creating instances of Range objects.

    Contains a few documented methods and a number of __*__ methods
    implementing arithmetic operations. Precise numeric types
    such as int and Decimal may also occur in some arithmetic expressions,
    but all occurrances of floating point numbers in arithmetic expressions
    will cause an exception to be raised.
"""

from fractions import Fraction

import six

import justbases

from ._config import Config

from ._errors import RangeFractionalResultError
from ._errors import RangeNonsensicalBinOpError
from ._errors import RangeNonsensicalBinOpValueError
from ._errors import RangePowerResultError
from ._errors import RangeValueError

from ._constants import B
from ._constants import BinaryUnits
from ._constants import DecimalUnits
from ._constants import PRECISE_NUMERIC_TYPES
from ._constants import RoundingMethods
from ._constants import UNIT_TYPES

from ._util.generators import next_or_last
from ._util.generators import take_until_satisfied


class Range(object):
    """ Class for instantiating Range objects. """

    _BYTES_SYMBOL = "B"

    @classmethod
    def _as_single_number(cls, value, config):
        """
        Returns a rational value as a single number according to the
        specified configuration.

        :param Rational value: a numeric value
        :param ValueConfig config: how to calculate the value to display

        :returns: the result and its relation to ``value``
        :rtype: Radix * int
        """
        return justbases.Radices.from_rational(
           value,
           config.base,
           config.max_places,
           config.rounding_method
        )

    @classmethod
    def _get_unit_value(cls, unit):
        """
        Returns numeric value for unit.

        :param unit: the unit
        :type unit: object
        :returns: None if not convertable, else numeric value
        :rtype: Fraction or NoneType
        """
        if not isinstance(unit, UNIT_TYPES) and  not isinstance(unit, Range):
            return None
        factor = getattr(unit, 'factor', getattr(unit, 'magnitude', None))
        try:
            return Fraction(factor if factor is not None else unit)
        except (ValueError, TypeError):
            return None

    def __init__(self, value=0, units=None):
        """ Initialize a new Range object.

            :param value: a size value, default is 0
            :type value: Range, or any finite numeric type (possibly as str)
            :param units: the units of the size, default is None
            :type units: any of the publicly defined units constants or a Range
            :raises RangeValueError: on bad parameters

            Must pass None as units argument if value has type Range.

            The units number must be a precise numeric type.
        """
        if isinstance(value, six.string_types) or \
           isinstance(value, PRECISE_NUMERIC_TYPES):
            try:
                units = B if units is None else units
                factor = self._get_unit_value(units)
                if factor is None:
                    raise RangeValueError(units, "units")
                magnitude = Fraction(value) * factor
            except (ValueError, TypeError):
                raise RangeValueError(value, "value")

        elif isinstance(value, Range):
            if units is not None:
                raise RangeValueError(
                   units,
                   "units",
                   "meaningless when Range value is passed"
                )
            magnitude = value.magnitude # pylint: disable=no-member
        else:
            raise RangeValueError(value, "value")

        if Config.STRICT is True and magnitude.denominator != 1:
            raise RangeFractionalResultError()
        self._magnitude = magnitude

    @property
    def magnitude(self):
        """
        :returns: the number of bytes
        :rtype: Fraction
        """
        return self._magnitude

    def getStringInfo(self, config):
        """
        Return a representation of the size.

        :param `ValueConfig` config: representation configuration
        :returns: a tuple representing the number to display
        :rtype: tuple of Radix * int * unit
        """
        (magnitude, units) = self.components(config)
        (result, relation) = self._as_single_number(magnitude, config)
        return (result, relation, units)

    def getString(self, config):
        """
        Return a string representation of the size.

        :param StringConfig config: the configuration
        :returns: a string representation
        :rtype: str
        :raises RangeValueError: if configuration is not satisfiable
        """
        (result, relation, units) = self.getStringInfo(config.VALUE_CONFIG)
        number = config.DISPLAY_IMPL.xform(result, relation)
        return "%s %s" % (number, units.abbr + self._BYTES_SYMBOL)

    def __str__(self):
        return self.getString(Config.STRING_CONFIG)

    def __repr__(self):
        """
        Displaying value to arbitrary precision could be time consuming.

        Instead, explicitly round to nearest integer, and display relation.

        Usually, the magnitude will be an integer.
        """
        (value, _) = \
           justbases.Rationals.round_to_int(
              self._magnitude,
              RoundingMethods.ROUND_HALF_ZERO
           )
        return "Range(%s)" % value

    def __deepcopy__(self, memo):
        # pylint: disable=unused-argument
        return Range(self._magnitude)

    def __nonzero__(self):
        return self._magnitude != 0

    def __int__(self):
        return int(self._magnitude)
    __trunc__ = __int__

    def __hash__(self):
        return hash(self._magnitude)

    def __bool__(self):
        return self.__nonzero__()

    # UNARY OPERATIONS

    def __abs__(self):
        return Range(abs(self._magnitude))

    def __neg__(self):
        return Range(-(self._magnitude))

    def __pos__(self):
        return Range(self._magnitude)

    # BINARY OPERATIONS
    def __add__(self, other):
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("+", other)
        return Range(self._magnitude + other.magnitude)
    __radd__ = __add__

    def __divmod__(self, other):
        # other * div + rem = self
        # Therefore, T(rem) = T(self) = Range
        #            T(div) = Range, if T(other) is numeric
        #                   = Fraction, if T(other) is Range
        if isinstance(other, Range):
            try:
                (div, rem) = divmod(self._magnitude, other.magnitude)
                return (div, Range(rem))
            except ZeroDivisionError:
                raise RangeNonsensicalBinOpValueError("divmod", other)
        if isinstance(other, PRECISE_NUMERIC_TYPES):
            try:
                (div, rem) = divmod(self._magnitude, Fraction(other))
                return (Range(div), Range(rem))
            except (TypeError, ValueError, ZeroDivisionError):
                raise RangeNonsensicalBinOpValueError("divmod", other)
        raise RangeNonsensicalBinOpError("divmod", other)

    def __rdivmod__(self, other):
        # self * div + rem = other
        # Therefore, T(rem) = T(other)
        #            T(div) = Fraction
        # and T(other) is Range
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("rdivmod", other)
        try:
            (div, rem) = divmod(other.magnitude, self._magnitude)
            return (div, Range(rem))
        except ZeroDivisionError:
            raise RangeNonsensicalBinOpValueError("rdivmod", other)

    def __eq__(self, other):
        return isinstance(other, Range) and \
           self._magnitude == other.magnitude

    def __floordiv__(self, other):
        # other * floor + rem = self
        # Therefore, T(floor) = Range, if T(other) is numeric
        #                     = int, if T(other) is Range
        if isinstance(other, Range):
            try:
                return self._magnitude.__floordiv__(other.magnitude)
            except ZeroDivisionError:
                raise RangeNonsensicalBinOpValueError("floordiv", other)
        if isinstance(other, PRECISE_NUMERIC_TYPES):
            try:
                return Range(self._magnitude.__floordiv__(Fraction(other)))
            except (TypeError, ValueError, ZeroDivisionError):
                raise RangeNonsensicalBinOpValueError("floordiv", other)
        raise RangeNonsensicalBinOpError("floordiv", other)

    def __rfloordiv__(self, other):
        # self * floor + rem = other
        # Therefore, T(floor) = int and T(other) is Range
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("rfloordiv", other)
        try:
            return other.magnitude.__floordiv__(self._magnitude)
        except ZeroDivisionError:
            raise RangeNonsensicalBinOpValueError("rfloordiv", other)

    def __ge__(self, other):
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError(">=", other)
        return self._magnitude >= other.magnitude

    def __gt__(self, other):
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError(">", other)
        return self._magnitude > other.magnitude

    def __le__(self, other):
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("<=", other)
        return self._magnitude <= other.magnitude

    def __lt__(self, other):
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("<", other)
        return self._magnitude < other.magnitude

    def __mod__(self, other):
        # other * div + mod = self
        # Therefore, T(mod) = Range
        if isinstance(other, Range):
            try:
                return Range(self._magnitude % other.magnitude)
            except ZeroDivisionError:
                raise RangeNonsensicalBinOpValueError('%', other)
        if isinstance(other, PRECISE_NUMERIC_TYPES):
            try:
                return Range(self._magnitude % Fraction(other))
            except (TypeError, ValueError, ZeroDivisionError):
                raise RangeNonsensicalBinOpValueError('%', other)
        raise RangeNonsensicalBinOpError("%", other)

    def __rmod__(self, other):
        # self * div + mod = other
        # Therefore, T(mod) = T(other) and T(other) = Range.
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("rmod", other)
        try:
            return Range(other.magnitude % Fraction(self._magnitude))
        except (TypeError, ValueError, ZeroDivisionError):
            raise RangeNonsensicalBinOpValueError("rmod", other)

    def __mul__(self, other):
        # self * other = mul
        # Therefore, T(mul) = Range and T(other) is a numeric type.
        if isinstance(other, PRECISE_NUMERIC_TYPES):
            try:
                return Range(self._magnitude * Fraction(other))
            except (TypeError, ValueError):
                raise RangeNonsensicalBinOpError("*", other)
        if isinstance(other, Range):
            raise RangePowerResultError()
        raise RangeNonsensicalBinOpError("*", other)
    __rmul__ = __mul__

    def __pow__(self, other):
        # pylint: disable=no-self-use
        # Cannot represent multiples of Ranges.
        if not isinstance(other, PRECISE_NUMERIC_TYPES):
            raise RangeNonsensicalBinOpError("**", other)
        raise RangePowerResultError()

    def __rpow__(self, other):
        # A Range exponent is meaningless.
        raise RangeNonsensicalBinOpError("rpow", other)

    def __ne__(self, other):
        return not isinstance(other, Range) or \
           self._magnitude != other.magnitude

    def __sub__(self, other):
        # self - other = sub
        # Therefore, T(sub) = T(self) = Range and T(other) = Range.
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("-", other)
        return Range(self._magnitude - other.magnitude)

    def __rsub__(self, other):
        # other - self = sub
        # Therefore, T(sub) = T(self) = Range and T(other) = Range.
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("rsub", other)
        return Range(other.magnitude - self._magnitude)

    def __truediv__(self, other):
        # other * truediv = self
        # Therefore, T(truediv) = Fraction, if T(other) is Range
        if isinstance(other, Range):
            try:
                return self._magnitude.__truediv__(other.magnitude)
            except ZeroDivisionError:
                raise RangeNonsensicalBinOpValueError("truediv", other)
        elif isinstance(other, PRECISE_NUMERIC_TYPES):
            try:
                return Range(self._magnitude.__truediv__(Fraction(other)))
            except (TypeError, ValueError, ZeroDivisionError):
                raise RangeNonsensicalBinOpValueError("truediv", other)
        raise RangeNonsensicalBinOpError("truediv", other)

    __div__ = __truediv__

    def __rtruediv__(self, other):
        # self * truediv = other
        # Therefore, T(truediv) = Fraction and T(other) = Range.
        if not isinstance(other, Range):
            raise RangeNonsensicalBinOpError("rtruediv", other)
        try:
            return other.magnitude.__truediv__(self._magnitude)
        except ZeroDivisionError:
            raise RangeNonsensicalBinOpValueError("rtruediv", self)

    __rdiv__ = __rtruediv__

    def convertTo(self, spec=None):
        """ Return the size in the units indicated by the specifier.

            :param spec: a units specifier
            :type spec: a units specifier or :class:`Range`
            :returns: a numeric value in the units indicated by the specifier
            :rtype: :class:`fractions.Fraction`
            :raises RangeValueError: if unit specifier is non-positive
        """
        spec = B if spec is None else spec
        factor = self._get_unit_value(spec)
        if factor is None:
            raise RangeValueError(spec, "spec")

        if factor <= 0:
            raise RangeValueError(
               factor,
               "factor",
               "can not convert to non-positive unit %s"
            )

        return self._magnitude / factor

    def componentsList(self, binary_units=True):
        """ Yield a representation of this size for every unit,
            decomposed into a Fraction value and a unit specifier
            tuple.

            :param bool binary_units: binary units if True, else SI
        """
        units = BinaryUnits if binary_units else DecimalUnits

        for unit in [B] + units.UNITS():
            yield (self.convertTo(unit), unit)

    def components(self, config=Config.STRING_CONFIG.VALUE_CONFIG):
        """ Return a representation of this size, decomposed into a
            Fraction value and a unit specifier tuple.

            :param ValueConfig config: configuration

            :returns: a pair of a decimal value and a unit
            :rtype: tuple of Fraction and unit
            :raises RangeValueError: if min_value is not usable

            The meaning of the parameters is the same as for
            :class:`._config.ValueConfig`.
        """
        units = BinaryUnits if config.binary_units else DecimalUnits

        if config.unit is not None:
            return (self.convertTo(config.unit), config.unit)

        # Find the smallest prefix which will allow a number less than
        # FACTOR * min_value to the left of the decimal point.
        # If the number is so large that no prefix will satisfy this
        # requirement use the largest prefix.
        limit = units.FACTOR * Fraction(config.min_value)
        components = self.componentsList(binary_units=config.binary_units)
        candidates = \
           list(take_until_satisfied(lambda x: abs(x[0]) < limit, components))

        if config.exact_value:
            return next_or_last(
               lambda x: self._as_single_number(x[0], config)[1] == 0,
               reversed(candidates)
            )
        else:
            return candidates[-1]

    def roundTo(self, unit, rounding, bounds=(None, None)):
        # pylint: disable=line-too-long
        """ Rounds to unit specified as a named constant or a Range.

            :param unit: a unit specifier
            :type unit: any non-negative :class:`Range` or element in :func:`._constants.UNITS`
            :param rounding: rounding mode to use
            :type rounding: a field of :class:`._constants.RoundingMethods`
            :param bounds: lower and upper bounds on the value
            :type bounds: tuple of (Range or NoneType) * (Range or NoneType)
            :returns: appropriately rounded Range
            :rtype: :class:`Range`
            :raises RangeValueError: on unusable arguments

            If unit is Range(0), returns Range(0).

            Note that rounding may be in the opposite direction of the rounding
            method, e.g., when the rounding method is ROUND_DOWN but the current
            value is below the lower bound the ultimate direction of the
            rounding will be up.
        """
        factor = self._get_unit_value(unit)
        if factor is None:
            raise RangeValueError(unit, "unit")

        if factor < 0:
            raise RangeValueError(factor, "factor")

        if factor == 0:
            res = Range(0)
        else:
            magnitude = self._magnitude / factor
            (rounded, _) = justbases.Rationals.round_to_int(magnitude, rounding)
            res = Range(rounded * factor)

        (lower, upper) = bounds
        if lower is not None and upper is not None:
            if lower > upper:
                raise RangeValueError(bounds, 'bounds')

        if lower is not None and res < lower:
            return lower
        if upper is not None and res > upper:
            return upper
        return res
