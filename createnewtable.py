"""creating new table from exsisting table for sentiment analysis . new table consists of tweet and label
Sentiment analysis using database is working fine on small dataset . dataset consists of 30 tweets fetched from twitter.
tested works fine"""


import mysql.connector 
import csv
from textblob.classifiers import NaiveBayesClassifier

conn = mysql.connector.connect(user="root", password="test123", host="127.0.0.1", database="twitter_database") 
cursor = conn.cursor()
#query = """ CREATE TABLE SentimentDataset3 AS # creates a new table from the exsisting table.new table consists of only tweet and label
 #  SELECT  Tweet,Label
 #  FROM tweetdata7
  # """
#cursor.execute(query)
#conn.commit()
cursor.execute("SELECT * from SentimentDataset3")  # performs sentiment analysis
train=cursor.fetchall()
cl = NaiveBayesClassifier(train)
#print(cl.classify("demonetization"))
cursor.close()
conn.close()





