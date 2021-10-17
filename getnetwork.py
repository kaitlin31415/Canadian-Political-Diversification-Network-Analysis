import tweepy
import csv
import time

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


lines = [x.rstrip('\n') for x in open('validTweets_1.csv','r')]
blah = []

for var in lines:
    blah.append((var.split(",")))

#blah[0][3]

#code to get a list (max length 100) of users liking and retweeting a tweet
#tweet_id = 1447751344421412868
#likes = client.get_liking_users(tweet_id)
#rts = client.get_retweeters(tweet_id)

#query to get tweets from watame that are not a retweet
query1="from:" 
query2=" -is:retweet"

f = open('output.csv', 'w')
writer = csv.writer(f)


timeout = 0
for item in blah:

    timeout += 1
    if timeout % 50 == 1:
        print("waiting....")
        for i in range (16):
            print (str(15-i) + " minutes remaining")
            time.sleep(60)
    tweetid = item[3]
    data = client.get_retweeters(tweetid)
    retweeters = data[0]
    if retweeters != None:
        for user in retweeters:
            line = (str(tweetid) + "," + str(user.id) +"\n")
            f.write(line)
            print(line)
            print(timeout)
