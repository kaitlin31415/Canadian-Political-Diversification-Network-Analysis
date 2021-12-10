import tweepy
from datetime import datetime
import csv
import time

#developer data
api_key = ""
api_key_secret = ""
bearer_token = ""
access_token = ""
access_token_secret = ""

#sutup our auth object that will be used to make v1 calls
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

#create an api object to use v1 endpoints
api = tweepy.API(auth)

#client object to use v2 endpoints
client = tweepy.Client(bearer_token)

#authenticate with twitter
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


lines = [x.rstrip('\n') for x in open('data.txt','r')]


#code to get a list (max length 100) of users liking and retweeting a tweet
#tweet_id = 1447751344421412868
#likes = client.get_liking_users(tweet_id)
#rts = client.get_retweeters(tweet_id)

#query to get tweets from watame that are not a retweet
query1="from:" 
query2=" -is:retweet"

f = open('out.csv', 'w')
writer = csv.writer(f)

#since sept 20 2021 ,start_time="2021-09-20T00:0:00Z"
waiter = 0
for item in lines:
    query = (query1 + item + query2)
    data = client.search_recent_tweets(query)
    if data[0] != None:
        for tweet in data[0]:
            if waiter % 50 == 1:
                print("waiting....")
                for i in range (15):
                    print (str(15-i) + " minutes remaining")
                    time.sleep(60)
                time.sleep(15)
            tweet_id = tweet.id
            rt = api.get_retweets(tweet_id)
            waiter =+ 1
            retweets = (len(rt))
            line = (item + "," + str(tweet_id) + "," + str(retweets) + "\n")
            f.write(line)
            print(line)

#run the query in the search_recent_tweets endpoint and then print the ids from the results
#testing = client.search_recent_tweets(query)
#for item in testing[0]:
#    print(item.id)