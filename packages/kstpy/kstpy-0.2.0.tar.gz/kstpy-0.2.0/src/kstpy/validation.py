# -*- coding: utf-8 -*-

from kstpy.helpers import domain
from kstpy.helpers import powerset
import collections as c

def distvec(data, structure):
    """Compute a vector of distances from response patterns to a knowledge structure

    Parameters
    ----------
    data: list
        List of kstFrozensets containing response patterns
    structure: set
        Family of kstFrozensets - the knowledge structure

    Returns
    -------
    Vector of distances between response patterns and knowledge structure
    """

    ddom = domain(data)
    sdom = domain(structure)
    if (ddom != sdom):
        raise Exception("Incompativble domains")

    dvec = []
    for pattern in data:
        di = len(ddom)
        for state in structure:
            d = len(pattern ^ state)
            di = min(di, d)
        dvec.append(di)
    return dvec


def difreq(data, structure):
    """Determine a vector of frequencies of distances between a set of response patterns and a knowledge structure

    Parameters
    ----------
    data: list
        List of kstFrozensets containing response patterns
    structure: set
        Family of kstFrozensets - the knowledge structure

    Returns
    -------
    Vector of distance frequencies
    """

    dvec = distvec(data, structure)
    cnt = c.Counter(dvec)
    di = [cnt[x] for x in sorted(cnt.keys())]
    return di


def di(data, structure):
    """Determine the Discrepancy Index
    
     Parameters
    ----------
    data: list
        List of kstFrozensets containing response patterns
    structure: set
        Family of kstFrozensets - the knowledge structure

    Returns
    -------
    Discrepancy Index
   """
    dvec = distvec(data, structure)
    index = sum(dvec) / len(dvec)
    return index


def da(data, structure):
    """Determine the Distance Agreement coefficient
    
    Parameters
    ----------
    data: list
        List of kstFrozensets containing response patterns
    structure: set
        Family of kstFrozensets - the knowledge structure

    Returns
    -------
    Distance Agreement coefficient
    """
    ddat = di(data, structure)
    p = kstpy.helpers.powerset(domain(structure))
    dpot = di(p, structure)
    return ddat / dpot