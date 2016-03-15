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

""" Test for configuration classes. """
import unittest

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbytes._config import DisplayConfig
from justbytes._config import InputConfig
from justbytes._config import SizeConfig
from justbytes._config import StrConfig

from justbytes._constants import RoundingMethods
from justbytes._constants import UNITS

from justbytes._errors import SizeValueError


class ConfigTestCase(unittest.TestCase):
    """ Exercise methods of output configuration classes. """
    # pylint: disable=too-few-public-methods

    def testStrConfigObject(self):
        """ Miscellaneous tests for string configuration. """
        self.assertIsInstance(str(SizeConfig.STR_CONFIG), str)

    def testException(self):
        """ Test exceptions. """
        with self.assertRaises(SizeValueError):
            StrConfig(min_value=-1)
        with self.assertRaises(SizeValueError):
            StrConfig(min_value=3.2)
        with self.assertRaises(SizeValueError):
            StrConfig(unit=2)
        with self.assertRaises(SizeValueError):
            StrConfig(base=1)

class InputTestCase(unittest.TestCase):
    """ Exercise methods of input configuration classes. """
    # pylint: disable=too-few-public-methods

    def testInputConfigObject(self):
        """ Miscellaneous tests for input configuration. """
        self.assertIsInstance(str(SizeConfig.INPUT_CONFIG), str)

class SizeTestCase(unittest.TestCase):
    """ Test Size configuration. """
    # pylint: disable=too-few-public-methods

    def setUp(self):
        self.display_config = SizeConfig.DISPLAY_CONFIG
        self.input_config = SizeConfig.INPUT_CONFIG
        self.str_config = SizeConfig.STR_CONFIG

    def tearDown(self):
        SizeConfig.DISPLAY_CONFIG = self.display_config
        SizeConfig.INPUT_CONFIG = self.input_config
        SizeConfig.STR_CONFIG = self.str_config

    @given(
       strategies.builds(
          DisplayConfig,
          show_approx_str=strategies.booleans(),
          strip=strategies.booleans()
       )
    )
    @settings(max_examples=30)
    def testSettingDisplayConfig(self, config):
        """ Test that new str config is the correct one. """
        SizeConfig.set_display_config(config)
        self.assertEqual(str(config), str(SizeConfig.DISPLAY_CONFIG))

    @given(
       strategies.builds(
          StrConfig,
          binary_units=strategies.booleans(),
          max_places=strategies.integers().filter(lambda x: x >= 0),
          min_value=strategies.fractions().filter(lambda x: x >= 0),
          exact_value=strategies.booleans(),
          unit=strategies.sampled_from(UNITS())
       )
    )
    @settings(max_examples=30)
    def testSettingStrConfig(self, config):
        """ Test that new str config is the correct one. """
        SizeConfig.set_str_config(config)
        self.assertEqual(str(config), str(SizeConfig.STR_CONFIG))

    @given(
       strategies.builds(
          InputConfig,
          method=strategies.sampled_from(RoundingMethods.METHODS()),
          unit=strategies.sampled_from(UNITS())
       )
    )
    @settings(max_examples=10)
    def testSettingInputConfig(self, config):
        """ That that new input config is the correct one. """
        SizeConfig.set_input_config(config)
        self.assertEqual(str(config), str(SizeConfig.INPUT_CONFIG))
