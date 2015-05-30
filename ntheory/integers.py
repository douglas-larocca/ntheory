from pyoeis import OEISClient
from numpy import inf, nan

class Integer(object):
    """utility class for representing and working
    with the integers
    
    very many things possible here. was originally 
    intended as syntax convenience to use of the 
    Ellipsis for generating lists of integers according 
    to some inferred rule;
    ---
    
    if no upper bound given, then Z returns a
    counter that will count based on the
    first few elements given, e.g.
    >>> pos_ints = Z[1, 2, ...]
    >>> [i for i in pos_ints if i < 10]
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    But note how the series will be *inferred*
    from the given elements:
    >>> even_ints = Z[2, 4, ...]
    >>> [i for i in even_ints if i < 10]
    [2, 4, 6, 8]
    
    This is computed only for the obvious cases.
    For unknown cases we can use `pyoeis` to suggest
    possible matches:
    
    >>> from pyoeis import OEISClient
    >>> oeis = OEISClient()
    >>> seq = oeis.lookup_by_terms([1,2,3,4])
    >>> seq0 = seq[0]
    >>> seq0.name, seq0.id, seq0.unsigned(10), \
    ... seq0.keywords, seq0.alt_ids, seq0.author
    ('The positive integers',
     'A000027',
     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
     ['%K A000027 core'],
     ['M0472', 'N0173'],
     '_N. J. A. Sloane_')
    
    An interesting idea would be to maintain a process
    while the `Z` integer object is alive that will query 
    the OEIS as `Z` is manipulated (in some intelligent way
    of course). 
    
    TODO: All queries and results from the OEIS should
    be stored permanently.
    """
    def __getitem__(self, items):
        types = {}
        for i, item in enumerate(items):
            item_type = type(item)
            if not types.get(item_type): 
                types[item_type] = {}
            types[item_type][i] = item
            
        ellip = types.get(type(...), {})
        before, after = list(), list()
        for position in sorted(ellip.keys()):
            # scan forward from ellipsis position
            i = position+1
            while True:
                try:
                    after.append(types[int][i])
                except KeyError:
                    break
                i+=1
            # scan backward from ellipsis position
            i = position-1
            while True:
                try:
                    before.append(types[int][i])
                except KeyError:
                    break
                i-=1
            before, after = [before[::-1]], [after]
        return types, before, after
                
Z = Integer()