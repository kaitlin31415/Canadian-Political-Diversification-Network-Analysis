import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import math
import random

G = nx.read_edgelist('largest_component_networkx_format.csv', comments='#',
                     create_using=nx.Graph(), 
                     delimiter=',', 
                     nodetype=int, 
                     encoding='utf-8')


for i in range(3000,3500):
    H = G.copy()
    nx.connected_double_edge_swap(H, nswap=15*len( G.edges() ))
    nx.write_weighted_edgelist(H, "UnDirected_Unweighted_Models/UnDirected_Unweighted_Random_Null_Model_{}".format(i))
