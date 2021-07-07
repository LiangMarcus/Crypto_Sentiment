import datetime
import mysql.connector
import time
import praw 

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

#Reddit API
reddit = praw.Reddit(client_id="", client_secret="",
                    password="", user_agent="",
                    username="")

#MySQL
db = mysql.connector.connect(
    host = "localhost",
    user = "",
    passwd = ""
)

cursor = db.cursor()

# Create a database for storing reddit data 
cursor.execute("CREATE DATABASE IF NOT EXISTS reddit_data")

# Title and body would be used for the sentiment analysis and for counting the number of times a particular ticker is mentioned 
cursor.execute("""CREATE TABLE IF NOT EXISTS reddit_data.reddit_data_sentiment
                (date_time DATETIME,
                subreddit VARCHAR(500),
                title VARCHAR(500),
                body VARCHAR(2000),
                author VARCHAR(500),
                sentiment_score DECIMAL(5,4)
                )
                """)

sqlFormula = "INSERT INTO reddit_data.reddit_data_sentiment (date_time, subreddit, title, body, author, sentiment_score) VALUES (%s, %s, %s, %s, %s, %s)"

## Streaming post/comments from reddit 
def reddit_stream():  
    data = ()
    while True:
        try:
            # list of subreddits to be tracked -- you can add the ones you think are important to track 
            subreddit = reddit.subreddit("CryptoMarket+CryptoCurrency+Crypto_Currency_News+CryptoCurrencyTrading")
            for comment in subreddit.stream.comments(skip_existing=True):
                    current_time = datetime.datetime.now()
                    subreddit = str(comment.subreddit)
                    author = str(comment.author)
                    title = str(comment.link_title)
                    body = str(comment.body)
                    if len(body) < 2000:
                        body = body
                    elif len(body) > 2000:
                        body = "data is too large" 
                    sentiment = sentiment_score(body)
                    data = (current_time,subreddit,title,body,author,sentiment)
                    cursor.execute(sqlFormula, data)
                    db.commit()
        # Keep an exception so that in case of error
        except Exception as e:
            data=e
            print(str(e))
            time.sleep(10)
    return data

#reddit_stream()
