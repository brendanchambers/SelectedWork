__author__ = 'Brendan'


from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['pymongo_twit_test'] # specify/create database

posts = db.posts  # sample entry
print "initial database: "
print db.posts

'''
post_data = {
    'title': 'My database entry',
    'content': 'somewhat disappointing',
    'author': 'Ywwh'
}
#result = posts.insert_one(post_data)
#print('One post: {0}'.format(result.inserted_id))

test_fetch = posts.find_one({'author':'Ywwh'})
print test_fetch
'''

# get a small batch of tweets



# write them to a database