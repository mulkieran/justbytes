# Copyright (C) 2016  Red Hat, Inc.
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

""" Handling lists of digits. """

import string

from .._errors import SizeValueError

class Digits(object):
    """
    Transforms digits as ints to corresponding symbols.
    """
    # pylint: disable=too-few-public-methods

    _LOWER_DIGITS = string.digits + string.ascii_lowercase
    _UPPER_DIGITS = string.digits + string.ascii_uppercase

    _MAX_SIZE_BASE_FOR_CHARS = len(string.digits + string.ascii_uppercase)

    @classmethod
    def xform(cls, number, config, base):
        """
        Get a number as a string.

        :param number: a number
        :type number: list of int
        :param DigitsConfig config: configuration for displaying digits
        :param int base: the base in which this number is being represented
        :raises: SizeValueError
        """
        if config.use_letters:
            if base > cls._MAX_SIZE_BASE_FOR_CHARS:
                raise SizeValueError(
                   base,
                   "base",
                   "must be no greater than number of available characters"
                )
            digits = \
               cls._UPPER_DIGITS if config.use_caps else cls._LOWER_DIGITS
            return ''.join(digits[x] for x in number)
        else:
            separator = '' if base <= 10 else config.separator
            return separator.join(str(x) for x in number)
