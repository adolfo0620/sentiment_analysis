import requests

class reddit_api:
	def __init__(self,subred):
		if subred == " ":
			self.url_link = "http://www.reddit.com/.json"
		else:
			self.url_link = "http://www.reddit.com/"+ subred +"/.json?limit=1000"
		
		bot = {"User-Agent": "sentiment bot by /u/adolfo0620"}
		
		self.json = (requests.get(self.url_link,headers=bot)).json()

	def get_info(self):
		lposts = []
		list_of_post = self.json["data"]["children"]
		for post in list_of_post:
			subred = post["data"]['subreddit']
			title = post["data"]['title']
			ups = post["data"]['ups']
			lposts.append(subred +" "+title)
			print(subred)
			print(title)
		return lposts
