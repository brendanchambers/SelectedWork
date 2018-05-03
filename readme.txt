Selected projects and code samples
Brendan Chambers
Postdoctoral gap year

CONTENTS

Note: Developer authorizations and account info have been removed from this codebase, so anyone
wishing to run scripts requiring authorization will need to obtain their own credentials.

1. stream_tweets_for_language_patterns

	Project Overview: To sample ongoing twitter activity and identify
	user camps within a topic of interest:
	Use bag-of-words analysis to identify functional similarity among 
	active users. Cluster the resulting maps to identify content groups.

	Data was collected with the Twitter Streaming API,
	on Martin Luther King Jr Day 2017. Tweets were filtered on the string "MLK".
	Formal retweets were excluded from analysis.
	To gain insight into viral discussion sparked by a dispute between
	Senator John Lewis and President Donald Trump, analysis was restricted to
	users who mentioned "john lewis" or "lewis" during the sample window.

	Analysis of linguistic communities was performed using the igraph package,
	suggesting at least three major clusters based on word choice.
	Clusters were visualized using word clouds. Prominent words for the clusters
	are listed below. Future directions: employ cluster validation to select
	the optimal number of communities, scale up data collection using Hadoop 
	and MongoDB (as instantiated in try_mongo), analyze functional relationships
	among users using my dynamic network analysis methods.

	module 0 [community, black, equalityforall, always, floor, assassination]
	module 1 [allies, friends, better, bashing, evil, fend]
	module 2 [ethics, caused, fact, family, conservative, feel]

2. get_twitter neighborhood

	Project Overview: For a user of interest, obtain the subnetwork of their
	direct friends and followers.
	
	In this project, I lay the foundation for comparing users based on their structural
	connections. Twitter data rate limitations impose severe constraints the on the
	number of users who can be crawled in this fashion, so celebrities with large
	numbers of followers are difficult to reconstruct in full. Instead, I chose
	to sample their local neighborhood probablistically.

	To determine how to make the tradeoff between
	number of users sampled and running time, I check the
	in- and out-degree distributions for the local neighborhood,
	finding that very few users in the subnetwork
	studied here have more than 15,000 friends.
	
	Data is packaged into a JSON object, ready to be inserted into a database model
	of choice. These data are visualized as a simple force-directed graph
	with basic interactive function, using d3, in the directory 'viz'.

3. viz
	a. scientific visualization portfolio
		Some examples of my design work, excerpted from publication.
		All data for the visualizations were collected and analyzed
		by me, during my time in the MacLean Neurobiological Laboratory.
	b. d3_local_neighborhood
		Basic interactive visualization of the local network obtained above.
	c. d3_friend_spindle

4. web scraping
	Selected examples of web scraping approaches, using Beautiful Soup and 
	Selenium Web Driver.

5. w30 tutorials
	Some of my independent work to become more fluent in JavaScript.
	Approximately 25 tutorials following course materials developed by Wes Bos (@wesbos).

6. rnn sandbox
	Toy construction and training of LSTM networks in the Theano framework.
	LSTM networks are a powerful model for representing sequential data.
7. open ai gym sandbox
	Toy construction and training of PID control systems for open ai gym
	benchmark problems. 

8. custom matlab utilities
	A few of the tools I have developed for shared use in the MacLean Lab.
