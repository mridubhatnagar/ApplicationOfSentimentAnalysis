#program to fetch tweets from twitter and stores  in MySQL database

from textblob import TextBlob
import mysql.connector
import tweepy
from tweepy import OAuthHandler
import json
import time

#tweet1 = {'id_str': '800598686568947712', 'entities': {'symbols': [], 'hashtags': [{'text': 'AdjustNoMore', 'indices': [118, 131]}], 'user_mentions': [{'screen_name': 'amazonIN', 'id': 1282946089, 'id_str': '1282946089', 'name': 'Amazon.in', 'indices': [0, 9]}, {'screen_name': 'AmazonHelp', 'id': 85741735, 'id_str': '85741735', 'name': 'Amazon Help', 'indices': [10, 21]}], 'urls': []}, 'retweet_count': 0, 'geo': None, 'truncated': False, 'retweeted': False, 'source': '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', 'created_at': 'Mon Nov 21 07:16:15 +0000 2016', 'favorited': False, 'place': None, 'in_reply_to_status_id_str': None, 'is_quote_status': False, 'in_reply_to_user_id': 1282946089, 'favorite_count': 0, 'in_reply_to_screen_name': 'amazonIN', 'in_reply_to_user_id_str': '1282946089', 'metadata': {'result_type': 'recent', 'iso_language_code': 'en'}, 'text': '@amazonIN @AmazonHelp Which Phone should i use until my phone as well as my money is with you for more than 10 days ? #AdjustNoMore', 'in_reply_to_status_id': None, 'user': {'location': 'India', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/100468594/1455872954', 'has_extended_profile': False, 'entities': {'description': {'urls': []}}, 'notifications': False, 'profile_use_background_image': True, 'default_profile': True, 'description': 'Nationalist. Engineer. Art lover. Photographer. Painter. Love to discuss Politics. Dream to Travel and work for Rural India.', 'id': 100468594, 'verified': False, 'created_at': 'Wed Dec 30 10:53:58 +0000 2009', 'profile_sidebar_fill_color': 'DDEEF6', 'screen_name': 'opjha', 'time_zone': 'Mumbai', 'id_str': '100468594', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/688231159080198144/XhtXa4ue_normal.jpg', 'friends_count': 234, 'profile_sidebar_border_color': 'C0DEED', 'translator_type': 'none', 'name': 'Omprakash C. Jha', 'utc_offset': 19800, 'is_translation_enabled': False, 'default_profile_image': False, 'statuses_count': 479, 'followers_count': 136, 'url': None, 'listed_count': 4, 'profile_image_url': 'http://pbs.twimg.com/profile_images/688231159080198144/XhtXa4ue_normal.jpg', 'favourites_count': 30, 'contributors_enabled': False, 'profile_text_color': '333333', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'following': False, 'is_translator': False, 'profile_link_color': '1DA1F2', 'profile_background_tile': False, 'protected': False, 'profile_background_color': 'C0DEED', 'follow_request_sent': False, 'geo_enabled': False, 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'lang': 'en'}, 'id': 800598686568947712, 'coordinates': None, 'contributors': None, 'lang': 'en'}


conn = mysql.connector.connect(user="root", password="test123", host="127.0.0.1", database="twitter_database") 
cursor = conn.cursor()
query = """CREATE TABLE tweetdata7 (
		
		 ID INT NOT NULL AUTO_INCREMENT,
		 TweetTime  DATETIME(6),
         Handle  VARCHAR(30),
         Tweet     VARCHAR(140),
         Polarity  Float(1),
         Label     CHAR(20),
         Location  VARCHAR(40),
         RetweetCount INT,
         primary key (ID)
         )"""
cursor.execute(query)
conn.commit()	

consumer_key = 'sPYOIfJ6FGJQXQXiYsvZDeXHx'
consumer_secret = '1J5EBejQ84ExRAEoGgAYA41ec8mDBjRLmHPBRgdQJDTw2ETica'
access_token = '798435833971781632-x4kSYHJ3ndxY4IJqR478s3T0k5EuEeX'
access_secret = 'o9ID3B9hfNjcTqdnaeGik430sCSHP3qv2oV5t0m90M1p9'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
MAX_TWEETS=250
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


	

for tweet in tweepy.Cursor(api.search,q="#demonetization OR #modi",lang="en" ).items(MAX_TWEETS): 
	try:	
		#json.loads returns JSON object. json.dumps returns a string 
		tweet1 = json.loads(json.dumps(tweet._json))
	

		if "text" in tweet1: # only messages having 'text' field is a tweet

			tweetime=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet1["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
			# %a - day , %b - month , %d - date,%H - hours,%M - minutes , %S - seconds , %Y - years



			
			time1=tweet1["in_reply_to_screen_name"] # when the tweet posted #twitter format Mon Nov 21 07:16:15 +0000 2016
			#print(time1)

			username=tweet1["user"]["screen_name"] # name of the user account, e.g. "cocoweixu"
			#print(username)

			tweetext=tweet1["text"] # content of the tweet
				

			retweet=tweet1["retweet_count"]
			#print(retweet)
			

			location=tweet1["user"]["location"]
			#print(location)

			threshold=0.0

			Blob=TextBlob(tweetext)
			threshold=Blob.polarity

			if(threshold==0.0):
				Label="Neutral"
			elif(threshold>0.0):
				Label="positive"
			elif(threshold<0.0):
				Label="negative"

			cursor.execute("""Insert into tweetdata7 (TweetTime,Handle,Tweet,Polarity,Label,Location,RetweetCount)
			values(%s,%s,%s,%s,%s,%s,%s)""", (tweetime,username,tweetext,threshold,Label,location,retweet))
			conn.commit()
			
	except tweepy.TweepError:
		time.sleep(60*15)
		
		print("in except block")
		continue


cursor.close()
conn.close()

	
		