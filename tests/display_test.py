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

""" Test for utility functions. """

import unittest

import justbases

from justbytes import DigitsConfig
from justbytes import DisplayConfig
from justbytes import StripConfig

from justbytes._util.display import String

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies


class TestString(unittest.TestCase):
    """
    Test display of Radix given display configuration.
    """

    @given(
       strategies.integers(min_value=2, max_value=1024).flatmap(
          lambda n: strategies.builds(
             justbases.Radix,
             strategies.integers(min_value=1, max_value=1),
             strategies.lists(
                elements=strategies.integers(min_value=0, max_value=n-1),
                min_size=0,
                max_size=10
             ),
             strategies.lists(
                elements=strategies.integers(min_value=0, max_value=n-1),
                min_size=0,
                max_size=10
             ),
             strategies.lists(
                elements=strategies.integers(min_value=0, max_value=n-1),
                min_size=0,
                max_size=10
             ),
             strategies.just(n)
          )
       ),
       strategies.builds(
          DisplayConfig,
          show_approx_str=strategies.booleans(),
          show_base=strategies.booleans(),
          digits_config=strategies.just(DigitsConfig(use_letters=False)),
          strip_config=strategies.just(StripConfig())
       ),
       strategies.integers(min_value=-1, max_value=1)
    )
    @settings(max_examples=100)
    def testFormat(self, radix, display, relation):
        """
        Verify that a xformed string with a repeating part shows that part.
        """
        result = String.xform(radix, display, relation)
        assert (radix.repeating_part != []) == (result[-1] == ")")
