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
    '8 GiB'

The string representation is configurable through the default configuration
and also by parameters to the getString() method::

    >>> size.getString(SizeConfig.VALUE_CONFIG, SizeConfig.DISPLAY_CONFIG)
    '8 GiB'
    >>> size.getString(SizeConfig.VALUE_CONFIG, DisplayConfig(strip_config=StripConfig(strip_whole=False))) 
    '8.00 GiB'
    >>> size.getString(ValueConfig(min_value=10), SizeConfig.DISPLAY_CONFIG)
    '8192 MiB'

Arithmetic
----------
Various arithmetic operations on Size objects are available::

    >>> str(size * 8)
    '64 GiB'
    >>> str(size * Fraction(1, 2))
    '4 GiB'

Floats and non-numbers like infinity are not allowed in these computations.

Some arithmetic operations work with two Size operands::

    >>> new_size = size + Size(1, KiB)
    >>> str(new_size)
    '> 8.00 GiB'

The symbol '>' is used to indicate that the value is approximate and that the
actual value represented is greater than that displayed. With
the current defaults, only 2 places are allowed after the decimal point,
and so the value can not be shown precisely.

Miscellaneous Examples
----------------------
Sometimes it is desirable to get the components of the string output rather
than the whole string value::

    >>> size.getStringInfo(SizeConfig.VALUE_CONFIG)
    (Radix(True,[8],[0, 0],[],10), 0, GiB)

For information about the Radix type see the justbases package.

getStringInfo() takes the same configuration parameters as getString()::

    >>> size.getStringInfo(ValueConfig(min_value=10))
    (Radix(True,[8, 1, 9, 2],[0, 0],[],10), 0, MiB)

To get an exact representation, set the configuration max_places value to None. ::

    >>> (size / 3).getStringInfo(ValueConfig(max_places=None))
    (Radix(True,[2],[],[6],10), 0, GiB)

The final list indicates the repeating values after the radix.

Round to get whole byte values, if desired::

    >>> (size / 3).roundTo(B, ROUND_DOWN)
    Size(2863311530)

Display in selected units::

    >>> size.getString(ValueConfig(unit=YiB), SizeConfig.DISPLAY_CONFIG)
    '> 0.00 YiB'


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
