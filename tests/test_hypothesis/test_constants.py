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

""" Test for constants classes. """
# isort: STDLIB
import unittest

# isort: THIRDPARTY
from hypothesis import given, strategies

# isort: LOCAL
from justbytes._constants import BinaryUnits, DecimalUnits


class ConstantsTestCase(unittest.TestCase):
    """ Exercise methods of constants classes. """

    @given(
        strategies.integers(min_value=0, max_value=BinaryUnits.max_exponent()),
        strategies.integers(min_value=0, max_value=DecimalUnits.max_exponent()),
    )
    def testExpMethod(self, bexp, dexp):
        """ Test extracting unit for a given exponent. """
        self.assertEqual(
            BinaryUnits.unit_for_exp(bexp).factor, BinaryUnits.FACTOR ** bexp
        )
        self.assertEqual(
            DecimalUnits.unit_for_exp(dexp).factor, DecimalUnits.FACTOR ** dexp
        )
