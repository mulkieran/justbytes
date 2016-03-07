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

""" Test for reading from user input. """
from fractions import Fraction

import unittest

from hypothesis import given
from hypothesis import settings

from justbytes import getSizeFromInput
from justbytes import B
from justbytes import InputConfig
from justbytes import ROUND_DOWN
from justbytes import SizeConfig

from .utils import NUMBERS_STRATEGY


class GetSizeFromInputTestCase(unittest.TestCase):
    """
    Test getting size from input.
    """

    def setUp(self):
        self._input_config = SizeConfig.INPUT_CONFIG

    def tearDown(self):
        SizeConfig.set_input_config(self._input_config)

    @given(NUMBERS_STRATEGY)
    @settings(max_examples=5)
    def testRoundingToBytes(self, n):
        """
        Test that it does the proper thing rounding down to bytes.
        """
        SizeConfig.set_input_config(InputConfig(B, ROUND_DOWN))
        res = getSizeFromInput(n)
        self.assertLessEqual(res.magnitude, Fraction(n))
        self.assertEqual(Fraction(res.magnitude).denominator, 1)
