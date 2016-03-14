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
       "show_approx_str=%(show_approx_str)s",
       "strip=%(strip)s",
       "strip_exact=%(strip_exact)s"
    ])

    def __init__(
       self,
       strip=False,
       show_approx_str=True,
       strip_exact=True
    ):
        """
        Initializer.

        :param bool strip: True if trailing zeros are to be stripped.
        :param bool show_approx_str: distinguish approximate str values
        :param bool strip_exact: True if stripping exact quantities

        If strip is True and there is a fractional quantity, trailing
        zeros are removed up to (and including) the decimal point.

        The default for strip is False, so that precision is always shown
        to max_places.

        strip_exact is like strip, but trailing zeros are only removed if
        the number represented equals its representation. If strip is True,
        strip_exact does nothing.
        """
        self.strip = strip
        self.show_approx_str = show_approx_str
        self.strip_exact = strip_exact

    def __str__(self):
        values = {
           'show_approx_str' : self.show_approx_str,
           'strip' : self.strip,
           'strip_exact' : self.strip_exact
        }
        return "StrConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


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
       "base=%(base)s",
       "binary_units=%(binary_units)s",
       "exact_value=%(exact_value)s",
       "max_places=%(max_places)s",
       "min_value=%(min_value)s",
       "rounding_method=%(rounding_method)s",
       "unit=%(unit)s"
    ])

    def __init__(
       self,
       max_places=2,
       min_value=1,
       binary_units=True,
       exact_value=False,
       unit=None,
       base=10,
       rounding_method=RoundingMethods.ROUND_HALF_ZERO
    ):
        """ Initializer.

            :param max_places: number of decimal places to use, default is 2
            :type max_places: an integer type or NoneType
            :param min_value: Lower bound for value, default is 1.
            :type min_value: A precise numeric type: int or Decimal
            :param bool binary_units: binary units if True, else SI
            :param bool exact_value: uses largest units that allow exact value
            :param unit: use the specified unit, overrides other options
            :param base: numeric base
            :param rounding_method: one of RoundingMethods.METHODS()
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

        if base < 2:
            raise SizeValueError(base, "base", "must be at least 2")

        self.max_places = max_places
        self.min_value = min_value
        self.binary_units = binary_units
        self.exact_value = exact_value
        self.unit = unit
        self.base = base
        self.rounding_method = rounding_method

    def __str__(self):
        values = {
           'base' : self.base,
           'binary_units' : self.binary_units,
           'exact_value' : self.exact_value,
           'max_places' : self.max_places,
           'min_value' : self.min_value,
           'rounding_method' : self.rounding_method,
           'unit' : self.unit
        }
        return "StrConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


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
        self.unit = unit
        self.method = method

    def __str__(self):
        values = {'method' : self.method, 'unit' : self.unit}
        return "InputConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class SizeConfig(object):
    """ Configuration for :class:`Size` class. """

    DISPLAY_CONFIG = DisplayConfig(False, True)

    STR_CONFIG = StrConfig(
       2,
       1,
       True,
       False,
       None,
       10,
       RoundingMethods.ROUND_HALF_ZERO
    )
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
            show_approx_str=config.show_approx_str,
            strip=config.strip,
            strip_exact=config.strip_exact
        )

    @classmethod
    def set_str_config(cls, config):
        """ Set the configuration for __str__ method for all Size objects.

            :param :class:`StrConfig` config: a configuration object
        """
        cls.STR_CONFIG = StrConfig(
            base=config.base,
            binary_units=config.binary_units,
            max_places=config.max_places,
            min_value=config.min_value,
            exact_value=config.exact_value,
            rounding_method=config.rounding_method,
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
