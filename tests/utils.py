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

""" Utilities for testing. """
# isort: THIRDPARTY
from hypothesis import strategies

# isort: LOCAL
from justbytes import UNITS, Range

NUMBERS_STRATEGY = strategies.one_of(
    strategies.integers(),
    strategies.fractions().map(lambda x: x.limit_denominator(100)),
)

SIZE_STRATEGY = strategies.builds(
    Range,
    strategies.one_of(NUMBERS_STRATEGY, strategies.builds(str, NUMBERS_STRATEGY)),
    strategies.sampled_from(UNITS()),
)
