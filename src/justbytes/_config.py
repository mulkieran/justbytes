# Copyright (C) 2015-2016  Red Hat, Inc.
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

from ._constants import PRECISE_NUMERIC_TYPES
from ._constants import RoundingMethods
from ._constants import UNITS

from ._errors import RangeValueError


class StripConfig(object):
    """
    Stripping trailing zeros.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "strip=%(strip)s",
       "strip_exact=%(strip_exact)s",
       "strip_whole=%(strip_whole)s"
    ])

    def __init__(self, strip=False, strip_exact=False, strip_whole=True):
        """
        Initializer.

        :param bool strip: strip all trailing zeros
        :param bool strip_exact: strip if value is exact
        :param bool strip_whole: strip if value is exact and non-fractional

        strip is stronger than strip_exact which is stronger than strip_whole
        """
        self.strip = strip
        self.strip_exact = strip_exact
        self.strip_whole = strip_whole

    def __str__(self): # pragma: no cover
        values = {
           'strip' : self.strip,
           'strip_exact' : self.strip_exact,
           'strip_whole' : self.strip_whole
        }
        return "StripConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class DigitsConfig(object):
    """
    How to display digits.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "separator=%(separator)s",
       "use_caps=%(use_caps)s",
       "use_letters=%(use_letters)s"
    ])

    def __init__(
       self,
       separator='~',
       use_caps=False,
       use_letters=True
    ):
        """
        Initializer.

        :param str separator: separate for digits
        :param bool use_caps: if set, use capital letters
        :param bool use_letters: if set, use letters

        If digits in this base require more than one character.
        """
        self.separator = separator
        self.use_caps = use_caps
        self.use_letters = use_letters

    def __str__(self): # pragma: no cover
        values = {
           'separator' : self.separator,
           'use_caps' : self.use_caps,
           'use_letters' : self.use_letters
        }
        return "DigitsConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class DisplayConfig(object):
    """
    Superficial aspects of display.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "show_approx_str=%(show_approx_str)s",
       "show_base=%(show_base)s",
       "digits_config=%(digits_config)s",
       "strip_config-%(strip_config)s"
    ])

    def __init__(
       self,
       show_approx_str=True,
       show_base=False,
       digits_config=DigitsConfig(
          separator='~',
          use_caps=False,
          use_letters=True
       ),
       strip_config=StripConfig(
          strip=False,
          strip_exact=False,
          strip_whole=True
       )
    ):
        """
        Initializer.

        :param bool show_approx_str: distinguish approximate str values
        :param bool show_base: True if base prefix to be prepended
        :param DigitsConfig digits_config:
        :param StripConfig strip_config:

        There are only two base prefixes acknowledged, 0 for octal and 0x for
        hexadecimal.
        """
        self.show_approx_str = show_approx_str
        self.show_base = show_base
        self.digits_config = digits_config
        self.strip_config = strip_config

    def __str__(self):
        values = {
           'show_approx_str' : self.show_approx_str,
           'show_base' : self.show_base,
           'digits_config' : self.digits_config,
           'strip_config' : self.strip_config
        }
        return "DisplayConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class ValueConfig(object):
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
            raise RangeValueError(
               min_value,
               "min_value",
               "must be a precise positive numeric value."
            )

        if unit is not None and unit not in UNITS():
            raise RangeValueError(
               unit,
               "unit",
               "must be one of %s" % ", ".join(str(x) for x in UNITS())
            )

        if base < 2:
            raise RangeValueError(base, "base", "must be at least 2")

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
        return "ValueConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class RangeConfig(object):
    """ Configuration for :class:`Range` class. """

    DISPLAY_CONFIG = DisplayConfig(
       show_approx_str=True,
       show_base=False,
       digits_config=DigitsConfig(
          separator='~',
          use_caps=False,
          use_letters=True
       ),
       strip_config=StripConfig(
          strip=False,
          strip_exact=False,
          strip_whole=True
       )
    )

    VALUE_CONFIG = ValueConfig(
       max_places=2,
       min_value=1,
       binary_units=True,
       exact_value=False,
       unit=None,
       base=10,
       rounding_method=RoundingMethods.ROUND_HALF_ZERO
    )
    """ Default configuration for string display. """

    STRICT = False

    @classmethod
    def set_display_config(cls, config):
        """
        Set configuration for superficial aspects of display.

        :param DisplayConfig config: a configuration object
        """
        cls.DISPLAY_CONFIG = DisplayConfig(
            show_approx_str=config.show_approx_str,
            show_base=config.show_base,
            digits_config=config.digits_config,
            strip_config=config.strip_config
        )

    @classmethod
    def set_value_config(cls, config):
        """
        Set the configuration for computing the value of string representation.

        :param :class:`ValueConfig` config: a configuration object
        """
        cls.VALUE_CONFIG = ValueConfig(
            base=config.base,
            binary_units=config.binary_units,
            max_places=config.max_places,
            min_value=config.min_value,
            exact_value=config.exact_value,
            rounding_method=config.rounding_method,
            unit=config.unit
        )
