__author__ = 'Brendan'

import json
import tweepy as twee
from pymongo import MongoClient
from dateutil.tz import tzutc
import numpy as np
import time
import csv
from http.client import IncompleteRead
from requests.packages.urllib3.exceptions import ProtocolError

#################33
# target usernames
username_filepath = 'senator twitter usernames.json'
k_tweets = 100 # get k tweets for each user (this is a bad way to sample, long term)

# twitter api info
consumer_key = "7M6nOHsYYKR4017OgL9DdgVtR"
consumer_secret = "WYNXMAOBTR37yENNVIPK3wVbFGlm17A7GOKhrFWmhRvnNADpEX"
access_token = "2569037840-pKDmLnVgJ6MHv8ikkQE3gyN2AbHV7C4ZoHadDLF"
access_token_secret = "ABbnsSv5Owzs6M0HVFYNUmH1KDiuBS9nmhGdloEUx49U5"

# mongodb stuff
client = MongoClient('mongodb://localhost:27017')
db = client['pymongo_twit_wrandom'] # specify/create database

###############3
#helper functions

def process_tweet(status):
    timestamp = status.created_at
    # convert to utc
    if timestamp.tzinfo:
        timestamp.astimezone(tzutc).replace(tzinfo=None)
    timestamp_serializeable = timestamp.isoformat() # serialize
    raw_text = status.text
    random_indices = np.random.rand(1,10) # for easy sampling

    tweet_info = {"screen_name":status.author.screen_name,
                 "created_at":timestamp_serializeable,
                 "raw_text":raw_text,
                 "random_indices":random_indices.tolist()}
                #"hyperlinks":links,
                 #"clean_text"

    return tweet_info

def add_entry_to_db(tweet_info):

    posts.insert_one(tweet_info) # posts is a global variable

#################333

# establish access to the tweepy api
auth = twee.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = twee.API(auth)

# establish the db
posts = db.posts  # sample entry
print "initial database: "
print db.posts

# load in username info
username_json_file = open(username_filepath, 'r')
username_dict = json.load(username_json_file) # has the fields 'senator_usernames' and 'senator_URLs'
username_json_file.close()


for username in username_dict['senator_usernames']:
    print username
    try:
        status_list = api.user_timeline(screen_name = username, count=k_tweets, include_rts = False) # get some tweets from this user
        for status in status_list:
            tweet_info = process_tweet(status)
            add_entry_to_db(tweet_info)

    except twee.error.TweepError:
        print "ERROR: probably an out of date username. Skipping."





# get past K tweets for the senators
#api.user_timeline(screen_name = 'danieltosh', count = 100, include_rts = True)




# visualize as a raster