.. image:: https://secure.travis-ci.org/mulkieran/justbytes.png?branch=master
   :target: http://travis-ci.org/mulkieran/justbytes

Justbytes
========

Justbytes is a module for handling computation with
sizes expressed in bytes. Its principle feature is a Size class from
which can be constructed Size objects which represent a precise and finite
quantity of bytes. Various arithmetic operations are defined for Size objects.

Its sole purpose is the representation of real quantities of memory on real
machines. For that reason, it does not allow powers of bytes, imprecise
quantities of bytes, or non-finite quantities of bytes. In order that the
usual laws of arithmetic can be maintained, it does allow fractional quantities
of bytes.

Practical Computing with Bytes
------------------------------

When computing with bytes, the numeric value can be viewed as a logical,
rather than a physical, quantity. That is, unlike, e.g., mass or length,
which are quantities which must be measured with a measuring instrument
which has some built-in imprecision, the number of bytes of memory in RAM,
or on a disk, is a quantity that is not measured, but is known precisely.
This precision arises because the number represents not as much an amount of
memory as a number of addressable, byte-size, locations in memory.

Consequently, computations such as addition of two Sizes, and conversion
between different magnitudes of bytes, i.e., from MiB to GiB, must be done
precisely. The underlying implementation must therefore use a precise
representation of the number of bytes. Floating point numbers, which are
frequently the preferred type for the representation of physical
quantities, are disallowed by this requirement.

Operations
----------
This module does not accomodate multi-dimensionality of byte quantities.
Consequently, multiplying one Size object by another Size object will cause
an error to be raised, since bytes^2 is not representable by the module.
For most uses any operation which would yield a multi-dimensional quantity
of bytes is not useful. There are no plans to adapt this package so that it
can accomodate multi-dimensionality of bytes.

Numerous computations with bytes are nonsensical. For example, 2 raised to a
power which is some number of bytes, is a meaningless computation. All such
operations cause an error to be raised.

Some computations with precise, finite, values may yield irrational results.
For example, while 2 is rational, its square root is an irrational number.
There is no allowed operation on Size objects which can result in an
irrational Size value. It turns out that all such operations are either
nonsensical or would result in a value with an unrepresentable type.

The result type of operations is a Size, where appropriate, or a subtype of
Rational, where a numeric value is appropriate.

Floating Point Numbers
----------------------
It is not possible to use floating point numbers in computations with Sizes.
Where a fractional quantity is desired, use Decimal objects instead of floats.
Thus, Size(0) * 1.2 raises an exception, but Size(0) * Decimal("1.2") is
acceptable.

Displaying Sizes
----------------
Sizes are displayed according to a specified configuration. In the default
configuration, Sizes are displayed using binary rather than SI prefixes
or names, regardless of the value. For example, 1000 bytes is not displayed
as 1KB (1 kilobyte), but as some number of bytes or KiB (kibibytes).

The detailed representation of Sizes uses a precise decimal representation
that includes the repeating portion, if any.

Representing Units
------------------
The size module supplies a set of named prefixes for both SI and binary units,
for all non-fractional prefixes. Fractional prefixes are not defined.

Constructing Sizes Programatically
----------------------------------
New Size objects can be constructed from Size objects, numeric values, e.g.,
int or Decimal, or strings which represent such numeric values.
strings may be used to represent fractional quantities, e.g., "1.2", but
floats are disallowed.

The constructor takes an optional units specifier, which defaults to bytes
for all numeric values, and to None for Size objects. The type of the
unit specifier is a named prefix supplied by the size module or a Size object.

Errors
------
All errors raised by justbytes operations are subtypes of the SizeError class.

Alternative Packages
--------------------
If you are interested in computing in Python with physical, rather than
logical, quantities, you should consult the pint package:
http://pint.readthedocs.org.
