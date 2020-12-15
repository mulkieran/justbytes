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

""" Special purpose generators. """


def takeuntil(pred, seq):
    """
    Like next(), but yields all values until the first matching value.

    :param bool pred: a predicate, return False if the value is not satisfactory
    :param seq: a sequence of values
    """
    for x in seq:
        yield x
        if pred(x):
            break


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
        return x  # pylint: disable=undefined-loop-variable
    except NameError:
        return default
