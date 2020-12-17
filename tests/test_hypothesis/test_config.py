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

# isort: THIRDPARTY
from hypothesis import given, settings, strategies

# isort: LOCAL
from justbytes._config import Config, DisplayConfig, ValueConfig
from justbytes._constants import UNITS


class RangeTestCase(unittest.TestCase):
    """ Test Range configuration. """

    # pylint: disable=too-few-public-methods

    def setUp(self):
        self.display_config = Config.STRING_CONFIG.DISPLAY_CONFIG
        self.str_config = Config.STRING_CONFIG.VALUE_CONFIG

    def tearDown(self):
        Config.STRING_CONFIG.DISPLAY_CONFIG = self.display_config
        Config.STRING_CONFIG.VALUE_CONFIG = self.str_config

    @given(strategies.builds(DisplayConfig, show_approx_str=strategies.booleans()))
    @settings(max_examples=30)
    def testSettingDisplayConfig(self, config):
        """ Test that new str config is the correct one. """
        Config.set_display_config(config)
        self.assertEqual(str(config), str(Config.STRING_CONFIG.DISPLAY_CONFIG))

    @given(
        strategies.builds(
            ValueConfig,
            binary_units=strategies.booleans(),
            max_places=strategies.integers().filter(lambda x: x >= 0),
            min_value=strategies.fractions().filter(lambda x: x >= 0),
            exact_value=strategies.booleans(),
            unit=strategies.sampled_from(UNITS()),
        )
    )
    @settings(max_examples=30)
    def testSettingValueConfig(self, config):
        """ Test that new str config is the correct one. """
        Config.set_value_config(config)
        self.assertEqual(str(config), str(Config.STRING_CONFIG.VALUE_CONFIG))
