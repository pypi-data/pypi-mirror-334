"""
Biprop is a python library that allows you to calculate seat distributions of
elections according to various apportionment methods.
Copyright (C) 2025  Talin Herold

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.

"""
import numpy as np
from pandas import DataFrame, Series
from pandas.core.indexes.range import RangeIndex



class InvalidOrderError(Exception):
    """
    Methods of Election object were called in an invalid order.

    """
    def __init__(self, *args):
        super().__init__(*args)



class Election():
    """
    The Election class is used to define elections for which we want to calculate
    a seat distribution. An election with `NoP` parties and `NoR` regions consits
    of a `votes`-array with shape `(NoP, NoR)`. `self.votes[i,j]` indicates, how
    many votes the i'th party received in the j'th region.

    Example Usage
    -------------
    This basic example demonstrates how you can use this library to calculate
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
    to calculate the seat distribution. We start with the upper apportionment.
    To assign seats to the parties, we use:

        >>> e.upper_apportionment(total_seats=20, which='parties')
        array([ 5, 11,  4])

    To assign seats to regions, we use:

        >>> e.upper_apportionment(total_seats=20, which='regions')
        array([7, 5, 8])

    Now that we have done the upper apportionment, we can continue with the lower
    apportionment:
        
        >>> seats = e.lower_apportionment()
        Lower apportionment converged after 2 iterations.
        >>> seats
        array([[1, 0, 4],
            [4, 4, 3],
            [2, 1, 1]])

    We can also perform the upper and lower apportionment in a single step using
    `Election.biproportional_apportionment`. To specify to this function that we
    want to perform the upper apportionmnent according to the Saint-Laguë method,
    we set the keyword arguments `party_seats` and `region_seats` to `np.round`.
    (Standard rounding corresponds to the Saint-Laguë method. For more methods
    and their corresponding rounding functions, see
    'https://en.wikipedia.org/wiki/Highest_averages_method#Specific_methods'.)

        >>> import numpy as np
        >>> e2 = bp.Election(votes, party_names=parties, region_names=regions)
        >>> seats2 = e2.biproportional_apportionment(total_seats=20,
        ...                 party_seats=np.round, region_seats=np.round)
        Lower apportionment converged after 2 iterations.
        >>> seats2
        array([[1, 0, 4],
            [4, 4, 3],
            [2, 1, 1]])

    Additional examples can be found on the project's GitHub page
    'https://github.com/herold-t/biprop'.


    """
    def __init__(self, votes, party_names=None, region_names=None,
                 total_seats=None, party_seats=None, region_seats=None):
        """
        Initializes an Election object.

        Prameters
        ---------
        votes : array-like with shape (NoP, NoR)
            The array that indicates which party received how many votes in which
            region. In an election with `NoP` parties and `NoR` regions, `votes`
            must have shape `(NoP, NoR)`. `votes[i,j]` then indicates how many
            votes the i'th party received in the j'th region.
        party_names : list with length NoP or None, optional
            A list of the names of the parties that participate in the election.
            `party_names[i]` must be the name of the party corresponding to the
            i'th row of `self.votes`. The default is None.
        region_names : list with length NoR or None, optional
            A list of the names of the regions in which the the election is held.
            `region_names[j]` must be the name of the region corresponding to the
            j'th column of `self.votes`. The default is None.
        total_seats : int or None, optional
            Indicates how many seats are to be apportioned. Is not required as it
            can also be set when calling the methods that calculate apportionments.
            However, if you use the same Election object to calculate many
            apportionments, passing the total seats once instead of for every
            apportionment individually can make your life easier. The default is None.
        party_seats : array_like with shape (NoP,) or None, optional
            If the amount of seats that each party gets is not defined through the
            votes but rather through some predefined distribution, you can pass this
            distribution here. `party_seats[i]` must be an integer and indicates how
            many seats the i'th party should receive in total. The default is None.
        region_seats : array_like with shape (NoP,) or None, optional
            If the amount of seats that each region gets is not defined through the
            votes but rather through some predefined distribution, you can pass this
            distribution here. `region_seats[j]` must be an integer and indicates how
            many seats the j'th region should receive in total. The default is None.

        Raises
        ------
        ValueError
            Is raised when the passed parameters do not define a valid Election object.

        """
        # initialize important attributes to None
        self._party_names = None
        self._region_names = None
        self._party_seats = None
        self._region_seats = None
        self._votes_offset = 0
        self._mode = 0
        
        # define votes
        self._votes = np.array(votes, dtype=float)
        if len(self._votes.shape) != 2:
            raise ValueError(f'Expected votes be a 2D-array but received a {len(self._votes.shape)}D-array.')
        if type(votes) == DataFrame:
            if type(votes.index) != RangeIndex:
                self.party_names = votes.index
            if type(votes.columns) != RangeIndex:
                self.region_names = votes.columns
        if total_seats == None:
            self._total_seats = None
        else:
            self._total_seats = int(total_seats)
        if party_names != None:
            self.party_names = party_names
        if region_names != None:
            self.region_names = region_names
        self.party_seats = party_seats
        self.region_seats = region_seats
        self._seats = None
        self._distributions = DistDict(self)
    
    @property
    def votes(self):
        return self._votes
    @votes.setter
    def votes(self, new_votes):
        new_votes = np.array(new_votes, dtype=float)
        if new_votes.shape != self.votes.shape:
            raise ValueError(f'You can only assign arrays of shape {self.votes.shape} to `self.votes`.')
        self._votes = new_votes
    
    @property
    def party_names(self):
        return self._party_names
    @party_names.setter
    def party_names(self, new_party_names):
        new_party_names = list(new_party_names)
        if len(new_party_names) != self.votes.shape[0]:
            raise ValueError(f'Cannot assign name list with {len(new_party_names)} parties to election with {self.votes.shape[0]} parties.')
        self._party_names = new_party_names
    @property
    def parties(self):
        return self.party_names
    @parties.setter
    def parties(self, new_parties):
        self.party_names(new_parties)

    @property
    def region_names(self):
        return self._region_names
    @region_names.setter
    def region_names(self, new_region_names):
        new_region_names = list(new_region_names)
        if len(new_region_names) != self.votes.shape[1]:
            raise ValueError(f'Cannot assign name list with {len(new_region_names)} regions to election with {self.votes.shape[1]} regions.')
        self._region_names = new_region_names
    @property
    def regions(self):
        return self.region_names
    @regions.setter
    def regions(self, new_regions):
        self.region_names(new_regions)

    @property
    def party_seats(self):
        return self._party_seats
    @party_seats.setter
    def party_seats(self, new_party_seats):
        if type(new_party_seats) == type(None):
            self._party_seats = None
        else:
            new_party_seats = np.array(new_party_seats, dtype=int).ravel()
            if new_party_seats.shape != (self.votes.shape[0], ):
                raise ValueError(f'Expected `party_seats` to have size {self.NoP} but has size {new_party_seats.size}.')
            new_total = np.sum(new_party_seats)
            if type(self.region_seats) != type(None) and np.sum(self.region_seats)!=new_total:
                raise ValueError(f'Cannot set `party_seats` ({new_total} total seats) as it conflicts with `region_seats` ({np.sum(self.region_seats)} total seats)\n'
                                 +'If you want to use `party_seats` instead of `region_seats`, set `region_seats` to `None` first.')
            if new_total != self.total_seats:
                if self.total_seats != None:
                    print(f'WARNING: Number of seats in `party_seats` ({new_total}) does not match `total_seats` ({self.total_seats}).\n'
                          +'`toal_seats` will be overwritten.')
                self._total_seats = int(new_total)
            self._party_seats = new_party_seats
    
    @property
    def region_seats(self):
        return self._region_seats
    @region_seats.setter
    def region_seats(self, new_region_seats):
        if type(new_region_seats) == type(None):
            self._region_seats = None
        else:
            new_region_seats = np.array(new_region_seats, dtype=int).ravel()
            if new_region_seats.shape != (self.votes.shape[1], ):
                raise ValueError(f'Expected `region_seats` to have size {self.NoR} but has size {new_region_seats.size}.')
            new_total = np.sum(new_region_seats)
            if type(self.party_seats) != type(None) and np.sum(self.party_seats)!=new_total:
                raise ValueError(f'Cannot set `region_seats` ({new_total} total seats) as it conflicts with `party_seats` ({np.sum(self.party_seats)} total seats)\n'
                                 +'If you want to use `region_seats` instead of `party_seats`, set `party_seats` to `None` first.')
            if new_total != self.total_seats:
                if self.total_seats != None:
                    print(f'WARNING: Number of seats in `region_seats` ({new_total}) does not match `total_seats` ({self.total_seats}).\n'
                          +'`toal_seats` will be overwritten.')
                self._total_seats = int(new_total)
            self._region_seats = new_region_seats

    @property
    def seats(self):
        return self._seats
    @property
    def distributions(self):
        return self._distributions
    @property
    def total_votes(self):
        return self.votes.sum() + self._votes_offset
    @property
    def shape(self):
        return self.votes.shape
    @property
    def NoP(self):
        return self.votes.shape[0]
    @property
    def NoR(self):
        return self.votes.shape[1]
    def __sizeof__(self):
        return self.votes.__sizeof__()
    @property
    def mode(self):
        return self._mode
    
    @property
    def total_seats(self):
        return self._total_seats
    @total_seats.setter
    def total_seats(self, new_total_seats):
        if new_total_seats == self.total_seats:
            return
        if type(self.party_seats) != type(None) or type(self.region_seats) != type(None):
            raise ValueError('Can only set `total_seats` while both `region_seats` and `party_seats` are `None`.')
        if new_total_seats == None:
            self._total_seats = None
        else:
            self._total_seats = int(new_total_seats)


    def __repr__(self):
        return f'<Election with {self._votes.shape[0]} parties and {self._votes.shape[1]} regions.>'
    

    def __str__(self):
        lines = self.votes.__repr__()[5:].split('\n')
        s = 'Election' + lines[0]
        for line in lines[1:]:
            s += '\n   ' + line
        return s
    

    def to_dataframe(self):
        """
        Converts `self.votes` to a pandas DataFrame and returns it.
        """
        return DataFrame(self.votes, index=self.parties, columns=self.regions, dtype=float, copy=True)
    

    # TODO: Implement
    def to_excel(self):
        raise NotImplementedError('Will become available in version 1.1.0.')

    
    def upper_apportionment_from_list(self, list_of_dicts, which=None):
        """
        Takes a list where each item corresponds to one region (party). Each item
        should be a dictionary and contain the number of seats of that region (party).
        Uses this list to create an array containing the number of seats every region
        (party) gets and returns that array. Optionally sets the `region_seats`
        (`party_seats`) attributes to the derived array.

        Parameters
        ----------
        list_of_dicts : list
            List containing dictionaries. Every item in that list corresponds to one
            region (party) and must contain a dictionary. That dictionary must have
            the number of seats of the corresponding region stored under the key
            'seats'.
        which : 'regions', 'parties' or None, optional
            Indicates whether the derived array is set as `region_seats` or
            `party_seats` attribute or if it is returned without being set
            (`which=None`). The default is None.

        Returns
        -------
        seats : numpy.ndarray of type int
            Numpy array where `seats[i]` are the seats of the i'th region (party) in
            `list_of_dicts`.

        """
        seats = []
        for item in list_of_dicts:
            seats.append(item['seats'])
        if which == 'regions':
            self.region_seats = seats
            return self.region_seats
        if which == 'parties':
            self.party_seats = seats
            return self.party_seats
        print('WARNING: Returning the seats array without setting the `region_seats` or `party_seats` attribute.')
        return np.array(seats, dtype=int)
    
    
    def upper_apportionment(self, total_seats=None, which='parties',
                            rounding_method=np.round, quorum=None, return_divisor=False,
                            update_seats=True, max_depth=100, scaling=2):
        """
        Uses a divisor method to calculate the upper apportionment, i.e. to assign
        seats to each party (region) according to the total number of votes the party
        received (that were casted in that region). The divisor method that is used is
        determined by the `rounding`-argument. The default divisor method is the
        Sainte-Laguë-method.

        Parameters
        ----------
        votes : array-like, two-dimensional
            2D array where the i'th row corresponds to the votes for the i'th party
            and the j'th column corresponds to the votes casted in the j'th region.
        total_seats : int > 0 or None, optional
            The total number of seats to be assigned. Must be larger than zero. If
            None, `self.total_seats` is used (requires `self.total_seats` to be set)
            as `total_seats`. The default is None.
        which : 'parties' or 'regions', optional
            Determines whether the seats are apportioned to parties or regions. The
            default is 'parties'.
        rounding_method : function, optional
            Rounding function that determines the divisor method. The function needs
            to be able to handle both floats and array-like inputs and needs to round
            them to integers. Use `np.round` for the Sainte-Laguë-method and `np.floor`
            for the D'Hont-method. For other methods, see
            'https://en.wikipedia.org/wiki/Highest_averages_method'.
            The default is `numpy.round`.
        quorum : float, (float, float) or NoneType, optional
            A quorum that a party (region) has to fulfill in order to be eligible for
            seats.
            If `quorum` is a single float, then only parties (regions) that received at
            least that many percent of the total votes are eligible.
            If `quorum` is a tuple of two floats, `(oq, rq)`, then oq defines the
            overall and rq the regional quorum. Parties (regions) that received at
            least `oq` percent of all votes and parties (regions) that received at
            least `rq` percent of at least one region's (party's) votes are both
            eligible.
            If None, no quorum is applied and every party (region) is qualified for
            seats (which does not mean that every party (region) will get one).
            The default is None.
        return_divisor : bool, optional
            If True, the final divisor used for the divisor method is returned. The
            default is False.
        update_seats : bool, optional
            If True, `self.party_seats` (`self.region_seats`) are set to the newly
            calculated upper apportionment before it is returned. The default is True.
        max_depth : int, optional
            The maximum number of recursions before a RecursionError is raised. The
            default is 100.
        scaling : float > 1, optional
            This scaling factor determines how fast the algorithm that finds the
            correct seat distribution converges. Smaller values lead to faster
            convergeance. However, too small values can lead to unstable overshoots
            and might result in the algorithem not converging. `scaling` must always be
            larger than one. The default is 2.

        Raises
        ------
        ValueError
            Is raised when `total_seats` is not positive.
        InvalidOrderError
            Is raised when this method is called after irrelevant parties or regions
            were deleted or grouped together with the `self.sort` or `self.reorder`
            methods.
        RecursionError
            Is raised when the function did not find the correct seat distribution
            after `max_depth` recursions. If this happens, increasing `max_depth`,
            changing `scaling` or changing to a different divisor method (i.e. changing
            the `rounding_method`-function) may help.

        Returns
        -------
        seats: np.ndarray of type int
            A 1D-array where the i'th entry is the total number of seats of the party
            (region) that corresponds to the i'th row (j'th column) of the
            `votes`-array.
        divisor: float (returned only if `return_divisor` is True)
            The divisor used to calculate the seats from the `votes`-array.

        """
        # check and update mode
        if self.mode > 1:
            raise InvalidOrderError('Cannot perform upper apportionment after sorting out irrelevant parties and regions with `self.reorder`.')
        self._mode = max(1, self.mode)
        # copy votes array
        votes = np.array(self.votes, dtype=float)
        # set axis and if which=='regions', transpose votes
        which = which.strip().lower()
        if which=='regions':
            axis = 0
        elif which=='parties':
            axis = 1
        else:
            raise ValueError(f'`which` needs to be "parties" or "regions", not "{which}".')
        # set total_seats and check whether it is positive
        if total_seats == None:
            total_seats = self.total_seats
            if total_seats == None:
                raise ValueError('Can not use `total_seats=None` while `self.total_seats==None`.')
        else:
            total_seats = int(total_seats)
            if total_seats < 1:
                raise ValueError(f"`total_seats` has to be a positive integer but is {total_seats}.")
        # check whether scaling is valid
        if scaling <= 1:
            raise ValueError('`scaling` needs to be strictly larger than one.')
        # modify votes according to quorum
        if type(quorum) != type(None):
            # get quorum-array
            try:
                quorum = np.array([quorum, 200], dtype=float)
            except ValueError:
                quorum = np.array(quorum, dtype=float)
            if which=='regions':
                votes = votes.T
            NoP, NoR = votes.shape
            # get valid_entry array
            valid = np.zeros((NoP, 1))
            # get total (regional) votes
            tot_votes = votes.sum()
            region_votes = votes.sum(axis=0)
            
            # iterate through every party to find the ones that fulfilled the quorum
            for n, party in enumerate(votes):
                # test if party fulfilled national quorum
                if party.sum()/tot_votes >= quorum[0]/100:
                    valid[n,0] = 1
                # otherwise iterate through all regions to test for regional quorum
                else:
                    for m, region_res in enumerate(party):
                        if region_res/region_votes[m] >= quorum[1]/100:
                            valid[n,0] = 1
                            break
            
            # multiply the votes of the disqualified parties by 0
            votes *= valid
            # turn votes back to original shape
            if which=='regions':
                votes = votes.T
        
        # get summed votes and provisional apportionment
        votes = np.array(votes, dtype=float).sum(axis=axis)
        divisor = np.sum(votes)/total_seats
        seats = rounding_method(votes/divisor)
        assigned_seats = np.sum(seats, dtype=int)
        
        # if provisional apportionment does not match requirements, start iteration
        if assigned_seats != total_seats:
            factor = 1
            iteration = 0
            too_low = assigned_seats < total_seats
            
            while True:
                if iteration >= max_depth:
                    raise RecursionError(f"`get_party_seats` did not converge after {iteration} iterations.")
                iteration += 1
                
                # update votes
                divisor *= 1-(total_seats-assigned_seats)/total_seats * factor
                seats = rounding_method(votes/divisor)
                assigned_seats = np.sum(seats, dtype=int)
                
                if assigned_seats == total_seats:
                    break
                elif ((too_low and assigned_seats>total_seats)
                    or (not too_low and assigned_seats<total_seats)):
                    too_low = not too_low
                    factor /= scaling
        
        if update_seats:
            if which == 'regions':
                self.region_seats = seats # implicitly converts float-array to int-array
                seats = self.region_seats # set seats to integer array
            else:
                self.party_seats = seats # implicitly converts float-array to int-array
                seats = self.party_seats # set seats to integer array
        else:
            seats = np.array(seats, dtype=int)
        if return_divisor:
            return seats, divisor
        return seats


    def merge(self, party_mergers=None, region_mergers=None):
        '''
        Merges parties (rows of `self.votes`) and regions (columns of `self.votes`) into
        new parties and regions.

        Parameters
        ----------
        party_mergers : list of lists or NoneType, optional
            Describes which parties (rows of `self.votes`) should be merged. If None,
            no parties are merged. Otherwise, it has to be a list in which every item
            must be a list of parties that are merged. For example, the value
            `party_mergers=[['party1', 'party3'], ['party2', 'party5', 'party6']]`
            merges the parties with names 'party1', and 'party3' into a new party
            called 'party1' and the parties with names 'party2', 'party5', and
            'party6' into a new party called 'party2'. For this to work,
            `self.party_names` must not be None. The newly merged party will have the
            name of the first item in the merger list. This can be used to rename
            (merged) parties. For example, assuming that `self.party_names` does not
            contain 'new_name', `party_mergers[['new_name', 'party1', 'party2']]`
            merges the parties 'party1' and 'party2' into a new party and renames it
            to 'new_name'. The default is None.
        region_mergers : list of lists or NoneType, optional
            Same as `party_mergers`, but for the regions (columns of `self.votes`).
            The default is None.

        Raises
        ------
        ValueError
            Is raised if the `party_mergers` (`region_mergers`) have an invalid value
            or if it is not None while `self.party_names` (`self.region_names`) is
            None.
        InvalidOrderError
            Is raised when this method is called after the first apportionment was
            calculated or after the first distribution was added to
            `self.distributions` or after the irrelevant parties or regions were
            deleted or grouped together with the `self.sort` or `self.reorder` methods.
        TypeError
            Is raised if `party_mergers` or `region_mergers` cannot be converted to a
            list of lists.

        '''
        # check mode
        if self.mode > 0:
            raise InvalidOrderError('Cannot merge parties or regions after the first distribution has been calculated or assigned.')
        # check whether self.party_names and self.region_names are properly set
        if type(party_mergers)!=type(None) and self.party_names==None:
            raise ValueError('Can only merge parties if `self.party_names` is not None.')
        if type(region_mergers)!=type(None) and self.region_names==None:
            raise ValueError('Can only merge regions if `self.region_names` is not None.')
        # check whether party_mergers and region_mergers have right format
        if type(party_mergers)!=type(None):
            try:
                party_mergers = [[party for party in merger] for merger in party_mergers]
            except (TypeError, ValueError):
                raise TypeError('Could not convert `party_mergers` to a list of lists.')
        if type(region_mergers)!=type(None):
            try:
                region_mergers = [[region for region in merger] for merger in region_mergers]
            except (TypeError, ValueError):
                raise TypeError('Could not convert `region_mergers` to a list of lists.')

        # merge parties
        if party_mergers:
            # find new indices
            new_indices = []
            next_index = 0
            merger_indices = [-1 for m in party_mergers]
            for party in self.party_names:
                assigned_index = False
                for m, merger in enumerate(party_mergers):
                    if party in merger:
                        if assigned_index:
                            raise ValueError(f"`party_mergers` must not contain the party '{party}' twice.")
                        if merger_indices[m] < 0:
                            merger_indices[m] = next_index
                            next_index += 1
                        assigned_index = True
                        new_indices.append(merger_indices[m])
                if not assigned_index:
                    new_indices.append(next_index)
                    next_index += 1
            # merge votes and names
            new_votes = np.zeros((next_index, self.NoR), dtype=float)
            new_names = [i for i in range(next_index)]
            for index, row, name in zip(new_indices, self.votes, self.party_names):
                new_votes[index] += row
                new_names[index]  = name
            for merger, index in zip(party_mergers, merger_indices):
                if index >= 0:
                    new_names[index] = merger[0]
            self._votes = new_votes
            self.party_names = new_names
            if type(self.party_seats) != type(None):
                new_seats = [0]*next_index
                for index, seats in zip(new_indices, self.party_seats):
                    new_seats[index] += seats
                self.party_seats = new_seats
        
        # merge regions
        if region_mergers:
            # find new indices
            new_indices = []
            next_index = 0
            merger_indices = [-1 for m in region_mergers]
            for region in self.region_names:
                assigned_index = False
                for m, merger in enumerate(region_mergers):
                    if region in merger:
                        if assigned_index:
                            raise ValueError(f"`region_mergers` must not contain the region '{region}' twice.")
                        if merger_indices[m] < 0:
                            merger_indices[m] = next_index
                            next_index += 1
                        assigned_index = True
                        new_indices.append(merger_indices[m])
                if not assigned_index:
                    new_indices.append(next_index)
                    next_index += 1
            # merge votes and names
            new_votes = np.zeros((self.NoP, next_index), dtype=float)
            new_names = [i for i in range(next_index)]
            for index, row, name in zip(new_indices, self.votes.T, self.region_names):
                new_votes[:, index] += row
                new_names[index]  = name
            for merger, index in zip(region_mergers, merger_indices):
                if index >= 0:
                    new_names[index] = merger[0]
            self._votes = new_votes
            self.region_names = new_names
            if type(self.region_seats) != type(None):
                new_seats = [0]*next_index
                for index, seats in zip(new_indices, self.region_seats):
                    new_seats[index] += seats
                self.region_seats = new_seats
    

    def merge_parties(self, mergers):
        '''
        Merges parties (rows of `self.votes`) into new ones.

        Parameters
        ----------
        mergers : list of lists
            Describes which parties (rows of `self.votes`) should be merged. If None,
            no parties are merged. Otherwise, it has to be a list in which every item
            must be a list of parties that are merged. For example, the value
            `mergers=[['party1', 'party3'], ['party2', 'party5', 'party6']]`
            merges the parties with names 'party1', and 'party3' into a new party
            called 'party1' and the parties with names 'party2', 'party5', and
            'party6' into a new party called 'party2'. For this to work,
            `self.party_names` must not be None. The newly merged party will have the
            name of the first item in the merger list. This can be used to rename
            (merged) parties. For example, assuming that `self.party_names` does not
            contain 'new_name', `mergers[['new_name', 'party1', 'party2']]`
            merges the parties 'party1' and 'party2' into a new party and renames it
            to 'new_name'.

        Raises
        ------
        ValueError
            Is raised if the `party_mergers` have an invalid value or if it is not
            None while `self.party_names` is None.
        TypeError
            Is raised if `party_mergers` cannot be converted to a list of lists.

        '''
        self.merge(party_mergers=mergers)
    

    def merge_regions(self, mergers):
        '''
        Merges regions (columns of `self.votes`) into new ones.

        Parameters
        ----------
        mergers : list of lists
            Describes which regions (columns of `self.votes`) should be merged. If
            None, no regions are merged. Otherwise, it has to be a list in which every
            item must be a list of regions that are merged. For example, the value
            `mergers=[['region1', 'region3'], ['region2', 'region5', 'region6']]`
            merges the regions with names 'region1', and 'region3' into a new region
            called 'region1' and the regions with names 'region2', 'region5', and
            'region6' into a new region called 'region2'. For this to work,
            `self.region_names` must not be None. The newly merged region will have the
            name of the first item in the merger list. This can be used to rename
            (merged) regions. For example, assuming that `self.region_names` does not
            contain 'new_name', `mergers=[['new_name', 'region1', 'region2']]` merges
            the regions 'region1' and 'region2' into a new region and renames it to
            'new_name'.

        Raises
        ------
        ValueError
            Is raised if the `region_mergers` have an invalid value or if it is not
            None while `self.party_names` (`self.region_names`) is None.
        TypeError
            Is raised if `region_mergers` cannot be converted to a list of lists.

        '''
        self.merge(region_mergers=mergers)

    
    def reorder(self, irr_parties=None, party_order=None, other_parties_name='other',
                other_parties_at_end=True, irr_regions=None, region_order=None,
                other_regions_name='other', other_regions_at_end=True):
        """
        This method can reorder the rows and columns of `self.votes`,
        `self.region_names`, `self.party_names`, `self.seats`, and all distributions
        in `self.distributions`. It can also delete rows and columns of parties and
        regions that did not receive any seats to make the arrays more compact.

        Parameters
        ----------
        irr_parties : {'other', 'delete', None}, optional
            Indicates what should be done with irrelevent parties (i.e. parties that
            did not recieve any seats). If 'other', all irrelevant parties are grouped
            together into a new "party" called 'other'. If 'delete', irrelevant parties
            and their rows are deleted. If None, they are kept like all other parties.
            The default is None.
        party_order : list or {'votes', 'seats', 'alphabetical', None}, optional
            This describes the desired new order of the party rows. It can either be
            a list of party names, one of the indicated strings or None.
            If `party_order` is None, the order of the parties is not changed.
            If `party_order` is a list, then `self.party_names` must not be None. In
            this case `party_order[0]` is the name of the party that should be in the
            first row after reordering, `party_order[1]` the name of the party in the
            second row and so on. `party_order` can contain names that are not in
            `party_names`. These names are skipped and do not get a row. `party_order`
            does not have to include all names in `party_names`. Parties that are
            mentioned in `party_names` but not in `party_order` will show up in the
            reordered arrays after the parties in `party_order` and they will have the
            same relative order as before.
            If `party_order` is 'votes', then the parties are ordered by their received
            votes.
            If `party_order` is 'seats', then the parties are ordered by the amount of
            seats they were allocated in all the distributions in `self.distributions`.
            If `party_order` is 'alphabetical', the parties are sorted alphabetically
            by their name. For this, `self.party_names` must not be None.
            The default is None.
        other_parties_name : Any, optional
            The name given to the group of "irrelevant other parties" will have in
            `self.party_names`. The default is 'other'.
        other_parties_at_end : bool, optional
            If true, the group of "irrelevant other parties" always is at the end of
            the reordered list, even if it received more votes than other parties. Only
            has an effect if `irr_parties='other'` and `party_order` is not a list. The
            default is True.
        irr_regions : {'other', 'delete', None}, optional
            Indicates what should be done with irrelevent regions (i.e. regions that
            did not recieve any seats). If 'other', all irrelevant regions are grouped
            together into a new "region" called 'other'. If 'delete', irrelevant
            regions and their columns are deleted. If None, they are kept like all
            other regions. The default is None.
        region_order : list or {'votes', 'seats', 'alphabetical', None}, optional
            Same as `party_order`, but for regions. The default is None.
        other_regions_name : Any, optional
            The name given to the group of "irrelevant other regions" will have in
            `self.region_names`. The default is 'other'.
        other_regions_at_end : bool, optional
            If true, the group of "irrelevant other regions" always is at the end of
            the reordered list, even if it received more votes than other regions. Only
            has an effect if `irr_regions='other'` and `regions_order` is not a list.
            The default is True.

        Raises
        ------
        ValueError
            Is raised when an invalid set of parameters is passed.

        """
        # get shape
        NoP, NoR = self.votes.shape
        # assert that all distributions have the same shape
        for dist in self.distributions.values():
            if dist.seats.shape != (NoP, NoR):
                raise ValueError(f"All distributions in `self.distributions` must have shape {self.votes.shape}.")
        if type(self.seats) == np.ndarray and self.seats.shape != (NoP, NoR):
            raise ValueError(f'`self.seats` must have shape {(NoP, NoR)} but has shape {self.seats.shape}.')
        # canonize irr_parties and irr_regions
        if type(irr_parties) == str:
            irr_parties = irr_parties.strip().lower()
            if irr_parties not in ('other', 'delete'):
                irr_parties = None
        else:
            irr_parties = None
        if type(irr_regions) == str:
            irr_regions = irr_regions.strip().lower()
            if irr_regions not in ('other', 'delete'):
                irr_regions = None
        else:
            irr_regions = None
        # assert that party_names are provided when party_order is a list
        if type(party_order) != type(None):
            if type(party_order) == str:
                party_order = party_order.strip().lower()
                if not party_order in ('votes', 'seats', 'alphabetical'):
                    raise ValueError(f"'{party_order}' is not a valid value for `party_order.`")
                if party_order == 'alphabetical' and self.party_names==None:
                    raise ValueError(f"`self.party_names` cannot be `None` when using `party_order='alphabetical'`.")
            else:
                party_order = list(party_order)
                if self.party_names == None:
                    raise ValueError('When `party_order` is provided and not a string, `self.party_names` cannot be `None`.')
        # assert that region_names are provided when region_order is a list
        if type(region_order) != type(None):
            if type(region_order) == str:
                region_order = region_order.strip().lower()
                if region_order not in ('votes', 'seats', 'alphabetical'):
                    raise ValueError(f"'{region_order}' is not a valid value for `region_order.`")
                if region_order == 'alphabetical' and self.region_names==None:
                    raise ValueError(f"`self.region_names` cannot be `None` when using `region_order='alphabetical'`.")
            else:
                region_order = list(region_order)
                if self.region_names == None:
                    raise ValueError("When `region_order` is provided and not a string, `self.region_names` cannot be `None`.")
        
        # find and delete the irrelevant parties
        irrelevant_parties = []
        if irr_parties:
            relevant_parties = []
            old_total = self.total_votes
            for dist in self.distributions.values():
                for n, party in enumerate(dist.seats):
                    if n not in relevant_parties and np.sum(party)!=0:
                        relevant_parties.append(n)
            if type(self.seats)==np.ndarray:
                for n, party in enumerate(self.seats):
                    if n not in relevant_parties and np.sum(party)!=0:
                        relevant_parties.append(n)
            relevant_parties.sort()
            if (irr_parties == 'delete' and self.NoP > len(relevant_parties)): # change mode if votes are deleted
                self._mode = max(2, self.mode)
            if irr_parties == 'other':
                irrelevant_parties = [i for i in range(NoP) if i not in relevant_parties]
            if irrelevant_parties:
                relevant_parties.append(irrelevant_parties[-1])
                self._mode = max(2, self.mode)
            for dist in self.distributions.values():
                dist._reorder_parties(relevant_parties, irrelevant_parties)
            if type(self.seats) == np.ndarray:
                if irrelevant_parties:
                    for i in irrelevant_parties[:-1]:
                        self.seats[irrelevant_parties[-1]] += self.seats[i]
                self._seats = self.seats[relevant_parties]
            if irrelevant_parties:
                for i in irrelevant_parties[:-1]:
                    self.votes[irrelevant_parties[-1]] += self.votes[i]
            self._votes = self.votes[relevant_parties]
            self._votes_offset += old_total - self.total_votes
            if type(self.party_seats) != type(None):
                if irrelevant_parties:
                    for i in irrelevant_parties[:-1]:
                        self.party_seats[irrelevant_parties[-1]] += self.party_seats[i]
                self.party_seats = self.party_seats[relevant_parties]
            if self.party_names != None:
                new_names = [self.party_names[i] for i in relevant_parties]
                if irrelevant_parties:
                    new_names[-1] = other_parties_name
                self.party_names = new_names
        
        # find and delete the irrelevant regions
        irrelevant_regions = []
        if irr_regions:
            relevant_regions = []
            old_total = self.total_votes
            for dist in self.distributions.values():
                for n, region in enumerate(dist.seats.T):
                    if n not in relevant_regions and np.sum(region)!=0:
                        relevant_regions.append(n)
            if type(self.seats) == np.ndarray:
                for n, region in enumerate(self.seats.T):
                    if n not in relevant_regions and np.sum(region)!=0:
                        relevant_regions.append(n)
            relevant_regions.sort()
            if (irr_regions == 'delete' and self.NoR > len(relevant_regions)): # change mode if votes are deleted
                self._mode = max(2, self.mode)
            if irr_regions == 'other':
                irrelevant_regions = [i for i in range(NoR) if i not in relevant_regions]
            if irrelevant_regions:
                relevant_regions.append(irrelevant_regions[-1])
                self._mode = max(2, self.mode)
            for dist in self.distributions.values():
                dist._reorder_regions(relevant_regions, irrelevant_regions)
            if type(self.seats)==np.ndarray:
                if irrelevant_regions:
                    for i in irrelevant_regions[:-1]:
                        self.seats[:, irrelevant_regions[-1]] += self.seats[:, i]
                self._seats = self.seats[:, relevant_regions]
            if irrelevant_regions:
                for i in irrelevant_regions[:-1]:
                    self.votes[:,irrelevant_regions[-1]] += self.votes[:,i]
            self._votes = self.votes[:, relevant_regions]
            self._votes_offset += old_total - self.total_votes
            if type(self.region_seats) != type(None):
                if irrelevant_regions:
                    for i in irrelevant_regions[:-1]:
                        self.region_seats[irrelevant_regions[-1]] += self.region_seats[i]
                self.region_seats = self.region_seats[relevant_regions]
            if self.region_names != None:
                new_names = [self.region_names[i] for i in relevant_regions]
                if irrelevant_regions:
                    new_names[-1] = other_regions_name
                self.region_names = new_names
        
        # reorder parties according to votes, seats or order-list
        if party_order == 'votes':
            votes = self.votes
            if irrelevant_parties and other_parties_at_end:
                votes = votes.copy()
                votes[-1] *= 0
            new_order = np.argsort(-votes.sum(axis=1), kind='stable')
        elif party_order == 'seats':
            tot_seats = np.zeros_like(self.votes, dtype=int)
            # if type(self.seats)==np.ndarray:
            #     tot_seats += self.seats
            for dist in self.distributions.values():
                tot_seats += dist.seats
            tot_seats = tot_seats.sum(axis=1)
            new_order = np.argsort(-tot_seats, kind='stable')
        elif party_order == 'alphabetical':
            if irrelevant_parties and other_parties_at_end:
                new_order = list(np.argsort(
                            [str(name).lower() for name in self.party_names[:-1]], 
                            kind='stable')) + [-1]
            else:
                new_order = np.argsort(
                            [str(name).lower() for name in self.party_names],
                            kind='stable')
        elif party_order:
            sort_dict = {party: -i for i, party in enumerate(party_order[::-1])}
            def value(party):
                if party in sort_dict:
                    return sort_dict[party]
                else:
                    return 1
            sort_arr = np.array([value(party) for party in self.party_names])
            new_order = np.argsort(sort_arr, kind='stable')
        
        # reorder parties according to new_order
        if party_order:
            for dist in self.distributions.values():
                dist._reorder_parties(new_order)
            if type(self.seats)==np.ndarray:
                self._seats = self.seats[new_order]
            self.votes = self.votes[new_order]
            if type(self.party_seats) != type(None):
                self.party_seats = self.party_seats[new_order]
            if self.party_names != None:
                self.party_names = [self.party_names[i] for i in new_order]
        
        # reorder regions according to votes, seats, or order-list
        if region_order == 'votes':
            votes = self.votes
            if irrelevant_regions and other_regions_at_end:
                votes = votes.copy()
                votes[:, -1] *= 0
            new_order = np.argsort(-votes.sum(axis=0), kind='stable')
        elif region_order == 'seats':
            tot_seats = np.zeros_like(self.votes, dtype=int)
            # if type(self.seats) == np.ndarray:
            #     tot_seats += self.seats
            for dist in self.distributions.values():
                tot_seats += dist.seats
            tot_seats = tot_seats.sum(axis=0)
            new_order = np.argsort(-tot_seats, kind='stable')
        elif region_order == 'alphabetical':
            if irrelevant_regions and other_regions_at_end:
                new_order = list(np.argsort(
                            [str(name).lower() for name in self.region_names[:-1]],
                            kind='stable')) + [-1]
            else:
                new_order = np.argsort(
                            [str(name).lower() for name in self.region_names],
                            kind='stable')
        elif region_order:
            sort_dict = {region: -i for i, region in enumerate(region_order[::-1])}
            def value(region):
                if region in sort_dict:
                    return sort_dict[region]
                else:
                    return 1
            sort_arr = np.array([value(region) for region in self.region_names])
            new_order = np.argsort(sort_arr, kind='stable')
        
        # reorder regions accoring to new_order
        if region_order:
            for dist in self.distributions.values():
                dist._reorder_regions(new_order)
            if type(self.seats)==np.ndarray:
                self._seats = self.seats[:, new_order]
            self.votes = self.votes[:, new_order]
            if type(self.region_seats) != type(None):
                self.region_seats = self.region_seats[new_order]
            if self.region_names != None:
                self.region_names = [self.region_names[i] for i in new_order]


    def sort(self, irr_parties=None, party_order=None, other_parties_name='other',
            other_parties_at_end=True, irr_regions=None, region_order=None,
            other_regions_name='other', other_regions_at_end=True):
        """
        This method can reorder the rows and columns of `self.votes`,
        `self.region_names`, `self.party_names`, `self.seats`, and all distributions
        in `self.distributions`. It can also delete rows and columns of parties and
        regions that did not receive any seats to make the arrays more compact.

        Passes all arguments to `self.reorder`. For full documentation, refer to
        `self.reorder`.

        """
        self.reorder(irr_parties=irr_parties, party_order=party_order,
            other_parties_name=other_parties_name, other_parties_at_end=other_parties_at_end,
            irr_regions=irr_regions, region_order=region_order,
            other_regions_name=other_regions_name, other_regions_at_end=other_regions_at_end)
    

    def reorder_parties(self, irr_parties=None, party_order=None,
                        other_parties_name='other', other_parties_at_end=True):
        """
        This method can reorder the rows of `self.votes`, `self.party_names`,
        `self.seats`, and all distributions in `self.distributions`. It can also delete
        rows of parties that did not receive any seats to make the arrays more compact.

        Parameters
        ----------
        irr_parties : {'other', 'delete', None}, optional
            Indicates what should be done with irrelevent parties (i.e. parties that
            did not recieve any seats). If 'other', all irrelevant parties are grouped
            together into a new "party" called 'other'. If 'delete', irrelevant parties
            and their rows are deleted. If None, they are kept like all other parties.
            The default is None.
        party_order : list or {'votes', 'seats', 'alphabetical', None}, optional
            This describes the desired new order of the party rows. It can either be
            a list of party names, one of the indicated strings or None.
            If `party_order` is None, the order of the parties is not changed.
            If `party_order` is a list, then `self.party_names` must not be None. In
            this case `party_order[0]` is the name of the party that should be in the
            first row after reordering, `party_order[1]` the name of the party in the
            second row and so on. `party_order` can contain names that are not in
            `party_names`. These names are skipped and do not get a row. `party_order`
            does not have to include all names in `party_names`. Parties that are
            mentioned in `party_names` but not in `party_order` will show up in the
            reordered arrays after the parties in `party_order` and they will have the
            same relative order as before.
            If `party_order` is 'votes', then the parties are ordered by their received
            votes.
            If `party_order` is 'seats', then the parties are ordered by the amount of
            seats they were allocated in all the distributions in `self.distributions`.
            If `party_order` is 'alphabetical', the parties are sorted alphabetically
            by their name. For this, `self.party_names` must not be None.
            The default is None.
        other_parties_name : Any, optional
            The name given to the group of "irrelevant other parties" will have in
            `self.party_names`. The default is 'other'.
        other_parties_at_end : bool, optional
            If true, the group of "irrelevant other parties" always is at the end of
            the reordered list, even if it received more votes than other parties. Only
            has an effect if `irr_parties='other'` and `party_order` is not a list. The
            default is True.

        Raises
        ------
        ValueError
            Is raised when an invalid set of parameters is passed.

        """
        self.reorder(irr_parties=irr_parties, party_order=party_order,
            other_parties_name=other_parties_name,
            other_parties_at_end=other_parties_at_end)
    
    
    def sort_parties(self, irr_parties=None, party_order=None,
                    other_parties_name='other', other_parties_at_end=True):
        """
        This method can reorder the rows of `self.votes`, `self.party_names`,
        `self.seats`, and all distributions in `self.distributions`. It can also delete
        rows of parties that did not receive any seats to make the arrays more compact.

        Passes all arguments to `self.reorder_parties`. For full documentation, refer
        to `self.reorder_parties`.

        """
        self.reorder_parties(irr_parties=irr_parties, parties_order=party_order,
            other_parties_name=other_parties_name, other_parties_at_end=other_parties_at_end)
    

    def reorder_regions(self, irr_regions=None, region_order=None,
                        other_regions_name='other', other_regions_at_end=True):
        """
        This method can reorder the columns of `self.votes`, `self.region_names`,
        `self.seats`, and all distributions in `self.distributions`. It can also delete
        columns of regions that did not receive any seats to make the arrays more
        compact.

        Parameters
        ----------
        irr_regions : {'other', 'delete', None}, optional
            Indicates what should be done with irrelevent regions (i.e. regions that
            did not recieve any seats). If 'other', all irrelevant regions are grouped
            together into a new "region" called 'other'. If 'delete', irrelevant
            regions and their columns are deleted. If None, they are kept like all
            other regions. The default is None.
        region_order : list or {'votes', 'seats', 'alphabetical', None}, optional
            This describes the desired new order of the region columns. It can either
            be a list of region names, one of the indicated strings or None.
            If `region_order` is None, the order of the regions is not changed.
            If `region_order` is a list, then `self.region_names` must not be None. In
            this case `region_order[0]` is the name of the region that should be in the
            first column after reordering, `region_order[1]` the name of the region in
            the second column and so on. `region_order` can contain names that are not
            in `region_names`. These names are skipped and do not get a column.
            `region_order` does not have to include all names in `region_names`.
            Regions that are mentioned in `region_names` but not in `region_order` will
            show up in the reordered arrays after the regions in `region_order` and
            they will have the same relative order as before.
            If `region_order` is 'votes', then the regionss are ordered by the votes
            casted in them.
            If `region_order` is 'seats', then the regionss are ordered by the amount
            of seats they were allocated in all the distributions in
            `self.distributions`.
            If `region_order` is 'alphabetical', the regions are sorted alphabetically
            by their name. For this, `self.region_names` must not be None.
            The default is None.
        other_regions_name : Any, optional
            The name given to the group of "irrelevant other regions" will have in
            `self.region_names`. The default is 'other'.
        other_regions_at_end : bool, optional
            If true, the group of "irrelevant other regions" always is at the end of
            the reordered list, even if it received more votes than other regions. Only
            has an effect if `irr_regions='other'` and `regions_order` is not a list.
            The default is True.

        Raises
        ------
        ValueError
            Is raised when an invalid set of parameters is passed.
        
        """
        self.reorder(irr_regions=irr_regions, region_order=region_order,
            other_regions_name=other_regions_name, other_regions_at_end=other_regions_at_end)
    

    def sort_regions(self, irr_regions=None, region_order=None,
                     other_regions_name='other', other_regions_at_end=True):
        """
        This method can reorder the columns of `self.votes`, `self.region_names`,
        `self.seats`, and all distributions in `self.distributions`. It can also delete
        columns of regions that did not receive any seats to make the arrays more
        compact.

        Passes all arguments to `self.reorder_regions`. For full documentation, refer
        to `self.reorder_regions`.

        """
        self.reorder_regions(irr_regions=irr_regions, region_order=region_order,
            other_regions_name=other_regions_name, other_regions_at_end=other_regions_at_end)


    def add_distribution(self, key, seats, **kwargs):
        """
        Creates a Distribution object and adds it to the `self.distibutions`
        dictionary.

        Parameters
        ----------
        key : str
            The key that is used to store the distribution in the `self.distributions`
            dictionary.
        seats : array-like
            Array that describes which party received how many seats in which region.
            Must have the same shape as `self.votes`.
        kwargs
            Keyword arguments that are passed to the `Distribution.__init__`-function.
            Refer to the documentation of that function for mor information about
            possible keyword arguments.
        
        Returns
        -------
        dist : Distribution
            The created Distribution object.

        """
        dist = Distribution(seats, self, **kwargs)
        # we do not need to update the mode here since the DistDict does this for us
        self.distributions[key] = dist
        return dist
    

    # TODO: Implement
    def protected_winner_rounding(self, rounding=np.round, which='parties'):
        raise NotImplementedError('Will become available in version 1.1.0')


    def _get_row_divisors(self, seats, row_divisors=None, column_divisors=None,
                          rounding_method=np.round, max_depth=100, scaling=2,
                          eps=1e-6):
        """
        Finds and returns row divisors for a votes-array such that the total number
        of seats of the i'th row corresponds to the i'th item of `seats`.
        
        """
        # define row and column vectors
        NoR, NoC = self.votes.shape
        if type(column_divisors) == type(None):
            column_divisors = np.ones((1, NoC), dtype=float)
        if type(row_divisors) == type(None):
            row_divisors = np.ones((NoR, 1))
        
        # get provision number of seats
        current_seats = rounding_method(self.votes/column_divisors/row_divisors)
        current_row_tot = current_seats.sum(axis=1)
        
        # if provisional number of seats does not match requirements, start iteration
        if np.any(current_row_tot != seats):
            factor = np.ones_like(current_row_tot)
            iteration = 0
            too_low = current_row_tot < seats
            
            while True:
                if iteration >= max_depth:
                    # print(factor)
                    raise RecursionError(f"`get_row_divisors` did not converge after {iteration} iterations.")
                iteration += 1
                
                # get a better guess for row_divisors
                row_divisors *= 1 + ((current_row_tot-seats)/(seats+eps)
                                    * factor).reshape(row_divisors.shape)
                
                # update provisionally assigned seats
                current_seats = rounding_method(self.votes/column_divisors/row_divisors)
                current_row_tot = current_seats.sum(axis=1)
                
                # if provisional seats match requirements, break
                if np.all(current_row_tot == seats):
                    break
                
                # update factor if an over-/undershoot happened
                factor = np.where(((current_row_tot>seats) & too_low)
                                | ((current_row_tot<seats) & (~too_low)),
                                factor/scaling, factor)
                too_low = current_row_tot < seats

        return current_seats, row_divisors


    def _get_column_divisors(self, seats, row_divisors=None, column_divisors=None,
                             rounding_method=np.round, max_depth=100, scaling=2,
                             eps=1e-6):
        """
        Finds and returns row divisors for a votes-array such that the total number
        of seats of the j'th column corresponds to the j'th item of `seats`.
        
        """
        # redefine rounding method such that it can handle votes.T as input
        new_rounding_method = lambda v: rounding_method(v.T).T
        # transpose arrays to transform the column-problem into a row-problem, then
        # call __get_row_divisors__()
        if type(row_divisors) == np.ndarray:
            row_divisors = row_divisors.T
        if type(column_divisors) == np.ndarray:
            column_divisors = column_divisors.T
        self._votes = self._votes.T
        try:
            current_seats, row_divisors = self._get_row_divisors(
                seats, column_divisors, row_divisors, new_rounding_method,
                max_depth, scaling, eps)
        except:
            self._votes = self._votes.T
            raise
        self._votes = self._votes.T
        # transpose arrays again to revert them and return them
        return current_seats.T, row_divisors.T
    

    def _lower_apportionment(self, party_seats=None, region_seats=None,
                rounding_method=np.round, max_depth=100, scaling=2, eps=1e-6):
        """
        Calculates the lower apportionment and creates and returns a the apportioned
        seats, party divisors and region divisors as arrays. For further information,
        refer to `self.lower_apportionment`.

        """
        # check and update mode
        if self.mode > 1:
            raise InvalidOrderError('Cannot calculate apportionments after `self.reorder` identified irrelevant parties and regions.')
        self._mode = max(1, self.mode)
        # convert arguments into numpy arrays
        if type(party_seats) != type(None):
            party_seats = np.array(party_seats, dtype=int)
        elif type(self.party_seats) == type(None):
            raise ValueError('The `party_seats` argument cannot be none while `self.party_seats` is None.')
        else:
            party_seats = self.party_seats
        if type(region_seats) != type(None):
            region_seats = np.array(region_seats, dtype=int)
        elif type(self.region_seats) == type(None):
            raise ValueError('The `region_seats` argument cannot be none while `self.region_seats` is None.')
        else:
            region_seats = self.region_seats
        
        # test that arguments have the right shapes and format
        if len(self.votes.shape) != 2:
            raise ValueError(f"`self.votes` has the wrong dimension ({len(self.votes.shape)} instead of 2).")
        NoP, NoC = self.votes.shape
        if party_seats.shape != (NoP,):
            raise ValueError(f"'party_seats' has shape {party_seats.shape} but needs shape {(NoP,)}.")
        if region_seats.shape != (NoC,):
            raise ValueError(f"'region_seats' has shape {region_seats.shape} but needs shape {(NoC,)}.")
        if party_seats.sum() != region_seats.sum():
            raise ValueError("`party_seats` and `region_seats` must have the same total number of seats.")
        if scaling <= 1:
            raise ValueError('The `scaling` argument must be a float strictly larger than 1.')
        
        # get inital estimate for the divisors and seats
        # party_divisors = np.sqrt((votes.sum(axis=1)/(party_seats+eps)).reshape((NoP, 1))/2)
        region_divisors = (self.votes.sum(axis=0)/(region_seats+eps)).reshape((1, NoC))
        party_divisors = np.ones((NoP, 1))
        # region_divisors = np.ones((1, NoC))
        # get provisional number of seats
        seats = rounding_method(self.votes/party_divisors/region_divisors)
        
        # calculate assigned party and region seats
        assigned_party_seats = seats.sum(axis=1)
        assigned_region_seats = seats.sum(axis=0)
        
        # if provisional seats do not match the requirements, start iterative process
        if (np.any(assigned_party_seats!=party_seats)
            or np.any(assigned_region_seats!=region_seats)):
            iteration = 0
            while True:
                if iteration >= max_depth: # stop and raise error after max_depth iterations
                    raise RecursionError(f"`lower_apportionment` did not converge after {iteration} iterations.")
                iteration += 1
                
                # update region_divisors
                seats, region_divisors = self._get_column_divisors(
                    region_seats, party_divisors, region_divisors,
                    rounding_method, max_depth, scaling, eps)
                
                # update assigned seats
                assigned_party_seats = seats.sum(axis=1)
                assigned_region_seats = seats.sum(axis=0)
                
                # if seats matches the requirements, break
                if (np.all(assigned_party_seats == party_seats)
                    and np.all(assigned_region_seats == region_seats)):
                    break
                
                # update party_divisors
                seats, party_divisors = self._get_row_divisors(
                    party_seats, party_divisors, region_divisors,
                    rounding_method, max_depth, scaling, eps)
                
                # update assigned seats
                assigned_party_seats = seats.sum(axis=1)
                assigned_region_seats = seats.sum(axis=0)
                
                # if seats matches the requirements, break
                if (np.all(assigned_party_seats == party_seats)
                    and np.all(assigned_region_seats == region_seats)):
                    break
            print(f'Lower apportionment converged after {iteration} iterations.')
        
        # return seats and divisors
        return np.array(seats, dtype=int), party_divisors, region_divisors
    

    def lower_apportionment(self, party_seats=None, region_seats=None, rounding_method=np.round,
                key='Biproportional Apportionment', return_distribution=False, max_depth=100,
                scaling=2, eps=1e-6, **kwargs):
        """
        Calculates the lower apportionment. The function returns an array containing
        the number of seats each party gets in each region. This array is chosen such
        that the total number of seats each party gets is equal to the `party_seats`-
        array and the total number of seats each region gets is equal to the
        `region_seats`-array.

        Parameters
        ----------
        party_seats: None or array-like with shape `(number_of_parties,)`, optional
            Upper apportionment to the parties. Must be a 1D-array where the i'th entry
            is the total number of seats of the party that corresponds to the i'th row
            of `self.votes`. If None, `self.party_seats` is used as upper apportionment
            to the parties (in this case, `self.party_seats` must not be None). The
            default is None.
        region_seats: None or array-like with shape `(number_of_regions,)`, optional
            Upper apportionment to the regions. Must be a 1D-array where the j'th entry
            is the total number of seats of the region that corresponds to the j'th
            column of `self.votes`. If None, `self.region_seats` is used as upper
            apportionment to the regions (in this case, `self.region_seats` must not be
            None). The default is None.
        rounding_method : function, optional
            Rounding function that determines the divisor method. The function needs
            to be able to handle array-like inputs and needs to round them to integers.
            The argument of `rounding_method` is always an array with the same shape
            like `self.votes`. This means that one can use this to implement a rounding
            method that never rounds certain parties in certain regions to zero. This
            is neccessary for a Grisons-like apportionment method where the strongest
            party in each region is guaranteed to win at least one seat in that region.
            Use `np.round` for the Sainte-Laguë-method and `np.floor` for the D'Hont-
            method. For other methods, see
            'https://en.wikipedia.org/wiki/Highest_averages_method'.
            The default is `numpy.round`.
        key : str, optional
            The key that the distribution will have in the `self.distributions`
            dictionary. The default is 'Biproportional Apportionment'.
        return_distribution : bool, optional
            If true, the function returns a Distribution object. Otherwise it just
            returns the seats array. The default is False.
        max_depth : int, optional
            Maximum number of recursions before a RecursionError is raised. Note that
            in a worst-case scenario, the maximum runtime of this function is
            proportional to `max_depth**2`. The default is 100.
        scaling : float > 1, optional
            This scaling factor determines how fast the algorithm that finds the
            correct seat distribution converges. Smaller values lead to faster
            convergeance. However, too small values can lead to unstable overshoots
            and might result in the algorithem not converging. `scaling` must always be
            larger than one. The default is 2.
        eps : float, optional
            Small value to avoid ZeroDivisionErrors. The default is 1e-6.
        **kwargs :
            Optional keyword arguments that are passed to the Distribution-constructor.
            Can be used to add custom attributes to the created Distribution object.

        Raises
        ------
        ValueError
            Is raised when the dimensions of the input-arrays do not match up or if
            the number of seats in `party_seats` and `region_seats` do not match.
        RecursionError
            Is raised when the algorithm did not converge after `max_depth` iterations.

        Returns
        -------
        seats : numpy.ndarray of type int
            Array containing the number of seats each party gets in each region. The
            array has the same shape as `self.votes`. `seats[i,j]` is the number of
            seats that the i'th party gets in the j'th region. Only returned if
            `return_distribution == False`.
        distribution : Distribution
            Distribution object corresponding to the calculated distribution. Only
            returned if `return_distributions == True`.
        
        """
        seats, pdiv, rdiv = self._lower_apportionment(party_seats=party_seats,
                                region_seats=region_seats, rounding_method=rounding_method,
                                max_depth=max_depth, scaling=scaling, eps=eps)
        self._seats = seats
        dist = Distribution(seats, self, method='Biproportional Apportionment',
                    region_divisors=rdiv, party_divisors=pdiv, rounding=rounding_method, **kwargs)
        self.distributions[key] = dist
        if return_distribution:
            return dist
        else:
            return self.seats

    
    def biproportional_apportionment(self, party_seats=None, party_quorum=None, region_seats=None,
            region_quorum=None, total_seats=None, rounding_method=np.round, key='Biproportional Apportionment',
            return_distribution=False, max_depth=100, scaling=2, eps=1e-6, **kwargs):
        """
        Uses the biproportional apportionment to assign each party and region seats
        according to `self.votes`.

        Parameters
        ----------
        party_seats: array-like, function or None
            Defines the upper apportionment to parties. Can either be array-like, a
            function or None.
            A 1D-array where the i'th entry is the total number of seats of the party
            that corresponds to the i'th row of `self.votes`.
            If a function, it will define a divisor method that calculates the number
            of seats each party gets from `self.votes`. It has to be a function that
            rounds (arrays of) foats to (arrays) of integers. You can use `numpy.round`
            for the Saint-Laguë-method, `numpy.floor` for the D'Hont-method or any
            other rounding function.
            If None, the upper apportionment from `self.party_seats` is used.
            The default is None.
        party_quorum: float, (float, float) or NoneType, optional
            A quorum that a party has to fulfill in order to be eligible for seats.
            If `party_quorum` is a single float, then only parties that received at
            least that many percent of the total votes are eligible.
            If `party_quorum` is a tuple of two floats, `(oq, rq)`, then oq defines the
            overall and rq the regional quorum. Parties that received at least `oq`
            percent of all votes and parties that received at least `rq` percent of at
            least one region's votes are both eligible.
            Only has an effect if `party_seats` is a function.
            If None, no quorum is applied and every party is qualified for seats (which
            does not mean that every party will get one). The default is None.
        region_seats: array-like, function or None
            Same as `party_seats`, but for the regions. The default is None.
        region_quorum: float, (float, float) or NoneType, optional
            Same as `party_quorum`, but for the regions. The default is None.
        total_seats: int or NoneType, optional
            The total number of seats in the parliament. Must be provided if both
            `party_seats` and `region_seats` are functions and `self.total_seats` is
            None. The default is None.
        rounding_method : function, optional
            Rounding function that determines the divisor method of the lower
            apportionment. The function needs to be able to handle array-like inputs
            and needs to round them to integers. The argument of `rounding_method` is
            always an array with the same shape like `votes`. This means that one can
            use this to implement a rounding method that never rounds certain parties
            in certain cantos to zero. This is neccessary for a Grisons-like
            apportionment method where the strongest party in each region is guaranteed
            to win at least one seat in that region. Use `np.round` for the Sainte-
            Laguë-method and `np.floor` for the D'Hont-method. For other methods, see
            https://en.wikipedia.org/wiki/Highest_averages_method.
            The default is `numpy.round`.
        key : str, optional
            The key that the distribution will have in the `self.distributions`
            dictionary. The default is 'Biproportional Apportionment'.
        return_distribution : bool, optional
            If true, the function returns a Distribution object. Otherwise it just
            returns the seats array. The default is False.
        max_depth : int, optional
            Maximum number of recursions before a RecursionError is raised. Note that
            in a worst-case scenario, the maximum runtime of this function is
            proportional to `max_depth**2`. The default is 100.
        scaling : float > 1, optional
            This scaling factor determines how fast the algorithm that finds the
            correct seat distribution converges. Smaller values lead to faster
            convergeance. However, too small values can lead to unstable overshoots
            and might result in the algorithem not converging. `scaling` must always be
            larger than one. The default is 2.
        eps : float, optional
            Small value to avoid ZeroDivisionErrors. The default is 1e-6.
        **kwargs :
            Optional keyword arguments that are passed to the Distribution-constructor.
            Can be used to add custom attributes to the created Distribution object.

        Raises
        ------
        ValueError
            Is raised if the shape of the input arrays do not match or if
            `party_seats`, `region_seats` and `total_seats` define a different number
            of total seats.
        InvalidOrderError
            Is raised when this method is called after irrelevant parties or regions
            were deleted or grouped together with the `self.sort` or `self.reorder`
            methods.
        RecursionError
            Is raised when the algorithm did not converge after `max_depth` iterations.

        Returns
        -------
        seats : numpy.ndarray of type int
            Array containing the number of seats each party gets in each region. The
            array has the same shape as `self.votes`. `seats[i,j]` is the number of
            seats that the i'th party gets in the j'th region. Only returned if
            `return_distribution == False`.
        distribution : Distribution
            Distribution object corresponding to the calculated distribution. Only
            returned if `return_distributions == True`.

        """
        # check and update mode
        if self.mode > 1:
            raise InvalidOrderError('Cannot calculate apportionments after `self.reorder` identified irrelevant parties and regions.')
        self._mode = max(1, self.mode)
        # deal with party_seats=None and region_seats=None
        if type(party_seats) == type(None):
            party_seats = self.party_seats
            if type(party_seats) == type(None):
                raise ValueError('Cannot use `party_seats=None` while `self.party_seats==None`.')
        if type(region_seats) == type(None):
            region_seats = self.region_seats
            if type(region_seats) == type(None):
                raise ValueError('Cannot use `region_seats=None` while `self.region_seats==None`.')

        NoP, NoR = self.shape
        tot_seats_assigned = total_seats != None
        
        # convert variables to correct data type and infer implicit varaibles
        if type(party_seats) in (list, set, np.ndarray, Series, DataFrame):
            party_seats = np.array(party_seats, dtype=int)
            tot_party_seats = party_seats.sum()
            if tot_seats_assigned and tot_party_seats!=total_seats:
                raise ValueError(f"Expected a total of {total_seats} in `party_seats` but got {tot_party_seats} seats.")
            elif not tot_seats_assigned:
                tot_seats_assigned = True
                total_seats = tot_party_seats
            if party_seats.shape != (NoP,):
                raise ValueError(f"`party_seats` needs to have shape {(NoP,)} but has shape {party_seats.shape}.")
        
        if type(region_seats) in (list, set, np.ndarray, Series, DataFrame):
            region_seats = np.array(region_seats, dtype=int)
            tot_region_seats = region_seats.sum()
            if tot_seats_assigned and tot_region_seats!=total_seats:
                raise ValueError(f"Expected a total of {total_seats} in `region_seats` but got {tot_region_seats} seats.")
            elif not tot_seats_assigned:
                tot_seats_assigned = True
                total_seats = tot_region_seats
            if region_seats.shape != (NoR,):
                raise ValueError(f"`region_seats` needs to have shape {(NoR,)} but has shape {region_seats.shape}.")
        
        if not tot_seats_assigned and self.total_seats==None:
            raise ValueError( "The total number of seats is not defined. It must be provided in either\n"
                            +"`party_seats`, `region_seats`, `total_seats` or `self.total_seats`.")
        elif not tot_seats_assigned:
            total_seats = self.total_seats
        
        if type(party_seats) != np.ndarray:
            party_seats, updiv = self.upper_apportionment(total_seats,
                    which='parties', quorum=party_quorum, rounding_method=party_seats,
                    max_depth=max_depth, scaling=scaling, return_divisor=True,
                    update_seats=False)
            party_rounding = party_seats
        else:
            party_rounding = 'Predefined Apportionment'
            updiv = None
        
        if type(region_seats) != np.ndarray:
            region_seats, urdiv = self.upper_apportionment(total_seats,
                    which='regions', quorum=region_quorum, rounding_method=region_seats,
                    max_depth=max_depth, scaling=scaling, return_divisor=True,
                    update_seats=False)
            region_rounding = region_seats
        else:
            region_rounding = 'Predefined Apportionment'
            urdiv = None
        
        seats, pdiv, rdiv = self._lower_apportionment(party_seats=party_seats,
                                region_seats=region_seats, rounding_method=rounding_method,
                                max_depth=max_depth, scaling=scaling, eps=eps)
        self._seats = seats
        dist = Distribution(seats, self, method='Biproportional Apportionment',
                    party_divisors=pdiv, region_divisors=rdiv, upper_party_divisor=updiv,
                    upper_region_divisor=urdiv, rounding=rounding_method,
                    party_rounding=party_rounding, region_rounding=region_rounding, **kwargs)
        self.distributions[key] = dist
        if return_distribution:
            return dist
        else:
            return self.seats


    def proportional_apportionment(self, seats=None, which='parties',
                rounding_method=np.round, key='Proportional Apportionment',
                return_distribution=False, max_depth=100, scaling=2, eps=1e-6, **kwargs):
        """
        This function takes the votes of each party (region) in each region (party) and
        allocates the seats in each region (party) seperately to the parties (regions)
        using a divisor method. Since the allocations in the diffenrent regions
        (parties) are independent of each other, proportionality between the number of
        votes and seats each party (region) received is not guaranteed. Thus, this
        apportionment method is not a type of biproportional apportionment.

        Parameters
        ----------
        seats : array-like or int or NoneType, optional
            If `which=='region'`, `seats` must be an array containing the total number
            of seats of each region and must have shape `(1, number_of_regions)` or
            `(number_of_regions,)`.
            If `which=='party'`, `seats` must be an array containing the total number
            of seats of each party and must have shape `(number_of_parties, 1)` or
            `(number_of_parties,)`
            If `which=='total'`, `seats` is the total number of seats and must be a
            positive integer.
            If None, `seats` is inferred from `self`. This requires that, depending on
            the value of `which`, either `self.region_seats`, `self.party_seats` or
            `self.total_seats` is not None.
            The default is None
        which : 'parties', 'regions' or 'both', optional
            Indicates whose seats are not yet known and to be apportioned.
            If `which` is 'parties', then the number of seats of each region has to be
            known and the seats are allocated to the parties.
            If `which` is 'regions', the number of seats of each party has to be known
            and the seats are allocated to the regions.
            If `which` is 'both', then only the total number of seats has to be known
            and the seats are allocated to both the parties and the regions.
            The default is 'parties'.
        rounding_method : function, optional
            Rounding function that determines the divisor method of the apportionment.
            The function needs to be able to handle array-like inputs and needs to
            round them to integers. The argument of `rounding_method` is always an
            array with the same shape like `votes`. Use `np.round` for the Sainte-
            Laguë-method and `np.floor` for the D'Hont-method. For other methods, see
            'https://en.wikipedia.org/wiki/Highest_averages_method'.
            The default is `numpy.round`.
        key : str, optional
            The key that the distribution will have in the `self.distributions`
            dictionary. The default is 'Biproportional Apportionment'.
        return_distribution : bool, optional
            If true, the function returns a Distribution object. Otherwise it just
            returns the seats array. The default is False.
        max_depth : int, optional
            Maximum number of recursions before a RecursionError is raised. The default
            is 100.
        scaling : float > 1, optional
            This scaling factor determines how fast the algorithm that finds the
            correct seat distribution converges. Smaller values lead to faster
            convergeance. However, too small values can lead to unstable overshoots
            and might result in the algorithem not converging. `scaling` must always be
            larger than one. The default is 2.
        eps : float, optional
            Small value to avoid ZeroDivisionErrors. The default is 1e-6.
        **kwargs :
            Optional keyword arguments that are passed to the Distribution-constructor.
            Can be used to add custom attributes to the created Distribution object.

        Raises
        ------
        ValueError
            Is raised when the parameters have wrong shape or invalid values.
        InvalidOrderError
            Is raised when this method is called after irrelevant parties or regions
            were deleted or grouped together with the `self.sort` or `self.reorder`
            methods.
        RecursionError
            Is raised when the algorithm did not converge after `max_depth` iterations.

        Returns
        -------
        seats : numpy.ndarray of type int
            Array containing the number of seats each party gets in each region. The
            array has the same shape as `self.votes`. `seats[i,j]` is the number of
            seats that the i'th party gets in the j'th region. Only returned if
            `return_distribution == False`.
        distribution : Distribution
            Distribution object corresponding to the calculated distribution. Only
            returned if `return_distributions == True`.

        """
        # check and update mode
        if self.mode > 1:
            raise InvalidOrderError('Cannot calculate apportionments after `self.reorder` identified irrelevant parties and regions.')
        self._mode = max(1, self.mode)
        # get number of parties and regions
        NoP, NoR = self.shape
        # assert that mode is valid
        which = which.strip().lower()
        if which.strip().lower() not in ('regions', 'parties', 'both'):
            raise ValueError(f"'{which}' is not a valid value for `mode`.")
        # assert that seats has the right format for the given mode
        if which == 'parties':
            if type(seats) == type(None):
                if type(self.region_seats) == type(None):
                    raise ValueError("`seats` cannot be None while `which=='parties'` and `self.region_seats==None`.")
                seats = self.region_seats
            else:
                seats = np.array(seats, dtype=int).ravel()
            if seats.shape != (NoR,):
                raise ValueError(f"`seats` needs size {NoR} but has size {seats.size}.")
        if which == 'regions':
            if type(seats) == type(None):
                if type(self.party_seats) == type(None):
                    raise ValueError("`seats` cannot be None while `which=='regions'` and `self.party_seats==None`.")
                seats = self.party_seats
            else:
                seats = np.array(seats, dtype=int).ravel()
            if seats.shape != (NoP,):
                raise ValueError(f"`seats` needs size {NoP} but has size {seats.size}.")
        if which == 'both':
            if type(seats) == type(None):
                if self.total_seats == None:
                    raise ValueError("`seats` cannot be None while `which=='both'` and `self.total_seats==None`.")
                seats = self.total_seats
            try:
                seats = int(seats)
            except (TypeError, ValueError):
                raise ValueError("`seats` must be an integer.")
            if seats < 1:
                raise ValueError(f"`seats` must be positive but is {seats}.")
        
        if which == 'parties':
            # get an inital guess for the column (region) divisors
            divisors = (self.votes.sum(axis=0)/(seats+eps)).reshape(1, NoR)
            # call __get_column_divisors__ to get the definite divisors
            assigned_seats, divisors = self.__get_column_divisors__(seats,
                    column_divisors=divisors, rounding_method=rounding_method,
                    max_depth=max_depth, scaling=scaling, eps=eps)
            dist = Distribution(assigned_seats, self,
                        method='Proportional Apportionment (fixed region seats)',
                        region_divisors=divisors, rounding=rounding_method, **kwargs)
        
        elif which == 'regions':
            # get an inital guess for the row (party) divisors
            divisors = (self.votes.sum(axis=1)/(seats+eps)).reshape(NoP, 1)
            # call __get_row_divisors__ to get the definite divisors
            assigned_seats, divisors = self.__get_row_divisors__(seats,
                    row_divisors=divisors, rounding_method=rounding_method,
                    max_depth=max_depth, scaling=scaling, eps=eps)
            dist = Distribution(assigned_seats, self,
                        method='Proportional Apportionment (fixed party seats)',
                        party_divisors=divisors, rounding=rounding_method, **kwargs)
        
        else:
            # get provisional divisor and seats
            divisors = self.votes.sum()/seats
            assigned_seats = rounding_method(self.votes/divisors)
            total_seats = assigned_seats.sum(dtype=int)
            
            # if assigned seats does not match total seats, start iteration
            if total_seats != seats:
                factor = 1
                iteration = 0
                too_low = total_seats < seats
                
                while True:
                    if iteration >= max_depth:
                        raise RecursionError(f"`proportional_apportionment` did not converge after {iteration} iterations.")
                    iteration += 1
                    
                    # update votes
                    divisors *= 1 + (total_seats-seats)/seats * factor
                    assigned_seats = rounding_method(self.votes/divisors)
                    total_seats = assigned_seats.sum(dtype=int)
                    
                    if total_seats == seats:
                        break
                    elif ((too_low and total_seats>seats)
                        or (not too_low and total_seats<seats)):
                        too_low = not too_low
                        factor /= scaling
        
            # convert assigned_seats into integer array and create Distribution object
            dist = Distribution(assigned_seats, self,
                        method='Proportional Apportionment (fixed total seats)',
                        divisor=divisors, rounding=rounding_method, **kwargs)
        
        self._seats = np.array(assigned_seats, dtype=int)
        self.distributions[key] = dist
        if return_distribution:
            return dist
        else:
            return self.seats



