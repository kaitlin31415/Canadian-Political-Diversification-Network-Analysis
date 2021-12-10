import sys

from pandas.io.parsers import count_empty_vals
import networkx as nx
import pandas as pd
import os

#stuff for making files
groupname = sys.argv[1]

clustering_filename = "{}_avg_clustering.csv".format(groupname)

apl_filename = "{}_apl.csv".format(groupname)

katz_cen_pd = "{}_katz_cen.csv".format(groupname)


clustering_pd = "{}_clustering_df.csv".format(groupname)

#functions to write to csv
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

#get the directory
dirname = sys.argv[2]
directory = os.fsencode(dirname)

#initialize varaibles
average_shortest_paths = []
average_clustering = []

count = 0
#go through all the files in the directory and pull the desired statistics ans write them to file
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    G = nx.read_weighted_edgelist(dirname + '/' + filename, comments='#',
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
        persist_first_to_csv(nx.clustering(G),clustering_pd,"filename")
        try:
            persist_first_to_csv(nx.algorithms.centrality.katz_centrality_numpy(G, weight="data"),katz_cen_pd,filename)
        except PowerIterationFailedConvergence:
            print("Could not converge on a value for file:" + filename)
            continue
    else:
        persist_centrality_to_csv(nx.clustering(G),clustering_pd,filename)
        try:
            persist_centrality_to_csv(nx.algorithms.centrality.katz_centrality_numpy(G, weight="data"),katz_cen_pd,filename)
        except PowerIterationFailedConvergence:
            print("Could not converge on a value for file:" + filename)
            continue
    count = count + 1
	
    print("Files done {}".format(count))



