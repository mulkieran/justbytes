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

""" Configuration of the justbytes package. """

from ._constants import B
from ._constants import PRECISE_NUMERIC_TYPES
from ._constants import RoundingMethods
from ._constants import UNITS

from ._errors import SizeValueError

class DisplayConfig(object):
    """
    Superficial aspects of display.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "approx_symbol=%(approx_symbol)s",
       "show_approx_str=%(show_approx_str)s",
       "strip=%(strip)s",
    ])

    def __init__(
       self,
       strip=False,
       show_approx_str=True,
       approx_symbol='@'
    ):
        """
        Initializer.

        :param bool strip: True if trailing zeros are to be stripped.
        :param bool show_approx_str: distinguish approximate str values
        :param str approx_symbol: symbol to indicate approximation

        If strip is True and there is a fractional quantity, trailing
        zeros are removed up to (and including) the decimal point.

        The default for strip is False, so that precision is always shown
        to max_places.
        """
        self._strip = strip
        self._show_approx_str = show_approx_str
        self._approx_symbol = approx_symbol

    def __str__(self):
        values = {
           'approx_symbol': self.approx_symbol,
           'show_approx_str' : self.show_approx_str,
           'strip' : self.strip,
        }
        return "StrConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__

    # pylint: disable=protected-access
    approx_symbol = property(lambda s: s._approx_symbol)
    strip = property(lambda s: s._strip)
    show_approx_str = property(lambda s: s._show_approx_str)

class StrConfig(object):
    """ Configuration for __str__ method.

        If max_places is set to None, all non-zero digits after the
        decimal point will be shown.  Otherwise, max_places digits will
        be shown.

        min_value sets the smallest value allowed.
        If min_value is 10, then single digits on the lhs of
        the decimal will be avoided if possible. In that case,
        9216 KiB is preferred to 9 MiB. However, 1 B has no alternative.
        If min_value is 1, however, 9 MiB is preferred.
        If min_value is 0.1, then 0.75 GiB is preferred to 768 MiB,
        but 0.05 GiB is still displayed as 51.2 MiB.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "binary_units=%(binary_units)s",
       "exact_value=%(exact_value)s",
       "max_places=%(max_places)s",
       "min_value=%(min_value)s",
       "unit=%(unit)s"
    ])

    def __init__(
       self,
       max_places=2,
       min_value=1,
       binary_units=True,
       exact_value=False,
       unit=None
    ):
        """ Initializer.

            :param max_places: number of decimal places to use, default is 2
            :type max_places: an integer type or NoneType
            :param min_value: Lower bound for value, default is 1.
            :type min_value: A precise numeric type: int or Decimal
            :param bool binary_units: binary units if True, else SI
            :param bool exact_value: uses largest units that allow exact value
            :param unit: use the specified unit, overrides other options
        """
        # pylint: disable=too-many-arguments
        if min_value < 0 or \
           not isinstance(min_value, PRECISE_NUMERIC_TYPES):
            raise SizeValueError(
               min_value,
               "min_value",
               "must be a precise positive numeric value."
            )

        if unit is not None and unit not in UNITS():
            raise SizeValueError(
               unit,
               "unit",
               "must be one of %s" % ", ".join(str(x) for x in UNITS())
            )

        self._max_places = max_places
        self._min_value = min_value
        self._binary_units = binary_units
        self._exact_value = exact_value
        self._unit = unit

    def __str__(self):
        values = {
           'binary_units' : self.binary_units,
           'exact_value' : self.exact_value,
           'max_places' : self.max_places,
           'min_value' : self.min_value,
           'unit' : self.unit
        }
        return "StrConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__

    # pylint: disable=protected-access
    exact_value = property(lambda s: s._exact_value)
    max_places = property(lambda s: s._max_places)
    min_value = property(lambda s: s._min_value)
    binary_units = property(lambda s: s._binary_units)
    unit = property(lambda s: s._unit)

class InputConfig(object):
    """ Configuration for input of Sizes.

        Specifies rounding unit and method for Sizes constructed from
        user input.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join(["method=%(method)s", "unit=%(unit)s"])

    def __init__(self, unit=B, method=RoundingMethods.ROUND_DOWN):
        """ Initializer.

            :param unit: unit to round to, default is B
            :type unit: an instance of :func:`._constants.UNITS`
            :param method: rounding method, default is ROUND_DOWN
            :type method: instance of :func:`._constants.ROUNDING_METHODS`
        """
        self._unit = unit
        self._method = method

    def __str__(self):
        values = {'method' : self.method, 'unit' : self.unit}
        return "InputConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__

    # pylint: disable=protected-access
    method = property(lambda s: s._method)
    unit = property(lambda s: s._unit)


class SizeConfig(object):
    """ Configuration for :class:`Size` class. """

    DISPLAY_CONFIG = DisplayConfig(False, True, '@')

    STR_CONFIG = StrConfig(2, 1, True, False, None)
    """ Default configuration for string display. """

    INPUT_CONFIG = InputConfig(B, RoundingMethods.ROUND_DOWN)
    """ Default configuration for interpreting input values. """

    STRICT = False

    @classmethod
    def set_display_config(cls, config):
        """
        Set configuration for superficial aspects of display.

        :param DisplayConfig config: a configuration object
        """
        cls.DISPLAY_CONFIG = DisplayConfig(
            approx_symbol=config.approx_symbol,
            show_approx_str=config.show_approx_str,
            strip=config.strip
        )

    @classmethod
    def set_str_config(cls, config):
        """ Set the configuration for __str__ method for all Size objects.

            :param :class:`StrConfig` config: a configuration object
        """
        cls.STR_CONFIG = StrConfig(
            binary_units=config.binary_units,
            max_places=config.max_places,
            min_value=config.min_value,
            exact_value=config.exact_value,
            unit=config.unit
        )

    @classmethod
    def set_input_config(cls, config):
        """ Set the configuration for input method for all Size objects.

            :param :class:`.InputConfig` config: a configuration object
        """
        cls.INPUT_CONFIG = InputConfig(
            method=config.method,
            unit=config.unit
        )
