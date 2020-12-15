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

""" Test for utility functions. """

# isort: STDLIB
import unittest

# isort: THIRDPARTY
from hypothesis import given, settings, strategies

# isort: LOCAL
from justbytes._util.generators import next_or_last, takeuntil


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
            value[0] if value != [] else default,
        )

    @given(strategies.lists(strategies.integers()), strategies.integers())
    @settings(max_examples=10)
    def testResultsFalse(self, value, default):
        """
        Test results when the predicate is always False.
        """
        self.assertEqual(
            next_or_last(lambda x: False, value, default),
            value[-1] if value != [] else default,
        )


class TakeTestCase(unittest.TestCase):
    """
    Test takeuntil.
    """

    @given(strategies.lists(strategies.integers()))
    @settings(max_examples=10)
    def testResultsFalse(self, value):
        """
        Test results when none are sastifactory.
        """
        self.assertEqual(list(takeuntil(lambda x: False, value)), value)

    @given(strategies.lists(strategies.integers()))
    @settings(max_examples=10)
    def testResultsTrue(self, value):
        """
        Test results when all are satisfactory.
        """
        self.assertEqual(list(takeuntil(lambda x: True, value)), value[:1])
