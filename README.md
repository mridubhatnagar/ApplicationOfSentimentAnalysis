# ApplicationOfSentimentAnalysis
 Developed a python application to listen and harvest tweets which are based on certain topic or contain keywords/hashtags etc.  Typical use is to analyse user tweets that may relate to a product feedback, some campaign or similar. The application needs to be generic which can be deployed for various uses. All the tweets that it harvests would be saved in mysql tables for later analysis. 
 
 
Requirements:
Python 3.4.2
MySQL
install tweepy 
TextBlob module


Files
1)FinalTest.py- Contains the code to fetch 5000 tweets from twitter using twitter's REST API and tweepy module.And stores the retrieved values in MySQL database.

import tweepy
from tweepy import OAuthHandler

consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)




2)Createnewtable.py-Has the code to perform sentiment analysis on the fetched tweets using TextBlob module and naive bayes algorithm.Trains the dataset and helps in classfying the keyword into positive,negative or neutral.



3)MergedGUI-Involves graphical interface for the project. Based on the data graphical analysis of data is done.

