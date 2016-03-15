Tutorial
========

Creating
---------------------
Import everything::

    >>> from justbytes import *

Create a Size object from a numeric value and a unit specification::

    >>> size = Size(8, GiB)

Displaying
----------
Display it using the internal representation which shows the number of bytes::

    >>> size
    Size(8589934592)

Display it using the string representation which uses units::

    >>> str(size)
    '8.00 GiB'

The string representation is configurable through the default configuration
and also by parameters to the getString() method::

    >>> size.getString(SizeConfig.STR_CONFIG, SizeConfig.DISPLAY_CONFIG)
    '8.00 GiB'
    >>> size.getString(SizeConfig.STR_CONFIG, DisplayConfig(strip=True))
    '8 GiB'
    >>> size.getString(StrConfig(min_value=10), SizeConfig.DISPLAY_CONFIG)
    '8192.00 MiB'

Arithmetic
----------
Various arithmetic operations on Size objects are available::

    >>> str(size * 8)
    '64.00 GiB'
    >>> str(size * Fraction(1, 2))
    '4.00 GiB'

Floats and non-numbers like infinity are not allowed in these computations.

Some arithmetic operations work with two Size operands::

    >>> new_size = size + Size(1, KiB)
    >>> str(new_size)
    '@8.00 GiB'

The symbol '@' is used to indicate that the value is approximate. With
the current defaults, only 2 places are allowed after the decimal point,
and so the value can not be shown precisely.

Miscellaneous Examples
----------------------
Sometimes it is desirable to get the components of the string output rather
than the whole string value::

    >>> size.getStringInfo(SizeConfig.STR_CONFIG)
    (False, 1, '8', '00', GiB)

getStringInfo() takes the same configuration parameters as getString()::

    >>> size.getStringInfo(StrConfig(min_value=10))
    (False, 1, '8192', '00', MiB)

To get a precise raw representation of a value use getDecimalInfo()::

    >>> size.getDecimalInfo(StrConfig(min_value=10))
    (1, 8192, [], [], MiB)

If the decimal is non-terminating, the repeating string is also shown::

    >>> size / 3
    Size(2863311530.(6))
    >>> (size / 3).getDecimalInfo(SizeConfig.STR_CONFIG)
    (1, 2, [], [6], GiB)

Round to get whole byte values, if desired::

    >>> (size / 3).roundTo(B, ROUND_DOWN)
    Size(2863311530)

Display in selected units::

    >>> size.getString(StrConfig(unit=YiB), SizeConfig.DISPLAY_CONFIG)
    '@0.00 YiB'


Using the Additive Identity
---------------------------

Sum a list of Size objects using the sum method and the additive identity::

    >>> sum([], AI)
    Size(0)

If the additive identity is not specified, there are two possiblities, both
bad:

1. A SizeError exception may be raised::

    >>> l = [Size(32)]
    >>> sum(l)
    Traceback (most recent call last):
    ...

This is due to the fact that addition must be type-correct. Only a Size can be
added to another Size, but the implementation of sum() adds the number 0 to
the elements in the list, resulting in an exception.

2. If the list argument is empty, the result will have the wrong type, int::

    >>> res = sum(l[1:])
    >>> res
    0
    >>> type(res)
    <type 'int'>

Of course, the additive identity is just Size(0)::

    >>> AI
    Size(0)
