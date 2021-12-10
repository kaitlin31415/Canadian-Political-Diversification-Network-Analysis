import sys

from pandas.io.parsers import count_empty_vals
import networkx as nx
import pandas as pd
import os
groupname = sys.argv[1]

clustering_filename = "{}_avg_clustering.csv".format(groupname)

apl_filename = "{}_apl.csv".format(groupname)

deg_cen_pd = "{}_deg_cen_df.csv".format(groupname)
in_deg_cen_pd = "{}_out_deg_cen_df.csv".format(groupname)
out_deg_cen_pd = "{}_in_deg_cen_df.csv".format(groupname)
eigenvector_cen_pd = "{}_eigenvector_cen_df.csv".format(groupname)
betweenness_cen_pd = "{}_betweenness_cen_df.csv".format(groupname)

clustering_pd = "{}_clustering_df.csv".format(groupname)

def persist_first_to_csv(centrality_dict, filename,columnname):
    curr = pd.DataFrame.from_dict(centrality_dict, orient="index", columns = [columnname])
    curr.to_csv(filename)

def persist_centrality_to_csv(centrality_dict, filename,columnname):
    #open the current csv
    persisted = pd.read_csv(filename)
    curr = pd.DataFrame.from_dict(centrality_dict, orient="index", columns = [columnname])
    persisted = persisted.set_index("Unnamed: 0")
    persisted = persisted.merge(curr, left_index=True, right_index=True)
    persisted.to_csv(filename)

dirname = sys.argv[2]
directory = os.fsencode(dirname)

average_shortest_paths = []
average_clustering = []

count = 0
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    G = nx.read_edgelist(dirname + '/' + filename, comments='#',
                     create_using=nx.DiGraph(), 
                     delimiter=' ', 
                     nodetype=int, 
                     encoding='utf-8')
    file_object = open(clustering_filename, 'a')
	# Append 'hello' at the end of file
    file_object.write(str(nx.average_clustering(G))+"\n")
	# Close the file
    file_object.close()	

    file_object = open(apl_filename, 'a')
	# Append 'hello' at the end of file
    file_object.write(str(nx.average_shortest_path_length(G))+"\n")
	# Close the file
    file_object.close()			

		 
    if (count == 0):
        persist_first_to_csv(nx.clustering(G),clustering_pd,filename)
        persist_first_to_csv(nx.degree_centrality(G),deg_cen_pd,filename)
        persist_first_to_csv(nx.in_degree_centrality(G),in_deg_cen_pd,filename)
        persist_first_to_csv(nx.out_degree_centrality(G),out_deg_cen_pd,filename)
        persist_first_to_csv(nx.betweenness_centrality(G,k=None, normalized=True),betweenness_cen_pd,filename)
    else:
        persist_centrality_to_csv(nx.clustering(G),clustering_pd,filename)
        persist_centrality_to_csv(nx.degree_centrality(G),deg_cen_pd,filename)
        persist_centrality_to_csv(nx.in_degree_centrality(G),in_deg_cen_pd,filename)
        persist_centrality_to_csv(nx.out_degree_centrality(G),out_deg_cen_pd,filename)
        persist_centrality_to_csv(nx.betweenness_centrality(G,k=None, normalized=True),betweenness_cen_pd,filename)
    count = count + 1
	
    print("Files done {}".format(count))



