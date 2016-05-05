.. image:: https://secure.travis-ci.org/mulkieran/justbytes.png?branch=master
   :target: http://travis-ci.org/mulkieran/justbytes

Justbytes
========

Justbytes is a module for handling computation with
address ranges expressed in bytes. Its principle feature is a Range class from
which can be constructed Range objects which represent a precise and finite
address range in bytes. Various arithmetic operations are defined for Range
objects.

Its sole purpose is the representation of real address ranges on real
machines. For that reason, it does not allow powers of ranges, imprecise
ranges, or non-finite ranges. In order that the
usual laws of arithmetic can be maintained, it does allow fractional ranges.


Practical Computing with Address Ranges
---------------------------------------

When computing with address ranges, the numeric value can be viewed as a
logical, rather than a physical, quantity. That is, unlike, e.g., mass or
length, which are quantities which must be measured with a measuring instrument
which has some built-in imprecision, an address range
is a quantity that is not measured, but is known precisely.
This precision arises because the number represents not as much an amount of
memory as a number of addressable, byte-size, locations in memory.

Consequently, computations such as addition of two Ranges, and conversion
between different magnitudes of bytes, i.e., from MiB to GiB, must be done
precisely. The underlying implementation must therefore use a precise
representation of the number of bytes. Floating point numbers, which are
frequently the preferred type for the representation of physical
quantities, are disallowed by this requirement.

Operations
----------
This module does not accomodate multi-dimensionality of address ranges.
Consequently, multiplying one Range object by another Range object will cause
an error to be raised, since bytes^2 is not representable by the module.
For most uses any operation which would yield a multi-dimensional quantity
is not useful. There are no plans to adapt this package so that it
can accomodate multi-dimensionality of address ranges.

Numerous computations with address ranges are nonsensical. For example, 2
raised to a power which is some address range, is a meaningless computation.
All such operations cause an error to be raised.

Some computations with precise, finite, values may yield irrational results.
For example, while 2 is rational, its square root is an irrational number.
There is no allowed operation on Range objects which can result in an
irrational Range value. It turns out that all such operations are either
nonsensical or would result in a value with an unrepresentable type.

The result type of operations is a Range, where appropriate, or a subtype of
Rational, where a numeric value is appropriate.

Floating Point Numbers
----------------------
It is not possible to use floating point numbers in computations with Ranges.
Where a fractional quantity is desired, use Decimal objects instead of floats.
Thus, Range(0) * 1.2 raises an exception, but Range(0) * Decimal("1.2") is
acceptable.

Computing the Representation of a Range
---------------------------------------
The representation of a Range is computed according to a specified
configuration. In the default configuration, the representation uses IEC
rather than SI units.

The representation of a Range is not a string, but a structured representation
of the precise value, as well as the relationship of the representation to
the actual value.

This representation is exposed to clients of the library, which may use it
in any way.

Displaying Ranges
----------------
The Range class also has standard methods for the representation of Range
objects as str objects.

The str representation can also be configured. The manipulation of the
representation to form a str object is abstracted from the rest of the source
to emphasize that clients of the package may choose to represent address ranges
in any manner they choose.

Representing Units
------------------
The size module supplies a set of named prefixes for both SI and binary units,
for all non-fractional prefixes. Fractional prefixes are not defined.

Constructing Ranges Programatically
----------------------------------
New Range objects can be constructed from Range objects, numeric values, e.g.,
int or Decimal, or strings which represent such numeric values.
strings may be used to represent fractional quantities, e.g., "1.2", but
floats are disallowed.

The constructor takes an optional units specifier, which defaults to bytes
for all numeric values, and to None for Range objects. The type of the
unit specifier is a named prefix supplied by the size module or a Range object.

Errors
------
All errors raised by justbytes operations are subtypes of the RangeError class.

Memory Consumption and Bandwidth vs. Address Ranges
---------------------------------------------------
Memory consumption, e.g., by a process during execution on a specified
workload, is a quantity, that like address ranges, is specified in
bytes. However, memory consumption is simply a measurement of the amount of
a phsyical quantity consumed.  When bytes are used only to represent memory
consumption, computations do not generally require the special handling
supplied by this library. Generally, measurement of memory consumption can
be treated like any other physical quantity. The same reasoning applies to
bandwidth. For a physical analogy, one can imagine memory consumption to be
analogous to volume, e.g., litres, and bandwidth to be analogous to flow,
e.g., litres per minute.

User Input
----------
This package does not handle arbitrary user input. It is expected that the
client will transform any input, from whatever source, into a number and an
optional unit specification which can be passed directly to the Range
constructor.

Alternative Packages
--------------------
If you are interested in computing in Python with physical, rather than
logical, quantities, you should consult the pint package:
http://pint.readthedocs.org.
