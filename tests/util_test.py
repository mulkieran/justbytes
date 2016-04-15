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

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbytes._util.generators import next_or_last
from justbytes._util.generators import take_until_satisfied


class NextTestCase(unittest.TestCase):
    """
    Test next_or_last.
    """

    @given(strategies.lists(strategies.integers()), strategies.integers())
    @settings(max_examples=10)
    def testResultsTrue(self, value, default):
        """
        Test results when the predicate is always True.
        """
        self.assertEqual(
           next_or_last(lambda x: True, value, default),
           value[0] if value != [] else default
        )

    @given(strategies.lists(strategies.integers()), strategies.integers())
    @settings(max_examples=10)
    def testResultsFalse(self, value, default):
        """
        Test results when the predicate is always False.
        """
        self.assertEqual(
           next_or_last(lambda x: False, value, default),
           value[-1] if value != [] else default
        )


class TakeTestCase(unittest.TestCase):
    """
    Test take_until_satisfied.
    """

    @given(strategies.lists(strategies.integers()))
    @settings(max_examples=10)
    def testResultsFalse(self, value):
        """
        Test results when none are sastifactory.
        """
        self.assertEqual(
           list(take_until_satisfied(lambda x: False, value)),
           value
        )

    @given(strategies.lists(strategies.integers()))
    @settings(max_examples=10)
    def testResultsTrue(self, value):
        """
        Test results when all are satisfactory.
        """
        self.assertEqual(
           list(take_until_satisfied(lambda x: True, value)),
           value[:1]
        )
