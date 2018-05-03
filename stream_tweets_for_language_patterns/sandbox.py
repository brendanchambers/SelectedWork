__author__ = 'Brendan'


import tweepy as twee
import csv

# todo
# 1. put up on github
# 2. import json (use json dumps to write to text file)

#1)   create a listener class
class MyStreamListener(twee.StreamListener):

    def on_status(self, status):
        #print([status.author.screen_name, status.created_at, status.text])

        try:
            tweet_info = [status.author.screen_name] # , str(status.created_at), str(status.text)] # convert to utf-8 first
                                        # or store as json objects instead maybe?
            print tweet_info
            self.writer.writerow(tweet_info)
        except:
            print "error"

    def on_error(self, status_code):
        print "ERR"
        print status_code
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

    def set_writer(self, csv_writer):
        self.writer = csv_writer
        #self.writer.writerow(header)
        #self.writer.writerow('')
        print "nullification and devourment"

###############

print twee.__version__
# https://apps.twitter.com/app/13290014/keys
# owner  cpchiptabernacl
# ownerid  	2569037840

consumer_key = "7M6nOHsYYKR4017OgL9DdgVtR"
consumer_secret = "WYNXMAOBTR37yENNVIPK3wVbFGlm17A7GOKhrFWmhRvnNADpEX"
auth = twee.OAuthHandler(consumer_key, consumer_secret)
access_token = "2569037840-pKDmLnVgJ6MHv8ikkQE3gyN2AbHV7C4ZoHadDLF"
access_token_secret = "ABbnsSv5Owzs6M0HVFYNUmH1KDiuBS9nmhGdloEUx49U5"
auth.set_access_token(access_token, access_token_secret)
api = twee.API(auth)

##################

#1b create stream writer (csv for now, json objects would be better, could use a noSQL database as well)
f = open('test.txt','w')
writer = csv.writer(f,delimiter=' ',escapechar='',quoting=csv.QUOTE_NONE) # pass to the listener below
header = ['Author,Date,Text']
writer.writerow(header) # todo variable scope problems? why isn't it writing
writer.writerow(header)

#2)   create a stream
myStreamListener = MyStreamListener()

myStreamListener.set_writer(writer) # for writing csv output

myStream = twee.Stream(auth = api.auth, listener=myStreamListener)

#3)  start the stream
myStream.filter(track=['chicago'], async=True)
