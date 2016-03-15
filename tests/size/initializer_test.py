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

""" Tests for Size initialization. """

from decimal import Decimal
from fractions import Fraction

import unittest

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies

from justbytes import B
from justbytes import Size
from justbytes import UNITS

from justbytes._errors import SizeValueError


class InitializerTestCase(unittest.TestCase):
    """ Test conversions. """

    def testExceptions(self):
        """ Test exceptions. """
        with self.assertRaises(SizeValueError):
            Size(1.23)
        with self.assertRaises(SizeValueError):
            Size("1.2.3")
        with self.assertRaises(SizeValueError):
            Size(Decimal('NaN'))

        s = Size(0)
        with self.assertRaises(SizeValueError):
            Size(s, B)

        with self.assertRaises(SizeValueError):
            Size(1, 1.2)

        with self.assertRaises(SizeValueError):
            Size(1, Decimal("NaN"))

    @given(
       strategies.one_of(
          strategies.integers(),
          strategies.fractions(),
          strategies.decimals().filter(lambda x: x.is_finite()),
          strategies.builds(
             str,
             strategies.decimals().filter(lambda x: x.is_finite())
          )
       ),
       strategies.one_of(
          strategies.sampled_from(UNITS()),
          strategies.builds(Size, strategies.fractions()),
          strategies.fractions(),
          strategies.decimals().filter(lambda x: x.is_finite())
       )
    )
    @settings(max_examples=50)
    def testInitialization(self, s, u):
        """ Test the initializer. """
        factor = getattr(u, "factor", getattr(u, "magnitude", None))
        if factor is None:
            factor = Fraction(u)
        self.assertEqual(Size(s, u).magnitude, Fraction(s) * factor)
