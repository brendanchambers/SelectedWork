__author__ = 'Brendan'

import json
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import matplotlib.pyplot as plt
import igraph as ig
import scipy.spatial.distance as ssd
import scipy.cluster.hierarchy as clst

#load_name = "sample_tweets_MLK.json"
load_name = "MLK_stream_no-retweets.json"
loadfile = open(load_name,'r')
tweetList = json.load(loadfile) # read in the array of json objects
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

    # todo I think it would be good to exclude quoted text (such a different kind of relationship than word similarity)
    # by the same logic, would be good to exclude non-dictionary words (or words within some distance of dict words)

    words_filtered = " ".join(words_filtered)
    #print " number of words " + str(len(words))
    return words_filtered


########################################################################################
# get content of tweets as a matrix, most-frequent words x counts in dimensions

clean_tweets = []
for tweet in tweetList:
    tweet_words = tweetlist_to_words(tweet)
    clean_tweets.append(tweet_words)

MAX_WORDS = 200
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

verboseplot = True
if verboseplot:
    plt.figure
    plt.imshow(tweet_vectors,aspect='auto')
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
    plt.imshow(tweet_vectors_norm,aspect='auto')
    plt.title('bag of words, normalized by count')
    plt.xlabel('words')
    plt.ylabel('tweets')
    plt.show()

############################################################################################
# look into community structure in the neighborhood around John AND Lewis
#verboseplot = True
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

## todo instead of checking for equality, check for liklihood with typo models or hamming distance or something


##########################################################################################
# RESTRICT ANALYSIS TO NEAREST NEIGHBORS OF JOHN LEWIS
# TODO would be interesting to expand to next-nearest

# get the indices of John and Lewis
for i,word in enumerate(vocab):
    if word=="lewis":
        lewisIdx = i
    if word=="john":
        johnIdx = i
    if word=="johnlewis":
        lewisIdx = i
        johnIdx = i
print " john is at entry " + str(johnIdx) + " with " + str(word_counts[johnIdx]) +  " occurrences"
print " lewis is at entry " + str(lewisIdx) + " with " + str(word_counts[lewisIdx]) + " occurrences"

THRESH = 0 # consider using the expected noise floor or something
johnNeighbors = [i for i,val in enumerate(words_together[johnIdx,:]) if val > THRESH]
print johnNeighbors
lewisNeighbors = [i for i,val in enumerate(words_together[lewisIdx,:]) if val > THRESH] # i.e. connected to john
print lewisNeighbors
neighborhood = set(johnNeighbors).union(lewisNeighbors) # temp try union to get a bigger sample

# initialize the neighborhood subset
words_together_JL = np.zeros((len(neighborhood),len(neighborhood)))
tweet_vectors_JL = np.zeros((np.shape(tweet_vectors_norm)[0],len(neighborhood)))
for i,val1 in enumerate(neighborhood):
    tweet_vectors_JL[:,i] = tweet_vectors_norm[:,val1]
    for j,val2 in enumerate(neighborhood):
        words_together_JL[i][j] = words_together[val1][val2]
words_together = words_together_JL # rename for e-z re-usal of my community detection code
tweet_vectors_norm = tweet_vectors_JL # rename for consistency

############################################################################################

if verboseplot:
    plt.figure
    plt.imshow(words_together)
    plt.title('word co-occurrence matrix')
    plt.xlabel('words i')
    plt.ylabel('words j')
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

community_labels = np.zeros(len(G.vs))
print "make sure community labels are 1D, not square: " + str(np.shape(community_labels))
for i, community in enumerate(word_communities):
    print " community " + str(i)
    community_labels[community] = i # metadata for G
    for idx in community:
        print vocab[idx] + " "
    file_string = "lewis community " + str(i) + " noretweets.graphml"
    G_export = G.subgraph(community)
    G_export.write(file_string,format="graphml") # write subgraphs
######
# export for gephi

G.vs['community'] = community_labels
G.write("G lewis neighborhood noretweets.graphml",format="graphml") #write the full graph



####################################################################################
#    try to visualize the clustering the tweetwords matrix (as a sanity check sort of validation)


## order the words in the tweets x words display
word_clusteridxs = []
tweet_vectors_norm_orderedwords = np.zeros(np.shape(tweet_vectors_norm)) # initialize to the right size
words_together_orderedwords = np.zeros(np.shape(words_together))
i = 0
for community in word_communities:
    for wordidx in community:
        word_clusteridxs.append(wordidx)
        tweet_vectors_norm_orderedwords[:,i] = tweet_vectors_norm[:,wordidx]
        words_together_orderedwords[:,i] = words_together[:,wordidx]
        words_together_orderedwords[:,i] = words_together[wordidx,:]
        i += 1
print " number of words: " + str(i)

if verboseplot:
    plt.figure
    plt.imshow(words_together_orderedwords)
    plt.title('word co-occurrence matrix after ordering by modularity community')
    plt.xlabel('words i')
    plt.ylabel('words j')
    plt.show()

if verboseplot:
    plt.figure
    plt.imshow(tweet_vectors_norm_orderedwords,aspect='auto')
    plt.title('bag of words, normalized by count, ordered by word communities')
    plt.xlabel('words')
    plt.ylabel('tweets')
    plt.show()

# rank tweets by similarity - starting with just raw similarity, without resepect to modularity community
            # that way we come at this from a neutral stance on modularity, let's see if the effect is visible by eye
 # useful - https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html#module-scipy.cluster.hierarchy
    # hmmm nice way to take care of raw&col sort with networkx: https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.utils.rcm.reverse_cuthill_mckee_ordering.htmlp
print "finding L1 distances betwen tweets..."
tweet_distances = ssd.pdist(tweet_vectors_norm_orderedwords,'cityblock') # needs to M words by N tweets in dimensionality

# use squareform to go from nxn to nChoose2 format on the distance matrix
# distVec = ssd.squareform(tweet_distances) # nevermind pdist does the right thing
# build a dendogram to get sort indices
tweetlinkage = clst.linkage(tweet_distances,method='complete') # max distance linkage

if verboseplot:
    print "check tweet distances ' shape: " + str(np.shape(tweet_distances))
    print "check shape of tweet linkage: " + str(np.shape(tweetlinkage))
    #print tweetlinkage
    plt.figure()
    clst.dendrogram(tweetlinkage)
    plt.title('dendrogram for tweet distances in k-top-word idf space')
    plt.show()

leaflist = clst.leaves_list(tweetlinkage)
print "leaflist " + str(leaflist)
print str(len(leaflist)) + " leaves total"

tweet_vectors_norm_orderedboth = np.zeros(np.shape(tweet_vectors_norm_orderedwords)) # these names are getting totally out of hand
i=0
for i_leaf in leaflist:
    tweet_vectors_norm_orderedboth[i,:] = tweet_vectors_norm_orderedwords[i_leaf,:]
    i += 1

if verboseplot:
    plt.figure()
    plt.imshow(tweet_vectors_norm_orderedboth,aspect='auto')
    plt.title('ordered tweets by raw similarity, words by modularity community')
    plt.ylabel('tweets')
    plt.xlabel('words')
    plt.show()



