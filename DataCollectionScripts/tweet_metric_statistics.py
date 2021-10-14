import requests
import csv
import time

bearerToken=""

# Get the id from username 
filename="../data.txt"

userIdByUsernameUrl = "https://api.twitter.com/2/users/by/username/"

tweetsByUserIdURL = "https://api.twitter.com/2/users/USERID/tweets?max_results=100&start_time=2021-09-20T00:00:00.000Z&tweet.fields=public_metrics,created_at"

payload={}
headers = {
  'Authorization': 'Bearer ' + bearerToken
}
f = open('out.csv', 'w')
writer = csv.writer(f)

lines = [x.rstrip('\n') for x in open(filename,'r')]
count = 0
for user in lines:
    count = count + 1; 
    if (count % 50 == 0):
        #Sleep for 15 minutes
        for i in range(15):
            print("Idle wait time remaining: {} minutes".format(str(15 - i)))
            time.sleep(60)


    response = requests.request("GET", userIdByUsernameUrl+user, headers=headers, data=payload)


    personJson = response.json()
    id = personJson["data"]["id"]
    print("Name: {} ID: {}".format(user,id))

    # Get all tweets from that id
    tweetsURL = tweetsByUserIdURL.replace("USERID", str(id))
    response = requests.request("GET", tweetsURL, headers=headers, data=payload)
    #loop through each tweet in data 
    if ("data" in response.json()):
        for tweet in response.json()["data"]:
            f.write("{userid},{username},{tweetid},{retweetCount},{likeCount}\n".format(userid=id,username=user, tweetid=tweet["id"], retweetCount=tweet["public_metrics"]["retweet_count"], likeCount=tweet["public_metrics"]["like_count"]))


# get the retweet count, like count, & quote count and place in CSV