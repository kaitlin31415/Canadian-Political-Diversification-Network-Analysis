import csv

#this code was an attempt to mix communities and the network nodes. This was scraped and later done in Gephi
nodefile = [x.rstrip('\n') for x in open("Network export nodes 8.csv", "r")]
communityfile = [x.rstrip('\n') for x in open("nodeColours_Greedy_community_gamma_0.115_weighted.csv", "r")]

communitieslist = []
for i in range(len(communityfile)):
    communitieslist.append(communityfile[i].split(","))

communitiesrefrence = []
for item in communitieslist:
    communitiesrefrence.append(item[0])

nodeslist = []
for i in range(len(nodefile)):
    nodeslist.append(nodefile[i].split(","))

refinednodes = []
for i in nodeslist:
    refinednodes.append([i[0],i[6]])


f = open('communities_mapping.csv', 'w')
writer = csv.writer(f)

print(refinednodes[0])
print(communitieslist[0])
for node in refinednodes:
    if node[0] in communitiesrefrence:
        for item in communitieslist:
            if item[0] == node[0]:
                line = node[0] +"," + node[1] + "," +item[1] +"\n"
                f.write(line)

