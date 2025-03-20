# -*- coding: utf-8 -*-

# This code was taken from the `hasseNetworkx`` module by Simon Hegele at GitHub 
# Only the `hasse()`function was slightly changed fromn his tutorial.

import matplotlib.pyplot
import networkx
import numpy
from kstpy.helpers import srdomain
from kstpy.helpers import reduceSR

def _exists_path(Graph, u, v, start=True):
    '''
    If there exits a path from u to v in G with length > 0: Return True
    Else                                                  : Return False
    Recursive method
    (Checks if there exists a path from any successor u' of u to v)
    
        Parameters:
            Graph (networkx.DiGraph)
            u     (string),  identifier of first node in Graph
            v     (string),  identifier of second node in Graph
            start (boolean), True  if u is the recursion start
                             False else
            
        Returns:
            (boolean) True  if there exits a path from u to v in G
                      False else
    
    Additional remark:
        If the execution of this function leads to an stack overflow
        this can indicate a faulty method for the evaluation of the
        relationships that might cause circles in the Graph.
    '''
    # Trivial case 1: Reached v
    if u == v and not start:
        return True
    successors = [successor for successor in Graph.neighbors(u) if not ((successor == v) and start)]
    # Trivial case 2: u has no successors 
    if len(successors) == 0:
        return False
    # Recursion
    successors_on_path = [_exists_path(Graph, successor, v, start=False) for successor in successors]
    return (True in successors_on_path)

def _transitivity_elimination(Graph):
    ''' 
    Removes edges that are implied by transitivity of the partial order
    
        Parameters:
            Graph (networkx.DiGraph)
            
         Returns:
         
    Additional remark:
        If the execution of this function leads to an stack overflow
        this can indicate a faulty method for the evaluation of the
        relationships that might cause circles in the Graph.
    '''
    edges_to_remove = []
    for edge in Graph.edges():
        if _exists_path(Graph, edge[0], edge[1], start=True):
            edges_to_remove.append(edge)
    Graph.remove_edges_from(edges_to_remove)

def _layer(positions, i):
    '''
    Returns the positions of nodes at layer i in a dictionary
    
        Parameters:
            posititions (dictionary)
            i           (int)
            
        Returns:
            (dictionary) the positions of nodes at layer i in a dictionary
    '''
    return {position[0]: position[1] for position in positions.items() if  position[1][1]==i}

def _y_positioning(Graph, positions, n = 0):
    ''' 
    '''
    current_layer = _layer(positions, n)
    final_layer = True
    for u in current_layer:
        for v in current_layer:
            if (u,v) in Graph.edges() and positions[v][1]==n:
                final_layer = False
                positions[v] = (positions[v][0],positions[v][1]+1)
    if final_layer:
        return positions
    else:
        return _y_positioning(Graph, positions, n = n+1)

def _y_positioning_by_function(Graph, positions, layer_function):
    '''
    '''
    for node in Graph.nodes():
        positions[node] = (0, layer_function(node))
    return positions

def _number_of_layers(positions):
    '''
    Returns the number of layers in the hasse-diagramm
    (i.e. the highest y-position value in positions)
    
        Parameters:
            positions (dictionary)
            
        Returns:
            (int)
    '''
    return max([position[1][1] for position in positions.items()])

def _max_layer_size(positions):
    '''
    Returns the maximum numbber of nodes in any layer of the hasse-diagram
    
        Parameters:
            positions (dictionary)
        
        Returns:
            (int)
    '''
    return max([len(_layer(positions, i)) for i in range(_number_of_layers(positions))])

def _shift_x_positions(positions):
    '''
    Shifts the layers alternately by half a unit to the left or right along the x-axis.
    
    Parametrs:
        positions (dictionary)
    
    Returns:
        (dictionary)
    '''
    y_positions = numpy.unique([positions[position][1] for position in positions])
    for i, y_position in enumerate(y_positions):
        for position in positions:
            if positions[position][1]==y_position:
                positions[position]=(positions[position][0]+0.5**(i%2),positions[position][1])
    return positions

def _x_positioning(Graph, positions, shift_x=False):
    n = _number_of_layers(positions) # height
    w = _max_layer_size(positions)   # width
    for i in range(n+1):
        current_layer = _layer(positions, i)
        for j, node in enumerate(current_layer):
            positions[node] = (1+2*(j+1)*w/(len(current_layer)+1), positions[node][1])
    if shift_x:
        return _shift_x_positions(positions)
    return positions

def _layout(Graph, layer_function=None, shift_x=False):
    '''
    Returns a dictionary with positions for the nodes of the graph
    '''
    positions = {node: (0,0) for node in Graph.nodes()}
    try:
        positions = _y_positioning_by_function(Graph, positions, layer_function)
    except:
        positions = _y_positioning(Graph, positions, n = 0)
    positions = _x_positioning(Graph, positions)
    if shift_x:
        positions = _shift_x_positions(positions)
    return positions

def hasse(structure, title = ""):
    """
    Draw a Hasse diagram for a knowledge structure
    
    Parameters
    ----------
    structure: list or set of sets (or derivatives)
    title: str (optional)

    Result
    ------
    Plot of Hasse diagram

    Example
    -------

    >>> hasse(kstpy.data.xpl_basis, title = "Small example basis")
    """
    subset_relationships = [(str(s1),str(s2)) for s1 in structure for s2 in structure if ((s1 != s2) and (s1.issubset(s2)))]

    # Defining the Graph object
    Graph = networkx.DiGraph()
    Graph.add_nodes_from([str(s) for s in structure])
    Graph.add_edges_from(subset_relationships)
    _transitivity_elimination(Graph)

    # Plotting
    matplotlib.pyplot.figure(figsize=(16, 12))
    networkx.draw_networkx(Graph, node_size=[(len(eval(node))+1)*2000 for node in Graph.nodes()], pos=_layout(Graph, shift_x=True), node_color = "#00cc00")
    matplotlib.pyplot.title(title, fontsize=20)
    matplotlib.pyplot.show()

def sr_hasse(sr, title = ""):
    """
    Draw a Hasse diagram for a surmise relation

    Parameters
    ----------

    sr: set of 2-tuples (surmise relation)
    title: str (optional)

    Result
    ------
    Plot of Hasse diagram

    Example
    -------

    >>> sr_hasse(kstpy.basics.surmiserelation(kstpy.data.xpl_basis), title = "Small example")
    """
    d = srdomain(sr)
    nt = reduceSR(sr)
    g = networkx.DiGraph()
    g.add_nodes_from([q for q in d])
    g.add_edges_from([(q1, q2) for q1 in d for q2 in d if ((q1 != q2) and ((q1,q2) in nt))])
    matplotlib.pyplot.figure(figsize=(16,12))
    networkx.draw_networkx(g, node_size=[2500 for node in g.nodes], pos=_layout(g, shift_x=True), node_color="#00cc00")
    matplotlib.pyplot.title(title, fontsize=20)
    matplotlib.pyplot.show()

