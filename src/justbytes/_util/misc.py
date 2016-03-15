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

""" Miscellaneous utilities. """

import itertools

import justbases


def take_until_satisfied(pred, seq):
    """
    Like next(), but yields all values until the first matching value.

    :param bool pred: a predicate, return False if the value is not satisfactory
    :param seq: a sequence of values
    """
    for x in seq:
        if pred(x):
            yield x
            return
        else:
            yield x

def next_or_last(pred, seq, default=None):
    """
    Return the first element that matches the predicate or the last element in
    the seq.

    If seq is empty, return ``default``.

    :param bool pred: a predicate, return False if the value is not satisfactory
    :param seq: a sequence of values
    :param default: returned if seq is empty, default is None
    """
    for x in seq:
        if pred(x):
            return x
    try:
        return x # pylint: disable=undefined-loop-variable
    except NameError:
        return default

def as_single_number(value, config):
    """
    Returns a rational value as a single number according to the
    specified configuration.

    :param Rational value: a numeric value
    :param StrConfig config: how to calculate the value to display

    :returns: the result and its relation to ``value``
    :rtype: Radix * int
    """
    return justbases.Radices.from_rational(
       value,
       config.base,
       config.max_places,
       config.rounding_method
    )

def relation_to_symbol(relation):
    """
    Change a numeric relation to a string symbol.

    :param int relation: the relation

    :returns: a symbol with the right relation to ``relation``
    :rtype: str
    """
    if relation == 0:
        return ''
    elif relation == -1:
        return '>'
    elif relation == 1:
        return '<'
    else:
        assert False # pragma: no cover

def strip_trailing_zeros(value):
    """
    Strip trailing zeros from a list of ints.

    :param value: the value to be stripped
    :type value: list of str

    :returns: list with trailing zeros stripped
    :rtype: list of int
    """
    return list(
       reversed(list(itertools.dropwhile(lambda x: x == 0, reversed(value))))
    )
