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

""" Test for error classes. """
# isort: STDLIB
import unittest

# isort: LOCAL
from justbytes._errors import (
    RangeFractionalResultError,
    RangeNonsensicalBinOpError,
    RangeNonsensicalBinOpValueError,
    RangePowerResultError,
    RangeValueError,
)


class ErrorTestCase(unittest.TestCase):
    """ Exercise methods of error classes. """

    def testRangeValueError(self):
        """ Miscellaneous tests for the method. """
        self.assertIsInstance(str(RangeValueError("junk", "junk", "junk")), str)
        self.assertIsInstance(str(RangeValueError("junk", "junk")), str)

    def testRangeFractionalResultError(self):
        """ Miscellaneous tests for the method. """
        self.assertIsInstance(str(RangeFractionalResultError()), str)

    def testRangeNonsensicalBinOpError(self):
        """ Miscellaneous tests for the method. """
        self.assertIsInstance(str(RangeNonsensicalBinOpError("+", 2)), str)

    def testRangeNonsensicalBinOpValueError(self):
        """ Miscellaneous tests for the method. """
        self.assertIsInstance(str(RangeNonsensicalBinOpValueError("+", 2)), str)

    def testRangePowerResultError(self):
        """ Miscellaneous tests for the method. """
        self.assertIsInstance(str(RangePowerResultError()), str)
