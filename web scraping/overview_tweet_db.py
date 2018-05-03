__author__ = 'Brendan'

# make a raster plot

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pymongo import MongoClient
import numpy as np
from dateutil.tz import tzutc
import dateutil.parser
import time

client = MongoClient('mongodb://localhost:27017')
db = client['pymongo_twit_wrandom'] # specify/create database

K_usernames = 5 # sample k entries for displaying timing

tweet_times = {}
username_list = []

for entry in db.posts.find():
    username = entry['screen_name']
    event_time = entry['created_at'] # temp
    if username in tweet_times:
        tweet_times[username].append(event_time)
    else:
        tweet_times[username] = []
        username_list.append(username)

plt.figure()
ylabels = []
yticks = []

for idx,username in enumerate(tweet_times):
    ylabels.append(username)
    yticks.append(idx)
    print username
    tweet_time_list = [dateutil.parser.parse(tweet_time) for tweet_time in tweet_times[username]]
    #print tweet_time_list

    row_color = [0.5,0,0.5]        # todo color code by party
    num_ticks = len(tweet_times[username])
    xx = idx*np.ones((1,num_ticks))
    #yy = mdates.date2num(my_datetime)
    plt.scatter(tweet_time_list,xx,color=row_color,marker='|') # todo want these to be taller
    # plot a row

# todo make the ylabels usernames
plt.title('timing of tweets in database')
plt.gcf().autofmt_xdate()
axarr = plt.gca()
axarr.set_yticks(yticks)
axarr.set_yticklabels(ylabels)
plt.show()



# grab a few random tweets from the database
#// Get one random document from the mycoll collection.
#OFFSET = 5 # todo choose this randomly to select a random sliding window of samples (this isn't a great sampling method)
#rand_cohort = db.posts.find().skip(OFFSET).limit(K_usernames)

N_users = len(tweet_times)
user_subset_idxs = np.random.randint(0,N_users,K_usernames)


plt.figure()
f, axarr = plt.subplots(K_usernames, sharex=True, sharey=False)

for user_subset_idx,user_idx in enumerate(user_subset_idxs):
    ylabels = []
    yticks = []
    #plt.subplot((K_usernames,1,user_subset_idx))
    username = username_list[user_idx]
    tweet_time_list = [dateutil.parser.parse(tweet_time) for tweet_time in tweet_times[username]]

    xx = np.zeros((1,len(tweet_times[username])))
    #ylabels.append(username)
    #yticks.append(user_subset_idx)
    ax = axarr[user_subset_idx]
    ax.scatter(tweet_time_list,xx,color=[0.25, 0.25, 0],marker='|')  # todo express this as tweets / day by convolving
    ax.set_yticks([])
    ax.set_ylabel(username,rotation='horizontal', ha='right')

ax = plt.gca()
xticks = ax.get_xticks()
xlabel = ax.get_xlabel()



f.add_subplot(111, frameon=False)
# hide tick and tick label of the big axes
plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
plt.grid(False)
plt.xticks(xticks)
plt.xlabel(xlabel)
plt.gcf().autofmt_xdate()
plt.title('timecourse of tweeting for a few random users')
plt.show()
