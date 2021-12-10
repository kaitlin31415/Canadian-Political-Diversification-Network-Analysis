import sys

from pandas.io.parsers import count_empty_vals
import networkx as nx
import pandas as pd
import os
import random
from functools import reduce
import numpy as np

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
        experiments_df = pd.merge(experiments[i], experiments_df, left_index=True, right_index=True, how='outer')
    
    experiments_df['{}_average_activation_time'.format(name)] = experiments_df.mean(axis=1)
    experiments_df['{}_average_activation_time'.format(name)] = experiments_df['{}_average_activation_time'.format(name)].apply(np.floor)
    return experiments_df[['{}_average_activation_time'.format(name)]]


active_nodes = {'Bloc': [1342125115383939073, 273262205, 24990450, 3025416359, 1425866189780160514, 2530008414, 2800741820, 16014404, 1063494232126689280, 3402128080, 803381983, 261772246, 1143229947932229632], 
'Conservative': [17969963, 2254171724, 2555308646, 739149720, 989311745100566529, 268832287, 883774859452579840, 15810950, 129395750, 791282631006621696, 256552850, 1086084557009575936, 36133644, 34606493, 564207331, 414218319, 943174774154498048, 412708728], 
'LGBTQ2S+': [294660973, 119925381], 
'Liberal': [150270263, 408072407, 234550882, 417389780, 1170770038208565248, 1707636642, 2852899113, 240786249, 1318671397560979456, 2937436849, 283226685, 45848808, 720579941184757760, 22849568, 1899063048, 579377522, 1646334073, 2242940071, 3257047456, 20199202, 2891740872, 488052222, 272185225, 1072270926, 3188558830, 282526718, 47692251, 205786669, 2678072299, 780323935, 2848993491, 276713213, 40550119, 29754743, 19634262, 2332742508, 272250877, 631988630, 61521038, 47338701, 4026045455, 415774799, 524557553, 2344419362, 2513973205, 1382336580518621186, 339752726, 911471588, 165812196], 
'NDP': [18681111, 59686058, 14079041, 2715275551, 377588094, 175259033, 215632349, 341866567, 196717787]
}

count = 0

for file in os.listdir(directory):
    count = count+1
    filename = os.fsdecode(file)
    G = nx.read_weighted_edgelist(dirname + '/' + filename, comments='#',
                     create_using=nx.DiGraph(), 
                     delimiter=' ', 
                     nodetype=int, 
                     encoding='utf-8')
    lib_cascade = run_cascade_metrics('liberal', active_nodes['Liberal'],G)
    con_cascade = run_cascade_metrics('conservative', active_nodes['Conservative'],G)
    ndp_cascade = run_cascade_metrics('ndp', active_nodes['NDP'],G)
    lgbt_cascade = run_cascade_metrics('lgbt', active_nodes['LGBTQ2S+'],G)
    bloq_cascade = run_cascade_metrics('bloq', active_nodes['Bloc'],G)

    data_frames = [lib_cascade, con_cascade, ndp_cascade, lgbt_cascade, bloq_cascade]

    df_merged = reduce(lambda  left,right: pd.merge(left,right,left_index=True, right_index=True,
                                                how='outer'), data_frames)
    df_merged.to_csv("{}_cascades.csv".format(filename))

    
    print("Files done {}".format(count))