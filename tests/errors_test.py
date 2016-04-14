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

""" Test for error classes. """
import unittest

from justbytes._errors import RangeFractionalResultError
from justbytes._errors import RangeNonsensicalBinOpError
from justbytes._errors import RangeNonsensicalBinOpValueError
from justbytes._errors import RangePowerResultError
from justbytes._errors import RangeValueError


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
