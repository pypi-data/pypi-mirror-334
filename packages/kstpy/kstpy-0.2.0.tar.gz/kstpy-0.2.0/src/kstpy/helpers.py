# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 13:03:53 2025

@author: hockemey
"""
import more_itertools as mi

class kstFrozenset(frozenset):
    """
    kstFrozenset is a derivative of the frozenset class.
    
    The main reason for its existance is the print function which
    does not show the class anymore. Set operands (|, &, ^, and -)
    have also been re-defined to produce kstFrozensets.
    """
    def __repr__(self):
        if self == frozenset({}):
            return "{}"
        else:
            return set(self).__repr__()

    def __str__(self):
        if self == frozenset({}):
            return "{}"
        else:
            return set(self).__str__()
    
    def __or__(self, value):
        return kstFrozenset(frozenset(self) | frozenset(value))
    
    def __and__(self, value):
        return kstFrozenset(frozenset(self) & frozenset(value))
    
    def __sub__(self, value):
        return kstFrozenset(frozenset(self) - frozenset(value))
    
    def __xor__(self, value):
        return kstFrozenset(frozenset(self) ^ frozenset(value))
    

def itemname(num):
    """Return an Itemname based on the item number
    """
    if (num < 0):
          raise Exception("Sorry, no numbers below zero")
    elif (num < 26):
         return(chr(num+97))
    elif (num < 676):
         return(chr((num//26)+97)+chr((num%26)+97)) 
    elif (num < 17576):
         return(chr((num//676)+97)+chr((num//26)+97)+chr((num%26)+97)) 
    else:
         raise Exception("So far limited to 17576 items")# -*- coding: utf-8 -*-



def domain(structure):
    """ Determine the domain of a set/list of frozensets
    """
    dom = set({})
    for s in structure:
        dom = dom | s
    return sorted(list(dom))

def srdomain(sr):
    """ Determine the domain of a surmise relation
    """
    dom = set({})
    for p in sr:
        dom = dom | set(p)
    return sorted(list(dom))

def reduceSR(sr):
    """
    Remove transitivities from a (surmise) relation
    
    Parameters
    ----------
    
    sr: set (of 2-tuples)

    Returns
    -------

    Reduced relation
    """
    src = sr.copy()
    d = srdomain(src)
    for i in d:
        for j in d:
            if (i != j) & ((i,j) in sr):
                for k in d:
                    if (i != k) & (j != k) & ((i,k) in sr) & ((j,k) in sr):
                        src.discard((i,k))
    return(src)


def powerset(domain):
    return mi.powerset_of_sets(domain)

def vector2kstFrozenset(v, d):
    if (len(v) != len(d)):
        raise Exception("Vector and domain do not match!")
    s = set({})
    for i in range(len(v)):
        if (v[i]!= "0"):
            s.add(d[i])
    return kstFrozenset(s)

def kstFrozenset2vector(s, d):
    if (not(s <= set(d))):
        raise Exception("Set and domain do not match!")
    v = ""
    for i in d:
        if i in s:
            v = v + "1"
        else:
            v = v + "0"
    return v
