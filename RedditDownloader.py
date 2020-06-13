import praw
import time
import youtube_dl
from praw_creds import client_id, client_secret, password, user_agent, username

def redditSearch(search_list,subreddit):

	# If subreddit is empty, change it to all (searches all subreddits)
	if not subreddit:
		subreddit = 'all'
	# If searchlist is empty, assuming you want to get new 25 from specific subreddit or just new 25.
	if not search_list:
		# Option 1 just gets new 25.
		print("+ Option 1")
		for sub in subreddit:
			sub = sub.strip()
			print(sub)
			for submission in reddit.subreddit(sub).new(limit=100):
				downloadVid(submission.url, sub)
	else:
		# Option 2 searches with your actual keyword
		print("+ Option 2")
		for search in search_list:
			if isinstance(subreddit, str):
				search = search.strip()
				subreddit = subreddit.strip()
				print(subreddit)
				for submission in reddit.subreddit(subreddit).search(search.lower()):
					downloadVid(submission.url, search + '-' + subreddit)
			if isinstance(subreddit, list):
				for sub in subreddit:
					search = search.strip()
					sub = sub.strip()
					print(sub)
					for submission in reddit.subreddit(sub).search(search.lower()):
						downloadVid(submission.url, search + '-' + sub)


# Downloads videos with youtube_dl library.
def downloadVid(url, file_loc):
	ydl_opts = {'outtmpl': './' + file_loc + '/%(title)s.%(ext)s'}
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url, ])
		print("+ Video Downloaded from {}".format(url))
	except Exception as exc:
		print(exc)

if __name__ == "__main__":

	# Variables
	delay = 4

	# Praw authentication, create a seperate praw_creds.py with this info.
	reddit = praw.Reddit(client_id=client_id, 
	                     client_secret=client_secret, 
	                     user_agent=user_agent,
	                     username=username, 
	                     password=password)

	# Authentication confirmation
	print("+ Authentication for " + str(reddit.user.me()) + " is verified. Proceeding.\r\n")

	# Search specific subreddit
	subred = input("# Enter a subreddit, I for import (from subreddit_list.py), multiple searches delimited by a comma (,) or leave blank for all: ")
	if ',' in subred:
		subred = subred.split(',')
	if subred == "I":
		from subreddit_list import subreddits
		subred = subreddits.split(',')
	# Search keyword.
	search_list = input("# Enter a search, multiple searches delimited by a comma (,) or leave blank: ")
	if search_list != '':
		search_list = search_list.split(',')

	# Print out searchlist
	print(search_list)

	# Returns a list of urls, and how many.
	redditSearch(search_list,subred)