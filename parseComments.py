import json
import os
import sets


# Recursive function to read comments
def readComments(obj, commentCount, subreddit, comment_corpus, user_links):
	newComments = 0
	existingComments = 0
	for i in obj:

		if 'data' not in i:
			return

		# Basic info, present both in Title and Comment
		commentId = i['data']['id']
		content = ""
		author = ""
		url = ""
		score = 0
		created = 0
		if 'created_utc' in i['data']:
			created = i['data']['created_utc']
		else:
			print "*** WARNING: created_utc not found in this record -> " + commentId

		# Is it a comment?
		if 'body' in i['data']:

			content = i['data']['body']
			ups = int(i['data']['ups'])
			downs = int(i['data']['downs'])
			author = i['data']['author']

			score = ups - downs

		# Or is it the title post?
		elif 'selftext' in i['data']:

			url = i['data']['url']
			content = i['data']['selftext']
			score = i['data']['score']

		# add contents to the comment corpus
		if subreddit in comment_corpus:
			temp_content = ' ' + content
			comment_corpus[subreddit] += temp_content
		else:
			comment_corpus[subreddit] = content

		# Update user links
		if author in user_links:
			user_links[author].add(subreddit)
		else:
			user_links[author] = {subreddit}

		#print author + ' ' + content + '\n'
		#commentCount = commentCount + 1
		#print commentCount

		# Does it have a reply?
		if 'replies' in i['data']:
			if len(i['data']['replies']) > 0:
				readComments(i['data']['replies']['data']['children'], commentCount, subreddit, comment_corpus, user_links)

directory = './r'
comment_corpus = {}
user_links = {}
for subreddit in os.listdir(directory):
	if subreddit != '.DS_Store':
		print(subreddit)
		for my_file in os.listdir(directory+'/'+subreddit):
			#print subreddit + ' ' + my_file
			json_data = open(directory+'/'+subreddit+'/'+my_file)
			try:
				commentThread = json.load(json_data)
			except ValueError:
				continue
			commentCount = 0
			readComments(commentThread[1]['data']['children'], commentCount, subreddit, comment_corpus, user_links)

#print(comment_corpus)

# Format user link output to file
# in format:
#		subreddit1 subreddit2
# This represents two links, one going each direction.
ul = open('userLinks.txt', 'w')
subreddit = set()

for user in user_links:
	subs = list(user_links[user])
	for x in xrange(len(subs)):
		for y in range(x+1, len(subs)):
			temp = [subs[x], subs[y]]
			temp.sort()
			tmp = (temp[0], temp[1])
			subreddit.add(tmp)

for pair in subreddit:
	line = pair[0] + ' ' + pair[1] + '\n'
	ul.write(line)

