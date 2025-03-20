# -*- coding: utf-8 -*-

"""

Created on Thu Mar 13 2025



@author: Cord Hockemeyer

"""

from kstpy.helpers import kstFrozenset
from kstpy.helpers import itemname
from kstpy.helpers import domain
from kstpy.helpers import vector2kstFrozenset
from kstpy.helpers import kstFrozenset2vector
import re

def readpatterns(filename):
    """Read a set of response patterns from a file

    Parameters
    ----------

    filename: str

    Returns
    -------
    List of patterns (kstFrozensets)
    """
    f = open(filename, "r")
    content = f.read()
    lines = content.split("\n")
    i = 0
    if (lines[0][0] == "#"):   # SRBT format
        i = 1
    pat = re.search("[01]*", lines[i]).group()
    if ((pat == lines[i]) & (len(pat) > 3)):    # File with just the matrix
        noi = len(lines[i])
        nos = len(lines) - i
    else:     # KST or SRBT format: #items, #states, matrix
        noi = int(lines[i])
        nos = int(lines[i+1])
        i = i+2
    d = list([])
    for q in range(noi):
        d.append(itemname(q))
    p = list([])
    for j in range(nos):
        p.append(vector2kstFrozenset(lines[j+i], d))
    return p

def readstructure(filename):
    """Read a knowledge structure from a file

    Parameters
    ----------
    
    filename: str

    Returns
    -------
    Set of states (kstFrozensets)
    """
    return set(readpatterns(filename))

    
def writekst(filename, x):
    """Write a knowledge structure or a data set to a file
    
    Parameters
    ----------

    filename: str
    x: list or set (of kstFrozensets)

    Currently, we write only classical KST format files.
    """
    f = open(filename, "w")
    d = domain(x)
    f.write(str(len(d))+"\n")
    f.write(str(len(x))+"\n")
    for s in x:
        f.write(kstFrozenset2vector(s, d)+"\n")
    f.close()
