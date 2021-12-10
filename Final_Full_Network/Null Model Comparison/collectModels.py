import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import math
import random

G = nx.read_edgelist('largest_component_networkx_format.csv', comments='#',
                     create_using=nx.DiGraph(), 
                     delimiter=',', 
                     nodetype=int, 
                     encoding='utf-8')

def directed_connected_double_edge_swap(G, nswap=1, _window_threshold=3, seed=None):
    """Attempts the specified number of double-edge swaps in the graph `G`.

    A double-edge swap selects two random edges
    and creates the new edges u->x and v->y::

     u-->v           u-->y
            becomes  
     x-->y           x-->v

    If either `(u, x)` or `(v, y)` already exist, then no swap is performed
    so the actual number of swapped edges is always *at most* `nswap`.

    Parameters
    ----------
    G : graph
       An undirected graph

    nswap : integer (optional, default=1)
       Number of double-edge swaps to perform

    _window_threshold : integer

       The window size below which connectedness of the graph will be checked
       after each swap.

       The "window" in this function is a dynamically updated integer that
       represents the number of swap attempts to make before checking if the
       graph remains connected. It is an optimization used to decrease the
       running time of the algorithm in exchange for increased complexity of
       implementation.

       If the window size is below this threshold, then the algorithm checks
       after each swap if the graph remains connected by checking if there is a
       path joining the two nodes whose edge was just removed. If the window
       size is above this threshold, then the algorithm performs do all the
       swaps in the window and only then check if the graph is still connected.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    int
       The number of successful swaps

    Raises
    ------

    NetworkXError

       If the input graph is not connected, or if the graph has fewer than four
       nodes.

    Notes
    -----

    The initial graph `G` must be connected, and the resulting graph is
    connected. The graph `G` is modified in place.

    References
    ----------
    .. [1] C. Gkantsidis and M. Mihail and E. Zegura,
           The Markov chain simulation method for generating connected
           power law random graphs, 2003.
           http://citeseer.ist.psu.edu/gkantsidis03markov.html
    """
    if not nx.is_weakly_connected(G):
        raise nx.NetworkXError("Graph not connected")

    n = 0
    swapcount = 0
    deg = G.degree()
    # Label key for nodes
    keys, degrees = zip(*G.degree())  # keys, degree
    cdf = nx.utils.cumulative_distribution(list(d for n, d in G.degree()))
    discrete_sequence = nx.utils.discrete_sequence
    window = 1
    while n < nswap:
#         print("---------------------")
        wcount = 0
        swapped = []
        # If the window is small, we just check each time whether the graph is
        # connected by checking if the nodes that were just separated are still
        # connected.
        if window < _window_threshold:
            # This Boolean keeps track of whether there was a failure or not.
            fail = False
            while wcount < window and n < nswap:
                # Pick two random edges without creating the edge list. Choose
                # source nodes from the discrete degree distribution.
                (ui, xi) = discrete_sequence(2, cdistribution=cdf, seed=seed)
                # If the source nodes are the same, skip this pair.
                if ui == xi:
                    continue
                # Convert an index to a node label.
                u = keys[ui]  # convert index to label
#                 print("u: ")
#                 print(u)
                x = keys[xi]
#                 print("x: ")
#                 print(x)
                # Choose targets uniformly from neighbors.
                if(len(list(G[u])) >0 and len(list(G[x])) >0 ):
#                     print("Outgoing edges u:")
#                     print(list(G[u]))
                    v = random.choice(list(G[u]))
                    y = random.choice(list(G[x]))
#                     print("Outgoing edges x:")
#                     print(list(G[x]))
#                     print("v:")
#                     print(v)
            
#                     print("y:")
#                     print(y)
                else:
                    continue
                # If the target nodes are the same, skip this pair.
                if v == y:
#                     print("sametarget")
                    continue
                if (v not in G[x]) and (y not in G[u]):  # don't create parallel edges
                    if (u == y or x ==v): # dont create a self loop
                        continue
                    G.add_edge(u, y)
#                     print("edge_added: ")
#                     print(u)
#                     print("->")
#                     print(y)
                    G.add_edge(x, v)
#                     print("edge_added: ")
#                     print(x)
#                     print("->")
#                     print(v)

#                     print("_____removed Edges___")
                    G.remove_edge(u, v)
#                     print(u)
#                     print("->")
#                     print(v)
                    G.remove_edge(x, y)
#                     print(x)
#                     print("->")
#                     print(y)
#                     print("______________________")
                    swapped.append((u, v, x, y))
                    swapcount += 1
                n += 1
                # If G remains connected... WHY ARE BOTH NOT CHECKED?
                if nx.has_path(G, u, v):
                    wcount += 1
                # Otherwise, undo the changes.
                else:
                    G.add_edge(u, v)
                    G.add_edge(x, y)
#                     print("We made the Graph disconnected")
                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    swapcount -= 1
                    fail = True
            # If one of the swaps failed, reduce the window size.
            if fail:
                window = int(math.ceil(window / 2))
            else:
                window += 1
        # If the window is large, then there is a good chance that a bunch of
        # swaps will work. It's quicker to do all those swaps first and then
        # check if the graph remains connected.
        else:
            while wcount < window and n < nswap:
                # Pick two random edges without creating the edge list. Choose
                # source nodes from the discrete degree distribution.
                (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
                # If the source nodes are the same, skip this pair.
                if ui == xi:
                    continue
                u = keys[ui]  # convert index to label
#                 print("u: ")
#                 print(u)
                x = keys[xi]
#                 print("x: ")
#                 print(x)
                # Choose targets uniformly from neighbors.
                if(len(list(G[u])) >0 and len(list(G[x])) >0 ):
#                     print("Outgoing edges u:")
#                     print(list(G[u]))
                    v = random.choice(list(G[u]))
                    y = random.choice(list(G[x]))
#                     print("Outgoing edges x:")
#                     print(list(G[x]))
#                     print("v:")
#                     print(v)
            
#                     print("y:")
#                     print(y)
                else:
                    continue
                # If the target nodes are the same, skip this pair.
                if v == y:
                    continue
                if (v not in G[x]) and (y not in G[u]):  # don't create parallel edges
                    if (u == y or x ==v): # dont create a self loop
                        continue
                    G.add_edge(u, y)
#                     print("edge_added: ")
#                     print(u)
#                     print("->")
#                     print(y)
                    G.add_edge(x, v)
#                     print("edge_added: ")
#                     print(x)
#                     print("->")
#                     print(v)

#                     print("_____removed Edges___")
                    G.remove_edge(u, v)
#                     print(u)
#                     print("->")
#                     print(v)
                    G.remove_edge(x, y)
#                     print(x)
#                     print("->")
#                     print(y)
#                     print("______________________")
                    swapped.append((u, v, x, y))
                    swapcount += 1
                n += 1
                wcount += 1
            # If the graph remains connected, increase the window size.
            if nx.is_weakly_connected(G):
                window += 1
            # Otherwise, undo the changes from the previous window and decrease
            # the window size.
            else:
                while swapped:
                    (u, v, x, y) = swapped.pop()
                    G.add_edge(u, v)
                    G.add_edge(x, y)
                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    swapcount -= 1
                window = int(math.ceil(window / 2))
    return swapcount

for i in range(2000,2300):
    H = G.copy()
    directed_connected_double_edge_swap(H, nswap=20*len( G.edges() ))
    nx.write_weighted_edgelist(H, "Directed_Unweighted_Models/Directed_Unweighted_Random_Null_Model_{}".format(i))
