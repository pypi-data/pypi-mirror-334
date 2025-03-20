"""
Biprop - A Python Library for Biproportional Apportionment
==========================================================

Biprop is a python library that allows you to calculate seat distributions of
elections according to various apportionment methods. For further documentation
and examples, refer to the project's GitHub page
'https://github.com/herold-t/biprop'.


Copyright (C) 2025  Talin Herold

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.


Example
-------
This is a basic example demonstrating how you can use this library to calculate
the biproportional apportionment of an election. We will use the same example
as the Wikipedia article
'https://en.wikipedia.org/wiki/Biproportional_apportionment#Specific_example'.
First we create an Election object that defines who got how many votes in the
election

    >>> import biprop as bp
    >>> parties = ['A', 'B', 'C']
    >>> regions = ['I', 'II', 'III']
    >>> votes   = [[123,  45, 815],
    ...            [912, 714, 414],
    ...            [312, 255, 215],]
    >>> e = bp.Election(votes, party_names=parties, region_names=regions)

Now that we have defined the election, we can use biproportional apportionment
to calculate the seat distribution. Since we perform the upper apportionment
according to the Sainte-Laguë method, we need to set `party_seats` and
`region_seats` to `numpy.round`.

    >>> import numpy as np
    >>> seats = e.biproportional_apportionment(total_seats=20,
    ...                 party_seats=np.round, region_seats=np.round)
    Lower apportionment converged after 2 iterations.
    >>> seats
    array([[1, 0, 4],
           [4, 4, 3],
           [2, 1, 1]])

Additional examples can be found on the project's GitHub page
'https://github.com/herold-t/biprop'.

"""
from .biprop import Election, Distribution, InvalidOrderError
__version__     = '1.0.4'
__all__         = ['biprop', 'Election', 'Distribution', 'InvalidOrderError']
__author__      = 'Talin Herold'
__description__ = 'Python library for biproportional and other apportionment methods.'
__copyright__   = 'Copyright (C) 2025 Talin Herold'
__license__     = 'GPL-3.0-or-later'
__title__       = 'biprop'
__url__         = 'https://github.com/herold-t/biprop'