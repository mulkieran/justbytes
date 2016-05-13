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

import justbases

from ._constants import PRECISE_NUMERIC_TYPES
from ._constants import RoundingMethods
from ._constants import UNITS

from ._errors import RangeValueError


class BaseConfig(justbases.BaseConfig):
    """
    Configuration for display of bases.

    Override defaults of justbases.BaseConfig.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, use_prefix=False, use_subscript=False):
        """
        Initializer.

        :param bool use_prefix: display base as prefix
        :param bool use_subscript: display base as subscript
        """

        super(BaseConfig, self).__init__(
           use_prefix=use_prefix,
           use_subscript=use_subscript
        )

DigitsConfig = justbases.DigitsConfig
StripConfig = justbases.StripConfig

class DisplayConfig(justbases.DisplayConfig):
    """
    DisplayConfig overrides justbases.DisplayConfig's defaults.
    """
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        show_approx_str=True,
        base_config=BaseConfig(),
        digits_config=DigitsConfig(),
        strip_config=StripConfig()
    ):
        """
        Intializer.

        :param boolean show_approx_str: whether to indicate approximation
        :param BaseConfig base_config: the base config
        :param DigitsConfig digits_config: the digits config
        :param StripConfig strip_config: the strip config
        """
        super(DisplayConfig, self).__init__(
           show_approx_str=show_approx_str,
           base_config=base_config,
           digits_config=digits_config,
           strip_config=strip_config
        )


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
        if max_places is not None and max_places < 0:
            raise RangeValueError(
               max_places,
               "max_places",
               "must be an int at least 0"
            )

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


class StringConfig(object):
    """ Configuration for :class:`Range` class. """
    # pylint: disable=too-few-public-methods

    def __init__(self, value_config, display_config, display_impl):
        """
        Initializer.

        :param ValueConfig value_config: the value configuration
        :param DisplayConfig display_config: the display configuration
        :param type display_impl: display implementation class
        :raises RangeValueError: if configuration and implementation can't work
        """
        try:
            self.DISPLAY_IMPL = display_impl(display_config, value_config.base)
        except justbases.BasesError as err:
            raise RangeValueError(display_config, "display_config", str(err))

        self.DISPLAY_IMPL_CLASS = display_impl
        self.VALUE_CONFIG = value_config
        self.DISPLAY_CONFIG = display_config


class Config(object):
    """
    The super top-level configuration class for ranges.
    """

    STRING_CONFIG = \
       StringConfig(ValueConfig(), DisplayConfig(), justbases.String)

    STRICT = False

    @classmethod
    def set_display_impl(cls, impl): # pragma: no cover
        """
        Set display implementation.

        :param type impl: the display implementation class
        """
        cls.STRING_CONFIG = StringConfig(
           cls.STRING_CONFIG.VALUE_CONFIG,
           cls.STRING_CONFIG.DISPLAY_CONFIG,
           impl
        )

    @classmethod
    def set_display_config(cls, config):
        """
        Set configuration for superficial aspects of display.

        :param DisplayConfig config: a configuration object
        """
        cls.STRING_CONFIG = StringConfig(
           cls.STRING_CONFIG.VALUE_CONFIG,
           config,
           cls.STRING_CONFIG.DISPLAY_IMPL_CLASS
        )

    @classmethod
    def set_value_config(cls, config):
        """
        Set the configuration for computing the value of string representation.

        :param :class:`ValueConfig` config: a configuration object
        """
        cls.STRING_CONFIG = StringConfig(
           config,
           cls.STRING_CONFIG.DISPLAY_CONFIG,
           cls.STRING_CONFIG.DISPLAY_IMPL_CLASS
        )
