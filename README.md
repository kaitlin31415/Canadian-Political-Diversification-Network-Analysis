# Canadian-Political-Diversification-Network-Analysis
Canadian Members of Parliament and Activist Organizations Twitter accounts retweets were analyzed for the brief period leading up to the 2021 federal elections. The object was to identify echo chambers that plague the scene and to find remedies in the form of bridge nodes that would serve to deliver a broader view for the people following. We believe doing so would reduce confirmation bias that is a leading cause for echo chambers, leading to a less polarized society. We found six main communities in Canadian politics, which we applied centrality measures, and information diffusion techniques to answer three research questions: 1. Given a user's interactions with political parties' tweets on Twitter, can we identify feedback loops created as a result of these politics-based interactions? 2. Can we identify activist organizations as non-partisan or partisan based on their interactions? 3. Can we identify users who have a wide breadth of interaction with different political groups? Our research helped us answer these questions to a certain extent, we can identify where the feedback loops are, place Activist Organizations on a political spectrum, and identify ways to combat confirmation bias by following certain Twitter accounts based on a few measures. We think this should help combat polarization in society and spark an open dialogue with people with different opinions.
## Research Paper
Read the research paper here: [Canadian Political Diversification Through Network Analysis](https://github.com/kaitlin31415/Canadian-Political-Diversification-Network-Analysis/blob/main/Research%20Paper/Canadian_Political_Diversification_Network_Analysis.pdf)
## Dataset Description
### Data Cleaning 
Due to the limitations of the retweeting users’ endpoint, we could only obtain the latest 100 retweeting users of a tweet, however there were still tweets that had more than 100 retweets on them, which meant we were getting a subset of the users who interacted with that tweet. To avoid the situation of missing out on important connections we removed any MP or Activist Organization that had a tweet which got over 100 retweets over the time period of September 29, 2021, to October 13, 2021. 
### Data Collection
Data was collected using Twitter's Developer API, See `Polished Code/get_tweet_from_user.py` to see how the tweets were collected and `Polished Code/getnetwork.py` to see how the retweeting users were collected.

### Nodes 
Nodes may be 
1. Activist Organization (AO): A group representing a cause in Canada. This Activist Organization may retweet other Activist Organizations or MP’s. 

2. Members of Parliament (MP): A member of a political party, has an affiliated party attached to this node. This MP may retweet other MP’s or Activist Organizations 

3. Retweeter: This is a user who has not been identified as an AO or MP, but rather is a user who retweets these other nodes. 

### Edges 
Edges are directed, they represent: “Source Retweets X tweets of Target” where X is a weight attached describing how many times Source retweeted Target. 

## Network Visualization
![Network Visualization](https://github.com/kaitlin31415/Canadian-Political-Diversification-Network-Analysis/blob/main/ReadMeImages/visualization.png)

## Basic Statistics

The network was comprised of 8984 nodes, and 14040 edges. Overall, the network is disconnected, containing 9 connected components, their sizes are: [8932, 10, 9, 8, 7, 4, 3]. The average path length of the largest connected component is 1.23 × 10-3 and its clustering coefficient is 9.61 × 10<sup>-3</sup>. This largest connected component was used as the size reference for the null models and is what the majority of the paper focuses on. The network displays properties of a scale free network as shown by the degree distributions. 

Out-degree Distribution: The out degree had a fit of γ = 2.21 this shows that the out degree distribution follows the power law fairly well. The error was 0.012 according to the powerlaw python library’s fit function 

## Experiments Run

### Community Analysis
Community analysis was done using the greedy_modularity_communities algorithm provided by NetworkX. We tried various resolution values to decrease the number of communities so we could have communities beyond only an MP or AO and their retweeters.  

Below is a summary of connections between communities:
![summary of intercommunity connections](https://github.com/kaitlin31415/Canadian-Political-Diversification-Network-Analysis/blob/main/ReadMeImages/Intercommunity_connection.PNG)
### Centrality Measures

1. In-Degree Centrality - which MPs and AOs are interacted with most, indicating the most popular MPs and A)s. 
2. Out-Degree Centrality - fy which retweeters are retweeting a lot of different MP’s and Activist Organizations.
3. Undirected Betweenness Centrality - what nodes are important in connecting groups together. Nodes with a high betweenness centrality are the ones that are more likely to interact with, or be interacted with multiple different communities 
4. Directed Betweenness Centrality - what MPs or activist groups are working to connect between groups in the network. 
5. Katz Centrality -  what nodes are influential in the network.

### Information Cascades
We proposed two experiments. The first was to mimic normal tweets in which two random nodes in the initial activation node set were identified and activated to see what communities information would pass through normally. The second experiment was where the starting nodes were all in on an announcement, and we disseminate information through them to find out who sees the message. This could mimic an announcement that all MPs were supposed to send out, but some forgot until they saw it on Twitter so just retweeted their fellow party member.

Below are visualizations from the large cascade:
![information cascades 1](https://github.com/kaitlin31415/Canadian-Political-Diversification-Network-Analysis/blob/main/ReadMeImages/cascade-1.PNG)

![information cascades 2](https://github.com/kaitlin31415/Canadian-Political-Diversification-Network-Analysis/blob/main/ReadMeImages/cascate-2.PNG)


