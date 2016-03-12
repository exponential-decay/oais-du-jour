import os 
import sys
from twitter import *

class HandleTwitter:

   #Twitter pieces
   def twitter_authentication(self):
	   CONSUMER_KEYS = os.path.expanduser('.twitter-consumer-keys')
	   CONSUMER_KEY, CONSUMER_SECRET = read_token_file(CONSUMER_KEYS)

	   MY_TWITTER_CREDS = os.path.expanduser('.twitter-oais-du-jour-credentials')
	   if not os.path.exists(MY_TWITTER_CREDS):
		   oauth_dance("oais-du-jour", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

	   oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
	   twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
	
	   return twitter

   def tweet_update(self, tweet):
      sys.stderr.write(str(len(tweet)) + " " + tweet   + "\n")
      self.twitter.statuses.update(status=tweet)

   def __init__(self):
      self.twitter = self.twitter_authentication()
