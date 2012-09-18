python-watarray
===============
`python-watarray` is a python wrappers for `wat-array <http://code.google.com/p/wat-array/>`_, a wavelet tree library. 

Requirements
------------

- Python>=2.4
- wat-array==0.06

Install
-------

.. code::

    $ git clone git://github.com/fuzzysphere/python-watarray.git
    $ cd python-watarray 
    $ python setup.py build
    $ python setup.py install

Usage
-----

.. code::

    >>> import watarray
    >>> wa = watarray.WatArray()
    >>> A = [5, 1, 0, 4, 2, 2, 0, 3]
    >>> wa.Init(A)
    >>> wa.length()
    8L
    >>> wa.Lookup(3)
    4L
    >>> wa.Rank(2, 6)
    2L
    >>> wa.Select(2, 2)
    5L
    >>> wa.RankLessThan(4, 5)
    3L
    >>> wa.RankMoreThan(4, 5)
    1L
    >>> wa.FreqRange(2, 5, 2, 6)
    3L
    >>> wa.RankAll(4, 5)
    (1L, 3L, 1L)
    >>> wa.RankAll(7, 5) == (watarray.NOTFOUND, watarray.NOTFOUND, watarray.NOTFOUND)
    True
    >>> wa.MaxRange(1, 6)
    (3L, 4L)
    >>> wa.MinRange(1, 6)
    (2L, 0L)
    >>> wa.QuantileRange(1, 6, 3)
    (4L, 2L)
    >>> wa.ListModeRange(2, 5, 1, 6, 3)
    [(2L, 2L), (4L, 1L)]
    >>> wa.ListMinRange(1, 5, 1, 6, 3)
    [(1L, 1L), (2L, 2L), (4L, 1L)]
    >>> wa.ListMaxRange(1, 5, 1, 6, 3)
    [(4L, 1L), (2L, 2L), (1L, 1L)]
    >>> data = wa.dumps()  
    >>> wa.Clear()
    >>> wa.length()
    0L
    >>> wa.loads(data)
    >>> wa.length()
    8L
    >>> del wa

An instance of `WatArray` has the following methods.

================================================== ===========================================================================================================
Init(A)                                            Create wat-array from A.
length()                                           Return the length of A.
alphabet_num()                                     Return the number of alphabet (max value in A + 1) of A.
Freq(c)                                            Return the number of c in A.
Lookup(pos)                                        Return A[pos].
Rank(c, pos)                                       Return the number of c in A[0:pos].
Select(c, rank)                                    Return the position of the (rank)-th occurence of c in A.
RankLessThan(c, pos)                               Return the number of c' < c in A[0:pos].
RankMoreThan(c, pos)                               Return the number of c' > c in A[0:pos].
FreqRange(min_c, max_c, beg_pos, end_pos)          Return the number of min_c <= c' < max_c in A[beg_pos:end_pos].
MaxRange(beg_pos, end_pos)                         Return the maximum value and its position in A[beg_pos:end_pos].
MinRange(beg_pos, end_pos)                         Return the minimum value and its position in A[beg_pos:end_pos].
QuantileRange(beg_pos, end_pos, k)                 Return the (k+1)-th smallest value and its position in A[beg_pos:end_pos].
ListModeRange(min_c, max_c, beg_pos, end_pos, num) Return the most frequent characters and its frequencies in A[beg_pos:end_pos] and min_c <= c < max_c.
ListMinRange(min_c, max_c, beg_pos, end_pos, num)  Return the characters in ascending order and its frequencies in A[beg_pos:end_pos] and min_c <= c < max_c.
ListMaxRange(min_c, max_c, beg_pos, end_pos, num)  Return the characters in descending order and its frequencies in A[beg_pos:end_pos] and min_c <= c < max_c.
dump(filename)                                     Save the current status to the file.
load(filename)                                     Load the status from the file.
dumps()                                            Return the current status as string.
load(string)                                       Load the status from the string.
================================================== ===========================================================================================================

For MaxRange, MinRange, and QuantileRange, if there are many such positions, return the left most position.
If an argument is invalid, these methods return `watarray.NOTFOUND`.

.. note::

    The descriptions above are based on `documents of wat-array <http://code.google.com/p/wat-array/wiki>`_.

License
-------
Released under the MIT License.
