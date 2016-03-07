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
from fractions import Fraction

import unittest

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbytes._util.misc import get_string_info


class FormatTestCase(unittest.TestCase):
    """ Test formatting. """

    @given(
       strategies.integers(min_value=1),
       strategies.integers(),
       strategies.integers(min_value=0, max_value=5),
       strategies.integers(min_value=0, max_value=5)
    )
    @settings(max_examples=10)
    def testExactness(self, p, q, n, m):
        """ When max_places is not specified and the denominator of
            the value is 2^n * 5^m the result is exact.
        """
        x = Fraction(p * q, p * (2**n * 5**m))
        (exact, sign, left, right) = get_string_info(x, places=None)
        if left != '' or right != '':
            self.assertEqual(sign * Fraction("%s.%s" % (left, right)), x)
        self.assertTrue(exact)
