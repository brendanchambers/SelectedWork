__author__ = 'Brendan'

# I'm noticing the cascading retweet structure of this dataset
# think I remember reading about that, todo take a look at hierarchical retweets in social science literature

# 1. in the meantime try to grab a single retweet tree and visualize it
# 2. work towards plotting retweet trees and word-similarity relationships among their root nodes

###################################
import json
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
import igraph as ig

###############################
# grab the tweets and their users # todo use elastic search in later iterations

load_name = "sample_tweets_MLK.json"
print 'loading tweets from json text'
loadfile = open(load_name,'r')
# read in from json file

tweetList = json.load(loadfile)
loadfile.close()

#print "first entry"
#print tweetList[0]
#print tweetList[0]['screen_name']
#print tweetList[0]['created_at']
#print tweetList[0]['text']

################################
# set up a smarter infrastructure to search if necessary

# alphabetical by screen name? tree?             keep it simple for now
# temporal order by 'created_at'
# alphabetical by tweet text

screen_names = []
for entry in tweetList:
    screen_names.append(entry['screen_name'].lower())             # lower case only


################################################
# helper functions

# todo have this function return a dictionary containing user as well as text
def grab_RT_user(tweet): # if a tweet begins with the prefix "RT", grab ther username which immediately follows
    RT_user = None
    words = tweet['text'].split()
    if words[0]=="RT":
        RT_user = words[1]
        if RT_user[0]=='@': # sometimes the @ sign gets left off so handle this case
            RT_user = RT_user[1:]
        if RT_user[-1]==':':
            RT_user = RT_user[:-1]
    return RT_user

def searchUp(tweet_ref):   # find a parent or return []

    # check if it's a retweet
    print tweet_ref['text'][0:2]
    prefix = tweet_ref['text'][0:2]
    if prefix == "RT":
        isRT = True

        # grab the parent user and text
        parentUser = grab_RT_user(tweet_ref)

        words = tweet_ref['text'].split() # we knw this will yield at least 3 words from the structure of a retweet
        parentText = ' '.join(words[2:])
    else:
        isRT = False
        parentUser = "Null"
        parentText = "Null"
    print "parent user: " + parentUser
    print "parent text: " + parentText

    # attempt to find parent in database
    print "checking for candidate parents based on username..."
    candidateTweets = []
    for i,tweet in enumerate(tweetList):
        if tweet['screen_name']==parentUser:
            candidateTweets.append(i)
    print "candidate parents " + str(candidateTweets)

    # make a lazy check for equality on the tweet itself
    parentTweet = None
    for idx in candidateTweets:
        if tweetList[idx]['text']==parentText:
            parentTweet = idx
            print "found parent tweet: " + tweetList[idx]['text']

    return parentTweet # todo probably will have to do a better job keeping track of indices too

def searchDown(tweet_ref):
    print tweet_ref
    print tweet_ref['screen_name']
    children = []
    for idx,child_candidate in enumerate(tweetList):     # this is an expesive search, obviously - could use smarter data type or elastic database
        child_text = child_candidate['text']
        if child_text[0:2]=="RT":
            RT_user = grab_RT_user(child_candidate)
            if RT_user == tweet_ref['screen_name']: # if this child retweeted from the reference user
                words = child_candidate['text'].split()
                childText = ' '.join(words[2:])
                if childText==tweet_ref['text']: # if the child retweeted THIS text from the ref user
                    children.append(idx)
    return children









#################################
# traverse a retweet tree (if applicable)

idx = np.random.randint(0,len(tweetList)) # grab a random tweet
tweet_ref = tweetList[idx]
print "reference tweet: "
print tweet_ref['screen_name']
print tweet_ref['created_at']
print tweet_ref['text']

parentTweet = searchUp(tweet_ref)

#################################
# traverse a retweet tree (if applicable)

idx = np.random.randint(0,len(tweetList)) # grab a random tweet
tweet_random = tweetList[idx]

print "random tweet: "
print tweet_random['screen_name']
print tweet_random['created_at']
print tweet_random['text']

# check if it's a retweet:
if tweet_random['text'][0:2] == "RT":
    print "random tweet is a retweet"

    print 'getting parent of ref tweet...'
    parentTweet = searchUp(tweet_random)          #
    print 'finding other re-tweeters in this tree...'
    if parentTweet is not None:                         # is the parent tweet in this database

        print "parent text: " + parentTweet['text']
        childrenIdxs = searchDown(parentTweet)       # find the rest of this retweet tree

    else:
        print "parent not found in database."
        print "checking for other nodes in this retweet tree"

        text = tweet_random['text'][2:] # pick off 'RT'  # could re-organize this a little more cleanly todo
        words = text.split()
        parent_user = words[0][1:-1] # pick off '@' and ':'
        parent_text = ' '.join(words[1:])
        pseudoParent = {"screen_name":parent_user,"text":parent_text}

        childrenIdxs = searchDown(pseudoParent)

    print 'child nodes: '
    for idx in childrenIdxs:
         print tweetList[idx]

else: # not a retweet
    print "random tweet does not appear to be a retweet"




# todo what fraction of tweets in this databse are retweets
# how many retweet trees are there
# how many unique parents and never-retweeted tweets are there

# todo plotting

