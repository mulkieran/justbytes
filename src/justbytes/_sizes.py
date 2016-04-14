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

""" Class for methods that do not properly belong in the Range class. """

from ._config import RangeConfig

from ._size import Range

def getRangeFromInput(value=0, units=None, config=None):
    """ Get a Range object from an input value and units.

        :param value: a size value, default is 0
        :type value: Range, or any finite numeric type (possibly as str)
        :param units: the units of the size, default is None
        :type units: any of the defined units constants or Range or NoneType
        :param config: configures interpretation of inputs
        :type config: a member of :class:`InputConfig` or NoneType
        :returns: a Range object
        :rtype: :class:`Range`
        :raises RangeValueError: on bad parameters
    """
    config = config or RangeConfig.INPUT_CONFIG

    return Range(value, units).roundTo(config.unit, config.method)

AI = Range(0) # pragma: no cover
