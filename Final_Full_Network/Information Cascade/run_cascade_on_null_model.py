import sys

from pandas.io.parsers import count_empty_vals
import networkx as nx
import pandas as pd
import os
import random
from functools import reduce

dirname = sys.argv[2]
directory = os.fsencode(dirname)

def information_cascade(G,t_tot,init):
    
    t = 0
    
    max_weight = max([e[2]['weight'] for e in G.edges(data=True)])
    
    activation_times = {}
    for i in init:
        activation_times[i]=0
    
    while t<t_tot:
    
        curr_infectious = [n for n in activation_times if activation_times[n]==t]

        for n in curr_infectious:
            for m in G.neighbors(n):
                if m not in activation_times.keys():
                    p = G[n][m]['weight']
                    if p>random.uniform(0,1)*max_weight:
                        activation_times[m] = t+1
                        
        t+=1

    return activation_times

def run_cascade_metrics(name, starting_nodes, G):
    experiments = []
    for i in range(1,1000):
        t5 = information_cascade(G,5,starting_nodes)
        experiment = pd.DataFrame.from_dict(t5, orient='index',
                           columns=[ "activation_time_exp_{}".format(i)])
        experiments.append(experiment)
    
    experiments_df = experiments[0]

    for i in range (1, 999):
        experiments_df = pd.merge(experiments[i], experiments_Bloc_df, left_index=True, right_index=True, how='outer')
    
    experiments_df['{}_average_activation_time'.format(name)] = experiments_df.mean(axis=1)
    experiments_df['{}_average_activation_time'.format(name)] = experiments_df['{}_average_activation_time'.format(name)].apply(np.floor)
    return experiments_df[['{}_average_activation_time'.format(name)]]



count = 0

for file in os.listdir(directory):
    count = count+1
    filename = os.fsdecode(file)
    G = nx.read_edgelist(dirname + '/' + filename, comments='#',
                     create_using=nx.DiGraph(), 
                     delimiter=' ', 
                     nodetype=int, 
                     encoding='utf-8')
    lib_cascade = run_cascade_metrics('liberal', [22849568, 2891740872],G)
    con_cascade = run_cascade_metrics('conservative', [1086084557009575936, 989311745100566529],G)
    ndp_cascade = run_cascade_metrics('ndp', [2715275551, 196717787],G)
    lgbt_cascade = run_cascade_metrics('lgbt', [294660973, 119925381],G)
    bloq_cascade = run_cascade_metrics('bloq', [1063494232126689280, 16014404],G)

    data_frames = [lib_cascade, con_cascade, ndp_cascade, lgbt_cascade, bloq_cascade]

    df_merged = reduce(lambda  left,right: pd.merge(left,right,left_index=True, right_index=True,
                                                how='outer'), data_frames)
    df_merged.to_csv("{}_cascades.csv".format(filename))

	
    print("Files done {}".format(count))