import tweepy

api_key = ""
api_key_secret = ""
bearer_token = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)


#api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

client = tweepy.Client(bearer_token)
data = client.get_liking_users(1446894001722904576)

for item in data[0]:
    print(item)
