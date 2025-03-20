# -*- coding: utf-8 -*-

import random
from kstpy.helpers import domain
from kstpy.helpers import kstFrozenset


def simulate(structure, number, beta, gamma):
    """Simulate data from a structure according to the BLIM

    Parameters
    ----------

    structure: set or list
        data basis for the simulation
    number: int
        number of response patterns to be simulated
    beta: float
        likelihood for careless errors
    gamma: float
        likelihood for lucky guesses

    """
    d = domain(structure)
    sl = list(structure)
    simdata = list()
    for i in range(number):
        h = list()
        s = sl[random.randint(0,len(sl)-1)]
        for q in d:
            if (q in s):
                if random.random() > beta:
                    h.append(q)
            else:
                if random.random() < gamma:
                    h.append(q)
        sl.append(kstFrozenset(set(h)))
    return sl

