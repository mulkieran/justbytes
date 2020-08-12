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

""" Exception types used by the justbytes class. """

# isort: STDLIB
import abc


class RangeError(Exception, metaclass=abc.ABCMeta):
    """ Generic Range error. """


class RangeValueError(RangeError):
    """ Raised when a parameter has an unacceptable value.

        May also be raised when the parameter has an unacceptable type.
    """

    _FMT_STR = "value '%s' for parameter %s is unacceptable"

    def __init__(self, value, param, msg=None):
        """ Initializer.

            :param object value: the value
            :param str param: the parameter
            :param str msg: an explanatory message
        """
        # pylint: disable=super-init-not-called
        self.value = value
        self.param = param
        self.msg = msg

    def __str__(self):
        if self.msg:
            fmt_str = self._FMT_STR + ": %s"
            return fmt_str % (self.value, self.param, self.msg)
        return self._FMT_STR % (self.value, self.param)


class RangeUnsupportedOpError(RangeError, metaclass=abc.ABCMeta):
    """ Error when executing unsupported operation on Range. """


class RangeNonsensicalOpError(RangeUnsupportedOpError, metaclass=abc.ABCMeta):
    """ Error when requesting an operation that doesn't make sense. """


class RangeNonsensicalBinOpValueError(RangeNonsensicalOpError):
    """ Error when requesting a binary operation with a nonsense value. """

    _FMT_STR = "nonsensical value for for %s: '%s'"

    def __init__(self, operator, other):
        """ Initializer.

            :param str operator: the operator
            :param object other: the other argument
        """
        # pylint: disable=super-init-not-called
        self._operator = operator
        self._other = other

    def __str__(self):
        return self._FMT_STR % (self._operator, self._other)


class RangeNonsensicalBinOpError(RangeNonsensicalOpError):
    """ Error when requesting a binary operation that doesn't make sense. """

    _FMT_STR = "nonsensical operand types for %s: 'Range' and '%s'"

    def __init__(self, operator, other):
        """ Initializer.

            :param str operator: the operator
            :param object other: the other argument
        """
        # pylint: disable=super-init-not-called
        self._operator = operator
        self._other = other

    def __str__(self):
        return self._FMT_STR % (self._operator, type(self._other).__name__)


class RangeUnrepresentableResultError(RangeUnsupportedOpError, metaclass=abc.ABCMeta):
    """ Error when requesting an operation that yields units that cannot
        be represented with Range, e.g., when multiplying a Range by a Range.
    """


class RangePowerResultError(RangeUnrepresentableResultError):
    """ Error when requesting an operation that would yield a byte power. """

    def __str__(self):
        return "requested operation result requires non-unit power of bytes"


class RangeFractionalResultError(RangeUnrepresentableResultError):
    """ Error when Range construction is strict. """

    def __str__(self):
        return "requested operation result has a fractional quantity of bytes"
