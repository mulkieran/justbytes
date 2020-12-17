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

""" Tests for Range initialization. """

# isort: STDLIB
import unittest
from fractions import Fraction

# isort: THIRDPARTY
from hypothesis import given, settings, strategies

# isort: LOCAL
from justbytes import UNITS, Range


class InitializerTestCase(unittest.TestCase):
    """ Test conversions. """

    @given(
        strategies.one_of(
            strategies.integers(),
            strategies.fractions(),
            strategies.builds(
                str, strategies.decimals().filter(lambda x: x.is_finite())
            ),
        ),
        strategies.one_of(
            strategies.sampled_from(UNITS()),
            strategies.builds(Range, strategies.fractions()),
            strategies.fractions(),
        ),
    )
    @settings(max_examples=50)
    def testInitialization(self, s, u):
        """ Test the initializer. """
        factor = getattr(u, "factor", getattr(u, "magnitude", None))
        if factor is None:
            factor = Fraction(u)
        self.assertEqual(Range(s, u).magnitude, Fraction(s) * factor)
