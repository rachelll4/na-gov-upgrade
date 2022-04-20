import tweepy
import json
import os
import requests
from requests_oauthlib import OAuth1Session

#Add your credentials here
twitter_keys = {
        'consumer_key':        os.environ.get('TWEEPY_API_KEY'),
        'consumer_secret':     os.environ.get('TWEEPY_API_SECRET'),
        'access_token_key':    os.environ.get('TWEEPY_ACCESS_TOKEN'),
        'access_token_secret': os.environ.get('TWEEPY_ACCESS_TOKEN_SECRET'),
        'bearer_token': os.environ.get('TWEEPY_BEARER_TOKEN')
    }

# client = tweepy.Client(consumer_key = twitter_keys['consumer_key'],
                        # consumer_secret = twitter_keys['consumer_secret'],
                        # access_token = twitter_keys['access_token_key'],
                        # access_token_secret = twitter_keys['access_token_secret'],
                        # bearer_token = twitter_keys['bearer_token'] )

# payload = "Hello world! This is an automated tweet!"

# response = client.create_tweet( text = payload )
# print(response)

#Setup access to API
# NEED API V1 WITH OAUTH V2
# https://docs.tweepy.org/en/stable/authentication.html#oauth-2-0-bearer-token-app-only
auth = tweepy.OAuth2BearerHandler(bearer_token = twitter_keys['bearer_token'])
#auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
#auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])
api = tweepy.API(auth)

response = api.home_timeline()
print(response)

## this is oauth v2, need v1 which is tweepy.Client.create_tweet(tweet)
#client = tweepy.Client(bearer_token='REPLACE_ME')
#https://docs.tweepy.org/en/stable/client.html#tweepy.Client.create_tweet
#payload = "Hello world! This is an automated tweet!"
#api.update_status(payload)

# # Get request token
# request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
# oauth = OAuth1Session(twitter_keys['consumer_key'], client_secret=twitter_keys['consumer_secret'])

# # Making the request
# response = oauth.POST(
    # "https://api.twitter.com/2/tweets",
    # json=payload,
# )

# if response.status_code != 201:
    # raise Exception(
        # "Request returned an error: {} {}".format(response.status_code, response.text)
    # )

# print("Response code: {}".format(response.status_code))

# # Saving the response as JSON
# json_response = response.json()
# print(json.dumps(json_response, indent=4, sort_keys=True))


# try:
    # fetch_response = oauth.fetch_request_token(request_token_url)
# except ValueError:
    # print(
        # "There may have been an issue with the consumer_key or consumer_secret you entered."
    # )

#resource_owner_key = fetch_response.get("oauth_token")
#resource_owner_secret = fetch_response.get("oauth_token_secret")
#print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
#base_authorization_url = "https://api.twitter.com/oauth/authorize"
#authorization_url = oauth.authorization_url(base_authorization_url)
#print("Please go here and authorize: %s" % authorization_url)
#verifier = input("Paste the PIN here: ")

# # Get the access token
# access_token_url = "https://api.twitter.com/oauth/access_token"
# oauth = OAuth1Session(
    # twitter_keys['consumer_key'],
    # client_secret=twitter_keys['consumer_secret'],
    # resource_owner_key=resource_owner_key,
    # resource_owner_secret=resource_owner_secret,
    # verifier=verifier,
# )
# oauth_tokens = oauth.fetch_access_token(access_token_url)

# access_token = oauth_tokens["oauth_token"]
# access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
#oauth = OAuth1Session(
#    twitter_keys['consumer_key'],
#    client_secret=twitter_keys['consumer_secret'],
#    resource_owner_key=twitter_keys['access_token_key'],
#    resource_owner_secret=twitter_keys['access_token_secret'],
#)

