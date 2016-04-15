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

""" Utilities for testing. """
from hypothesis import strategies

from justbytes import Range
from justbytes import UNITS

NUMBERS_STRATEGY = strategies.one_of(
   strategies.integers(),
   strategies.fractions().map(lambda x: x.limit_denominator(100)),
   strategies.decimals().filter(lambda x: x.is_finite()),
)

SIZE_STRATEGY = strategies.builds(
   Range,
   strategies.one_of(
      NUMBERS_STRATEGY,
      strategies.builds(
         str,
         NUMBERS_STRATEGY
      )
   ),
   strategies.sampled_from(UNITS())
)
