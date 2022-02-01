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

""" Tests for operations on Range objects. """

# isort: STDLIB
import copy
import unittest

# isort: LOCAL
from justbytes import Range


class ConversionTestCase(unittest.TestCase):
    """Test conversions."""

    def test_bool(self):
        """
        Test conversion to bool.

        Note that bool calls __bool__() in Python 3, __nonzero__ in Python2.
        """
        self.assertFalse(bool(Range(0)))
        self.assertFalse(Range(0).__bool__())

        self.assertTrue(bool(Range(1)))
        self.assertTrue(Range(1).__bool__())

    def test_float(self):
        """
        Test float conversion.

        Converting a Range to a float should require some effort.
        """
        with self.assertRaises(TypeError):
            float(Range(0))

    def test_deep_copy(self):
        """Test that deepcopy is different but equal."""
        size_1 = Range(0)
        size_2 = copy.deepcopy(size_1)
        self.assertEqual(size_1, size_2)
        size_1._magnitude += 1
        self.assertNotEqual(size_1, size_2)
