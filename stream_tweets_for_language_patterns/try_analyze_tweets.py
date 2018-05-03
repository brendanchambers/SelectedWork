__author__ = 'Brendan'

import json
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
import igraph as ig

load_name = "sample_tweets_MLK.json"

loadfile = open(load_name,'r')
# read in from json file

tweetList = json.load(loadfile)
loadfile.close()

print "one entry"
print tweetList[0]
print tweetList[0]['screen_name']
print tweetList[0]['created_at']
print tweetList[0]['text']

########################################################################################
# helper function for grabbing the data and preprocessing

def tweetlist_to_words(json_tweet):

    ##### bag of words analysis
    #print json_tweet
    text_only = re.sub("[^a-zA-Z]",           # The pattern to search for
                          " ",                   # The pattern to replace it with
                          json_tweet['text'] )  # The text to search

    # notice that this isn't a good way of handling contractions
    # note is there some way to get rid of links beforehand - also note thtat some of these words are just characters from links...
            # and any nonsense strings are treated on equal footing with genuine dictionary words

    #text_full_string = " ".join(text_only)

    #print 'text from this tweet:'
    #print text_only

    lower_case = text_only.lower()
    words = lower_case.split()

    # remove common words (using nltk "stopwords" list
    exclusions = set(stopwords.words("english"))
    words_filtered = [w for w in words if not w in exclusions]
    #print words

    # todo "Porter Stemming" to merge simple postfix variations

    words_filtered = " ".join(words_filtered)
    #print " number of words " + str(len(words))
    return words_filtered


########################################################################################
# get content of tweets as a matrix, most-frequent words x counts in dimensions

clean_tweets = []
for tweet in tweetList:
    tweet_words = tweetlist_to_words(tweet)
    clean_tweets.append(tweet_words)

MAX_WORDS = 1000
num_tweets = len(clean_tweets)

print "count vectorizer..."
vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None,
                             max_features = MAX_WORDS)
tweet_vectors = vectorizer.fit_transform(clean_tweets)
tweet_vectors = tweet_vectors.toarray()
print tweet_vectors.shape

vocab = vectorizer.get_feature_names()
print vocab

word_counts = np.sum(tweet_vectors, axis=0)

# take a quick look at the common words and their counts
for tag, count in zip(vocab, word_counts):
    print count, tag

verboseplot = False
if verboseplot:
    plt.figure
    plt.imshow(tweet_vectors)
    plt.title('bags of words')
    plt.xlabel('words')
    plt.ylabel('tweets')
    plt.show()

#################################################################################################
# inverse document freq normalization:

print "inverse doc freq normalization..."
tweet_vectors_norm = np.zeros(np.shape(tweet_vectors))
for i_tweet in range(num_tweets):
    for i_word in range(np.shape(tweet_vectors)[1]):
        tweet_vectors_norm[i_tweet][i_word] = (tweet_vectors[i_tweet][i_word]*1.0) / word_counts[i_word] # make sure this is floating point division

if verboseplot:
    plt.figure
    plt.imshow(tweet_vectors_norm)
    plt.title('bag of words, normalized by count')
    plt.xlabel('words')
    plt.ylabel('tweets')
    plt.show()

############################################################################################
# look into community structure within this wordcount list

# these are symmetric links so just fill in the lower triangle (i > j)
print "computing word co-occurrences..."

words_together = np.zeros((MAX_WORDS, MAX_WORDS))
for idx,val in enumerate(tweet_vectors_norm):
    for i_word in range(MAX_WORDS):
        if val[i_word] > 0:
            for j_word in range(i_word+1,MAX_WORDS):
                if val[j_word] > 0:
                    words_together[i_word,j_word] += (val[i_word]*val[j_word]) # todo capture their null probability of co-occurrence

words_together = words_together + words_together.T # fill in the upper triangle
print "finished "

if verboseplot:
    plt.figure
    plt.imshow(words_together)
    plt.title('word co-occurrence matrix')
    plt.xlabel('words j')
    plt.ylabel('tweets')
    plt.show()

# find community structure by maximizing modularity with the partition:

# get the row, col indices of the non-zero elements in your adjacency matrix
conn_indices = np.where(words_together)
# get the weights corresponding to these indices
weights = words_together[conn_indices]
# a sequence of (i, j) tuples, each corresponding to an edge from i -> j
edges = zip(*conn_indices)
# initialize the graph from the edge sequence
G = ig.Graph(edges=edges, directed=False)

# assign node names and weights to be attributes of the vertices and edges
# respectively
G.vs['label'] = vocab
G.es['weight'] = weights

# I will also assign the weights to the 'width' attribute of the edges. this
# means that igraph.plot will set the line thicknesses according to the edge
# weights
#G.es['width'] = weights

# plot the graph, just for fun (oops need to install Cairo for this)
#igraph.plot(G, layout="rt", labels=True, margin=80)

# run the greedy community detection algorithm

print ig.summary(G)
print G.get_edgelist()[1:20]
print G.vs['label'][1:20]

# quick look at the degree histogram
NUMBINS = 20
if verboseplot:
    plt.figure()
    plt.hist(G.degree(),NUMBINS)
    plt.title('degree distribution for the word co-occurrences graph')
    plt.show()

print "finding high modularity communities..."
G_simple = G.simplify() # removes self loops and duplicate edges
word_dendrogram = G.community_fastgreedy()
print "word dendrogram " + str(word_dendrogram.merges)
word_communities = word_dendrogram.as_clustering() # n is an optional argument here fyi
print "word communities " + str(word_communities)

for i, community in enumerate(word_communities):
    print " community " + str(i)
    for idx in community:
        print vocab[idx] + " "
