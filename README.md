# Canadian-Political-Diversification-Network-Analysis
Canadian Members of Parliament and Activist Organizations Twitter accounts retweets were analyzed for the brief period leading up to the 2021 federal elections. The object was to identify echo chambers that plague the scene and to find remedies in the form of bridge nodes that would serve to deliver a broader view for the people following. We believe doing so would reduce confirmation bias that is a leading cause for echo chambers, leading to a less polarized society. We found six main communities in Canadian politics, which we applied centrality measures, and information diffusion techniques to answer three research questions: 1. Given a user's interactions with political parties' tweets on Twitter, can we identify feedback loops created as a result of these politics-based interactions? 2. Can we identify activist organizations as non-partisan or partisan based on their interactions? 3. Can we identify users who have a wide breadth of interaction with different political groups? Our research helped us answer these questions to a certain extent, we can identify where the feedback loops are, place Activist Organizations on a political spectrum, and identify ways to combat confirmation bias by following certain Twitter accounts based on a few measures. We think this should help combat polarization in society and spark an open dialogue with people with different opinions.

## Dataset Description
### Data Cleaning 
Due to the limitations of the retweeting users’ endpoint, we could only obtain the latest 100 retweeting users of a tweet, however there were still tweets that had more than 100 retweets on them, which meant we were getting a subset of the users who interacted with that tweet. To avoid the situation of missing out on important connections we removed any MP or Activist Organization that had a tweet which got over 100 retweets over the time period of September 29, 2021, to October 13, 2021. 
### Data Collection
Data was collected using Twitter's Developer API, See `Polished Code/get_tweet_from_user.py` to see how the tweets were collected and `Polished Code/getnetwork.py` to see how the retweeting users were collected.

## Nodes 

## Edges 
