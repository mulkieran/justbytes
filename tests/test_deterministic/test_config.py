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

""" Test for configuration classes. """
# isort: STDLIB
import unittest

# isort: LOCAL
from justbytes._config import Config, ValueConfig
from justbytes._errors import RangeValueError


class ConfigTestCase(unittest.TestCase):
    """ Exercise methods of output configuration classes. """

    # pylint: disable=too-few-public-methods

    def testValueConfigObject(self):
        """ Miscellaneous tests for string configuration. """
        self.assertIsInstance(str(Config.STRING_CONFIG.VALUE_CONFIG), str)

    def testException(self):
        """ Test exceptions. """
        with self.assertRaises(RangeValueError):
            ValueConfig(min_value=-1)
        with self.assertRaises(RangeValueError):
            ValueConfig(min_value=3.2)
        with self.assertRaises(RangeValueError):
            ValueConfig(unit=2)
        with self.assertRaises(RangeValueError):
            ValueConfig(base=1)
        with self.assertRaises(RangeValueError):
            ValueConfig(max_places=-1)
