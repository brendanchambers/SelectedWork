__author__ = 'Brendan'


import tweepy as twee
import json
from datetime import datetime
from dateutil.tz import tzutc
import time
import csv
from http.client import IncompleteRead
from requests.packages.urllib3.exceptions import ProtocolError
from pymongo import MongoClient

##########################################
KEYWORD = "moore"
pause_time = 20 # pause time in minutes when reaching REST api call limit # todo think hard about sampling
max_tweets = 10
MIN_SPACING = 1 # sleep time after each call (to control calls per second)
json_target_string = 'sample_tweets_moore.json'
TIME_LIMIT = 2 # (seconds) stream calls initiated before TIME_LIMIT, then finish the final stream iteration

consumer_key = "7M6nOHsYYKR4017OgL9DdgVtR"
consumer_secret = "WYNXMAOBTR37yENNVIPK3wVbFGlm17A7GOKhrFWmhRvnNADpEX"
access_token = "2569037840-pKDmLnVgJ6MHv8ikkQE3gyN2AbHV7C4ZoHadDLF"
access_token_secret = "ABbnsSv5Owzs6M0HVFYNUmH1KDiuBS9nmhGdloEUx49U5"

client = MongoClient('mongodb://localhost:27017')
db = client['pymongo_twit_test2'] # specify/create database

CLEAR_DATABASE = True
##########################################

#1)   create a listener class
class MyStreamListener(twee.StreamListener):

    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open(json_target_string,'a')
        self.maxtweets = max_tweets
        self.file.write("[")

    def on_status(self, status):
        #print([status.author.screen_name, status.created_at, status.text])

        #try:

        if hasattr(status,'retweeted_status'):
            print 'retweet: '
            print status.text
        else: # if the tweet is not a retweet, add it to the database
            if self.num_tweets < self.maxtweets:
                timestamp = status.created_at
                # convert to utc
                if timestamp.tzinfo:
                    timestamp.astimezone(tzutc).replace(tzinfo=None)
                timestamp_serializeable = timestamp.isoformat() # serialize
                raw_text = status.text

                tweet_info = {"screen_name":status.author.screen_name,
                             "created_at":timestamp_serializeable,
                             "raw_text":raw_text} #,
                             #"hyperlinks":links,
                             #"clean_text"
                             #"text":status.text} # possibly need to convert to utf-8 first
                # todo separate text and links
                # todo put this into a mongo db instead
                self.write_to_db(tweet_info)
                '''
                json.dump(tweet_info,self.file, indent=4, sort_keys=True, separators=(',', ':'))
                self.num_tweets += 1
                if self.num_tweets < (self.maxtweets-1):
                    self.file.write(",")
                print 't ' + str(self.num_tweets)
                '''
                time.sleep(MIN_SPACING) # minimum spacing of samples
                return True
            else: # full batch of tweets successfully collected
                self.close_up_shop()
                return False


        #except Exception:
        #    print "caught error: " + str(Exception)
    def write_to_db(self, tweet_info):
        posts.insert_one(tweet_info)
        #json.dump(tweet_info,self.file, indent=4, sort_keys=True, separators=(',', ':'))
        self.num_tweets += 1
        #if self.num_tweets < (self.maxtweets-1):
        #    self.file.write(",")
        print 't ' + str(self.num_tweets)

    def on_error(self, status_code):
        print "ERR"
        print status_code
        #if status_code == 420:
        #    return False #returning False in on_data disconnects the stream
        self.close_up_shop()
        return False

    def on_limit(self, status):
        print 'Limit threshold exceeded. Pausing... ' # , status
        time.sleep(60 * pause_time) # convert minutes to seconds
        #self.close_up_shop()
        return True

    def on_timeout(self, status):
        print 'Stream disconnected on timeout...'
        self.close_up_shop()
        return False

    def close_up_shop(self):
        print 'Closing stream...'
        self.file.write("]")
        self.file.close()


###############

print twee.__version__
# https://apps.twitter.com/app/13290014/keys
# owner  cpchiptabernacl
# ownerid  	2569037840



auth = twee.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = twee.API(auth)

##################




posts = db.posts  # sample entry
print "initial database: "
print db.posts

##################################

elapsed = 0
start = time.time()
while elapsed < TIME_LIMIT:
    try:
        # Connect/reconnect the stream
        myStreamListener = MyStreamListener()
        myStream = twee.Stream(auth = api.auth, listener=myStreamListener)
        # DON'T run this approach async or you'll just create a ton of streams!
        myStream.filter(track=[KEYWORD], async=False)

    except ProtocolError:
        print "excepted protocol error"
        time.sleep(10)
        # Oh well, reconnect and keep trucking
        continue
               # wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    elapsed = (time.time() - start)

print "running async tasks"
print "dumping database contents: "
print db.posts