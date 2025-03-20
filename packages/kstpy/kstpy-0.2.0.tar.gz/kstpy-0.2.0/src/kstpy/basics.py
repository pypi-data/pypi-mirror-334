# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 2025

@author: Cord Hockemeyer
"""
from kstpy.helpers import kstFrozenset
from kstpy.helpers import domain
from kstpy.helpers import srdomain

def constr(structure):
    """ Compute the smallest knowledge space containing a famly of kstFrozensets

    Parameters
    ----------
    structure: set
        Family of kstFrozensets

    Returns
    -------
    Knowledge space

    Examples
    --------
    >>> from kstpy.data import xpl_basis
    >>> constr(xpl_basis)
    """
        
    space = set({kstFrozenset({}), kstFrozenset(domain(structure))})
    space.union(structure)
    for state in structure:
        new_states = set({})
        for s in space:
            if not ((set({state | s})) <= space):
                new_states.add((state | s))
        space = space | new_states
    return space

def basis(structure):
    """ Determine the basis of a knolwdge space/structure
    
    Parameters
    ----------
    structure: set
        Family of kstFrozensets
    
    Returns
    -------
    Basis

    Examples
    --------
    >>> from kstpy.data import xpl_basis
    >>> s = constr(xpl_basis)
    >>> basis(s)
    """
    b = set({})
    for state in structure:
        h = set(state)
        for i in structure:
            if set(i) < set(state):
                h = h - set(i)
            if h == set({}):
                break
        if len(h) > 0:
            b.add(kstFrozenset(state))
    return b

def surmiserelation(structure):
    """Compute the surmise relation for a knowledge structure
    
    Parameters
    ----------

    structure: set
        Family of kstFrozensets
    
    Returns
    -------

    Corresponding surmise relation

    Examples
    --------
    >>> from kstpy.data import xpl_basis
    >>> s = constr(xpl_basis)
    >>> surmiserelation(s)

    """
    d = domain(structure)
    sr = set({})
    b = basis(structure)

    for i in d:
        for j in d:
            sr.add((i,j))
    for s in b:
        for i in d:
            for j in d:
                if i in s and not j in s:
                    sr.discard((j,i))
                if j in s and not i in s:
                    sr.discard((i,j))
    return(sr)

def sr2basis(sr):
    """ Compute the basis corresponding to a surmise relation

    Parameters
    ----------

    sr: set (of 2-tuples)

    Returns
    -------

    Corresponding basis
    """
    d = srdomain(sr)
    b = set({})
    for q in d:
        s = set({q})
        for p in sr:
            if p[1]==q:
                s.add(p[0])
        b.add(kstFrozenset(s))
    return b


def neighbourhood(state, structure, maxdist = 1):
    """
    Determine the neighbourhood of a state"

    Parameters
    ----------
    state: kstFrozenset
    structure: set (of kstFrozensets)
    maxdist: int (radius of the neighbourhood; default = 1)

    Returns
    -------
    Set containing the neighbourhood
    """
    n = set({})
    for s in structure:
        if (len(s ^ state) <= maxdist) & (s != state):
            n.add(s)
    return n

def fringe(state, structure, maxdist = 1):
    """
    Determine the inner, outer, and total fringe of a state"

    Parameters
    ----------
    state: kstFrozenset
    structure: set (of kstFrozensets)
    maxdist: int (radius of the fringe; default = 1)

    Returns
    -------
    Dictionary with three lists: fringe, inner (fringe), and Outer (fringe)
    """
    f = set({})
    fi = set({})
    fo = set({})
    n = neighbourhood(state, structure, maxdist)
    for s in n:
        f.add(s^state)
        if s.issubset(state):
            fi.add(s^state)
        elif state.issubset(s):
            fo.add(s^state)
    fl = {"fringe": f,
          "inner": fi,
          "outer": fo}
    return fl

def equivalence(structure):
    """Determine equi9valence classes
    
    Parameters
    ----------

    structure: set or list of kstFrozensets

    Returns
    -------

    Equivalence classes (set of kstFrozensets)
    """
    d = domain(structure)
    ecl = set({})
    for q in d:
        c = set({q})
        for r in d:
            if q != r:
                cd = True
                for s in structure:
                    if len(set({q,r}) & set(s)) == 1:
                        cd = False
                if cd:
                    c.add(r)
        ecl.add(kstFrozenset(c))
    return ecl

                    
def gradations(s1, s2, structure):
    """Determine all gradations from s1 to s2 in structure
    
    Parameters
    ----------

    s1: kstFrozenset (starting state)
    s2: kstFrozenset (goal state)
    structure: set of kstFrozensets (knowledge structure)

    Returns
    -------
    set of lists containing all gradations from s1 to s2 within structure
    """
    if s1 == s2:
        return set({tuple(set({s1}))})
    if not s1 < s2:
        return None
    res = set({})
    n = neighbourhood(s1, structure, maxdist=1)
    for s in n:
        if (s > s1) and (s <= s2):
            g = gradations(s, s2, structure)
            newg = set({})
            if (len(g) >= 1):
                for lp in g:
                    l = list(lp)
                    l.insert(0, s1)
                    lt = tuple(l)
                    newg = newg | set({lt})
                res = res | newg
    return(res)

    
    
def learningpaths(structure):
    """ Return all learning paths in a knwoledge structure
    
    Parameters
    ----------
    structure: set of kstFrozensets

    Returns
    -------
    set of lists containing all learning paths in the structure
    """
    empty = kstFrozenset(set({}))
    Q = kstFrozenset(set(domain(structure)))
    return gradations(empty, Q, structure)