class Distribution():
    """
    Distribution objects are used to store the seat distributions. The core
    of each Distribution object is the `self.seats` array that stores which
    party received how many seats in which region. It also has other attributes
    that store additional information about the apportionment that lead to the
    distribution such as the used divisors.

    """
    def __init__(self, seats, election, method=None, party_divisors=None, region_divisors=None,
                 upper_party_divisor=None, upper_region_divisor=None, divisor=None,
                 rounding=None, party_rounding=None, region_rounding=None, **kwargs):
        """
        Creates a Distribution object. Every distribution must be linked to an
        Election object. We assume that this election has `NoP` parties and `NoR`
        regions.

        Parameters
        ----------
        seats : array-like with shape (`NoP`, `NoR`)
            An array indicating which party received how many seats in which region.
            `seats[i,j]` must be an integer and indicates how many seats the i'th party
            received in the j'th region.
        election : Election
            The election to which the Distribution is linked. `election.shape` must be
            `(NoP, NoR)`. This link is required to handle `self.party_names` and
            `self.region_names`.
        method : str or None, optional
            The name of the apportionment method used to calculate the distribution.
            The default is None.
        party_divisors : array-like or None, optional
            Array containing the party divisors used to calculate the distribution, or
            None if no divisors were used. Must be reshapable to `(NoP, 1)`. The
            default is None.
        region_divisors : array-like or None, optional
            Array containing the region divisors used to calculate the distribution, or
            None if no divisors were used. Must be reshapable to `(1, NoR)`. The
            default is None.
        upper_party_divisor : float or None, optional
            The divisor used in the upper apportionment of the seats to the parties,
            or None if no divisor was used. The default is None.
        upper_region_divisor : float or None, optional
            The divisor used in the upper apportionment of the seats to the regions,
            or None if no divisor was used. The default is None.
        divisor : float or None, optional
            A single divisor for all parties and regions, or None if no such divisor
            was used. The default is None.
        rounding : function or None
            The rounding function that was used to round the divided votes to seats,
            or None if no such rounding function was used. The default is None.
        party_rounding : function or None
            The rounding function that was used in the upper apportionment of seats
            to parties, or None if no such rounding function was used. The default is
            None.
        region_rounding : function or None
            The rounding function that was used in the upper apportionment of seats
            to regions, or None if no such rounding function was used. The default is
            None.
        kwargs
            Additional keyword arguments that can be used to give the Distribution
            objects additional attributes. For example, `kwargs=={'myAttribute': 12,
            'otherAttr': 'value}` creates the two attributes `self.myAttribute` and
            `self.otherAttr` and sets them to the values 12 and 'value'.

        Raises
        ------
        KeyError
            Is raised when `kwargs` contains an invalid key. Keys starting with '_'
            are considered invalid as well as the keys 'NoP', 'NoR', 'shape',
            'party_names', 'region_names', 'parties', 'regions', 'total_seats',
            'region_seats', and 'party_seats'.
        ValueError
            Is raised when the parameters do not define a valid Distribution object.

        """
        # test if all given kwargs are valid and set them as attributes
        illegal_attr = ('NoP', 'NoR', 'shape', 'party_names', 'region_names', 'parties',
                        'regions', 'total_seats', 'region_seats', 'party_seats')
        for key, value in kwargs.items():
            if key[0]=='_' or key in illegal_attr:
                raise AttributeError(f'{key} is not an allowed keyword argument for Distribution objects.')
            setattr(self, key, value)
        
        # test if given election and seats are valid
        if type(election) != Election:
            raise TypeError(f'`election` argument must be of type {Election} but is type {type(election)}.\n')
        self._election = election
        NoP, NoR = self.election.votes.shape
        self._seats = np.array(seats, dtype=int)
        if self.seats.shape != self.election.votes.shape:
            raise ValueError(f'`seats` argument must have shape {self.election.votes.shape} but has shape {self.seats.shape}.')
        
        # check whether divisors have right shape and set them
        if type(party_divisors) == type(None):
            self._party_divisors = None
        else:
            try:
                self._party_divisors = np.array(party_divisors, dtype=float)
            except:
                raise ValueError(f'Invalid argument for `party_divisors`. Could not convert `party_divisors` to numpy.ndarray.')
            try:
                self._party_divisors = self.party_divisors.reshape((NoP, 1))
            except:
                raise ValueError(f'`party_divisors` must have shape {(NoP,)} or {(NoP, 1)} but has shape {self._party_divisors.shape}.')
        if type(region_divisors) == type(None):
            self._region_divisors = None
        else:
            try:
                self._region_divisors = np.array(region_divisors, dtype=float).reshape((1, NoR))
            except:
                raise ValueError(f'Invalid argument for `region_divisors`. Could not convert `region_divisors` to numpy.ndarray.')
            try:
                self._region_divisors = self.region_divisors.reshape((1, NoR))
            except:
                raise ValueError(f'`region_divisors` must have shape {(NoP,)} or {(NoP, 1)} but has shape {self._party_divisors.shape}.')
        if type(upper_party_divisor) == type(None):
            self._upper_party_divisor = None
        else:
            try:
               self._upper_party_divisor = float(upper_party_divisor)
            except:
                raise ValueError(f'Could not convert `upper_party_divisor` ({upper_party_divisor}) to float.')
        if type(upper_region_divisor) == type(None):
            self._upper_region_divisor = None
        else:
            try:
                self._upper_region_divisor = float(upper_region_divisor)
            except:
                raise ValueError(f'Could not convert `upper_region_divisor` ({upper_region_divisor}) to float.')
        if type(divisor) == type(None):
            self._divisor = None
        else:
            try:
                self._divisor = float(divisor)
            except:
                raise ValueError(f'Could not convert `divisor` ({divisor}) to float.')

        # set other attributes
        self.method = method
        self._rounding = rounding
        self._party_rounding = party_rounding
        self._region_rounding = region_rounding
    
    @property
    def election(self):
        return self._election
    @property
    def seats(self):
        return self._seats
    @seats.setter
    def seats(self, new_seats):
        new_seats = np.array(new_seats, dtype=int)
        if new_seats.shape != self.election.votes.shape:
            raise ValueError(f'`seats` must have shape {self.election.votes.shape}.')
        self._seats = new_seats
    @property
    def party_divisors(self):
        return self._party_divisors
    @property
    def region_divisors(self):
        return self._region_divisors
    @property
    def upper_party_divisor(self):
        return self._upper_party_divisor
    @property
    def upper_region_divisor(self):
        return self._upper_region_divisor
    @property
    def divisor(self):
        return self._divisor
    @property
    def rounding(self):
        return self._rounding
    @property
    def party_rounding(self):
        return self._party_rounding
    @property
    def region_rounding(self):
        return self._region_rounding
    @property
    def total_seats(self):
        return self.seats.sum()
    @property
    def party_seats(self):
        return self.seats.sum(axis=1)
    @property
    def region_seats(self):
        return self.seats.sum(axis=0)
    @property
    def party_names(self):
        return self.election.party_names
    @property
    def parties(self):
        return self.election.parties
    @property
    def region_names(self):
        return self.election.region_names
    @property
    def regions(self):
        return self.election.regions
    @property
    def shape(self):
        return self.seats.shape
    def __sizeof__(self):
        return self.seats.__sizeof__()
    @property
    def NoP(self):
        return self.shape[0]
    @property
    def NoR(self):
        return self.shape[1]
    
    def __repr__(self):
        return f'<Distribution with {self.NoP} parties and {self.NoR} regions.>'

    def __str__(self):
        lines = self.seats.__repr__()[5:].split('\n')
        s = 'Distribution' + lines[0]
        for line in lines[1:]:
            s += '\n' + 7*' ' + line
        return s

    def _reorder_parties(self, new_order, other=[]):
        """
        Reorders the rows of `self.seats` and `self.party_divisors` according to
        to `new_order`.

        """
        if other:
            if type(self.party_divisors)==np.ndarray:
                self.party_divisors[other[-1], 0] = np.nan
            for i in other[:-1]:
                self.seats[other[-1]] += self.seats[i]
        if type(self.party_divisors)==np.ndarray:
            self._party_divisors = self.party_divisors[new_order]
        self._seats = self.seats[new_order]
    
    def _reorder_regions(self, new_order, other=[]):
        """
        Reorders the columns of `self.seats` and `self.region_divisors` according to
        to `new_order`.

        """
        if other:
            if type(self.region_divisors)==np.ndarray:
                self.region_divisors[0, other[-1]] = np.nan
            for i in other[:-1]:
                self.seats[:, other[-1]] += self.seats[:, i]
        if type(self.region_divisors)==np.ndarray:
            self._region_divisors = self.region_divisors[:, new_order]
        self._seats = self.seats[:, new_order]
    
    def to_dataframe(self):
        """
        Converts `self.seats` to a pandas DataFrame and returns it.

        """
        return DataFrame(self.seats, index=self.parties, columns=self.regions, dtype=int, copy=True)


class DistDict(dict):
    """
    Subclass of python dictionaries that only allows values of type `Distribution`
    and enforces that these distributions point to the same Election object and
    that they have a shape that is compatible with the Election object.

    """
    def __init__(self, election, *args, **kwargs):
        if type(election) != Election:
            raise TypeError(f'`election` must be of type {Election}, not {type(election)}.')
        self._election = election
        super().__init__(*args, **kwargs)
    def __setitem__(self, key, value):
        if type(value)!=Distribution:
            try:
                value = np.array(value, dtype=int)
            except:
                raise TypeError(f'`value` must be array-like or of type {Distribution}, not {type(value)}.')
            if value.shape != self.election.shape:
                raise ValueError(f'`value` must have shape {self.election.shape} but has shape {value.shape}.')
            value = Distribution(value, self.election)
        else:
            if self.election != value.election:
                raise ValueError(f'`self.election` and `value.election` must be identical.')
            if self.election.votes.shape != value.seats.shape:
                raise ValueError(f"The distribution's seats-array must have shape {self.election.votes.shape} but has shape {value.seats.shape}.")
        self.election._mode = max(1, self.election.mode)
        return super().__setitem__(key, value)
    @property
    def election(self):
        return self._election