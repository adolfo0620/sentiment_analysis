import requests

class reddit_api:
	def __init__(self):
		self.url_link = "http://www.reddit.com/.json"
		self.json = (requests.get(self.url_link)).json()

	def get_info(self):
		lposts = []
		print(self.json)
		list_of_post = self.json["data"]["children"]
		for post in list_of_post:
			author = post["data"]['author']
			subred = post["data"]['subreddit']
			title = post["data"]['title']
			ups = post["data"]['ups']
			url = post["data"]['url']
			created = post["data"]['created']
			lposts.append(subred +" "+title)
		return lposts



r = reddit_api()
r.get_info()