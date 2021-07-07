import yfinance as yf
import csv
import mysql.connector

#Database connection
db = mysql.connector.connect(
    host = "localhost",
    user = "MarcusLiang",
    passwd = "24A78r00!123"
)
cursor = db.cursor()

#Turn csv to dictionary
def get_dict():
    crypto_dict = dict()
    crypto_csv = open("Sentiment_Analysis\Crypto_Symbols.csv")
    for line in crypto_csv:
        line = line.strip('\n')
        (key, val) = line.split(",")
        crypto_dict[key] = val
    return crypto_dict

def reverse_dict():
    crypto_dict = get_dict()
    symbol_dict = dict()
    symbol_dict = {v: k for k, v in crypto_dict.items()}
    return symbol_dict


#Get all Crypto infomation
def crypto_finance_info(name):
    crypto_dict = get_dict()
    try:
        symbol = crypto_dict[name]
        return yf.Ticker(symbol+"-USD").info      
    except:
        return yf.Ticker(name+"-USD").info


#Get Sentiment Score of Specific Crypto in DB
def get_crypto_sentiment(text):
    crypto_dict = get_dict()
    symbol_dict = reverse_dict()
    sqlFormula = "SELECT AVG(sentiment_score) FROM reddit_data.reddit_data_sentiment WHERE title LIKE %s OR title LIKE %s OR body LIKE %s OR body LIKE %s"
    crypto = text
    try:
        symbol = crypto_dict[text.lower()]
        
    except:
        symbol = symbol_dict[text.upper()]

    data = ("%" + text + "%" , "%" + symbol + "%"  , "%" + text + "%"  , "%" + symbol + "%" )
    cursor.execute(sqlFormula, data)
    reddit_score = cursor.fetchone()[0]
    sqlFormula = "SELECT AVG(sentiment_score) FROM twitter_data.twitter_data_sentiment WHERE tweet LIKE %s OR tweet LIKE %s"
    data = ("%" + text + "%" , "%" + symbol + "%")
    cursor.execute(sqlFormula, data)
    twitter_score = cursor.fetchone()[0]
    return  (reddit_score+twitter_score)/2

#Test Cases:
    #print(crypto_finance_info("btc"))
    #print(yf.Ticker("BTC").info)
    #print(crypto_dict["BTC"])
print(get_crypto_sentiment("BTC"))
 