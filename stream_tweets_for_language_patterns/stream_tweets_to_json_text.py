__author__ = 'Brendan'


import tweepy as twee
import json
from datetime import datetime
from dateutil.tz import tzutc
import time
import csv
from http.client import IncompleteRead
from requests.packages.urllib3.exceptions import ProtocolError

# todo
# 1. put up on github
# 2. import json (use json dumps to write to text file)
KEYWORD = "MLK"
pause_time = 20 # pause time in minutes when reaching REST api call limit # todo think hard about sampling
max_tweets = 10000

#1)   create a listener class
class MyStreamListener(twee.StreamListener):

    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open('sample_tweets_MLK.json','a')
        self.maxtweets = max_tweets
        self.file.write("[")

    def on_status(self, status):
        #print([status.author.screen_name, status.created_at, status.text])

        #try:

            self.num_tweets += 1
            if self.num_tweets < self.maxtweets:
                timestamp = status.created_at
                # convert to utc
                if timestamp.tzinfo:
                    timestamp.astimezone(tzutc).replace(tzinfo=None)
                timestamp_serializeable = timestamp.isoformat() # serialize
                tweet_info = {"screen_name":status.author.screen_name,
                             "created_at":timestamp_serializeable,
                             "text":status.text} # possibly need to convert to utf-8 first
                                            # or store as json objects instead maybe? # update got this done
                json.dump(tweet_info,self.file, indent=4, sort_keys=True, separators=(',', ':'))
                if self.num_tweets < (self.maxtweets-1):
                    self.file.write(",")
                print 't ' + str(self.num_tweets)
                time.sleep(1) # minimum spacing of samples
                return True
            else:
                self.close_up_shop()
                return False


        #except Exception:
        #    print "caught error: " + str(Exception)

    def on_error(self, status_code):
        print "ERR"
        print status_code
        #if status_code == 420:
        #    return False #returning False in on_data disconnects the stream
        self.close_up_shop()
        return False

    def on_limit(self, status):
        print 'Limit threshold exceeded. Pausing. ' # , status
        time.sleep(60 * pause_time) # convert minutes to seconds
        #self.close_up_shop()
        return True

    def on_timeout(self, status):
        print 'Stream disconnected...'
        self.close_up_shop()
        return False

    def close_up_shop(self):
        self.file.write("]")
        self.file.close()


###############

print twee.__version__
# https://apps.twitter.com/app/13290014/keys
# owner  cpchiptabernacl
# ownerid  	2569037840

consumer_key = "obfuscated"
consumer_secret = "obfuscated"
auth = twee.OAuthHandler(consumer_key, consumer_secret)
access_token = "obfuscated"
access_token_secret = "obfuscated"
auth.set_access_token(access_token, access_token_secret)
api = twee.API(auth)

##################

#1b create stream writer (csv for now, json objects would be better, could use a noSQL database as well)
#f = open('testing.json','w')
#header = {"test":"check","testing":"chceck"}
#json.dump(header, f)


#2)   create a stream


#myStreamListener.set_writer(writer) # for writing csv output
#myStreamListener.set_file(f)\


# warning - the automatic restart is currently causing bad-formatting in the json database
#  this time around I just fixed the formatting by hand but todo fix this


#3)  start the stream
#elapsed = 0
#start = time.time()
#while elapsed < 5:
while True:
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
#    elapsed = (time.time() - start)

print "running async tasks"