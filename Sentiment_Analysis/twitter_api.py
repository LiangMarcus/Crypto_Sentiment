from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import mysql.connector
import datetime
import time
import pandas as pd
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

new_words = {
    'moon': 2.0,
    '🚀': 2.0,
    'paper hands': -0.8,
    'diamond hands': 0.5,
    '💎🤲': 0.5,
    '🧻🤲': -0.8,    
    '📈': 1.9,
    '📉': -1.9,
    'bullish': 1,
    '🐂': 1,
    'bearish': -1,
    '🧸': -1
}

SIA = SentimentIntensityAnalyzer()

SIA.lexicon.update(new_words)

def sentiment_score(text):
    sentiment_dict = SIA.polarity_scores(text)
    return sentiment_dict['compound']




#MySQL
db = mysql.connector.connect(
    host = "localhost",
    user = "",
    passwd = ""
)

cursor = db.cursor()

# Create a database for storing twitter data 
cursor.execute("CREATE DATABASE IF NOT EXISTS twitter_data")

cursor.execute("""CREATE TABLE IF NOT EXISTS twitter_data.twitter_data_sentiment
                (date_time DATETIME,
                author VARCHAR(500),
                tweet VARCHAR(2000),
                sentiment_score DECIMAL(5,4)
                )
                """)

sqlFormula = "INSERT INTO twitter_data.twitter_data_sentiment (date_time, author, tweet, sentiment_score) VALUES (%s, %s, %s, %s)"

ckey=""
csecret=""
atoken=""
asecret=""  

class listener(StreamListener):
    def on_data(self,data):
        all_data = json.loads(data)
        current_time = datetime.datetime.now()
        author = str(all_data['user']['screen_name'])
        tweet = str(all_data["text"])
        sentiment = sentiment_score(tweet)
        data = (current_time, author, tweet,sentiment)
        cursor.execute(sqlFormula, data)
        db.commit()
    def on_error(self,status):
        print(status)

## Connecting to twitter and establishing a live stream 
def twitter_stream():
    while True:
        try:
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=["#cryptocurrency"]) 
        except Exception as e:
            print(str(e))
            time.sleep(10)
