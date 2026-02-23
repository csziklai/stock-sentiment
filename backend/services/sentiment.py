# Load model directly
# from transformers import AutoTokenizer, AutoModelForSequenceClassification

# tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
# model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
# Use a pipeline as a high-level helper
import os
from transformers import pipeline
import finnhub
from datetime import date, timedelta
#import requests
from newspaper import Article
#import torch
from dotenv import load_dotenv

pipe = pipeline(task="sentiment-analysis", model="ProsusAI/finbert") #ignore error

def get_articles(ticker : str):
    load_dotenv()
    finnhub_client = finnhub.Client(api_key=os.getenv("API_KEY"))
    today = date.today()
    week_ago = today - timedelta(days=7)
    today_str = today.strftime("%Y-%m-%d")
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    text_results = []

    results = finnhub_client.company_news(ticker, _from=today_str, to=today_str)
    # play around with timeframe - will there be enough news for 24h? or make it
    # a week if it's a lesser known company?
    if len(results) < 5:
        results = finnhub_client.company_news(ticker, _from=week_ago_str, to=today_str)
        print("finnhub found " + str(len(results)) + " articles")
    for a in results[:7]: #limit to the first 5 results for now
        if a["source"] in ["Bloomberg", "WSJ", "Financial Times"]:
            continue # skip these because of paywalls
        article = Article(a["url"]) 
        try:
            article.download()
            article.parse()
        except: 
            # skip past this article if we cannot open it
            print("could not open article")
            continue

        text = (article.text)[:1000] # truncate to 2000 chars for finbert
        text_results.append(text)

    return text_results

def analyze_sentiment(stock : str):
    sentiments = []

    article_texts = get_articles(stock)
    print("how many articles were retrieved: " + str(len(article_texts)))
    # brute force version, might need to do some sort of batching
    for a in article_texts:
        res = pipe(a)
        sentiments.append(res)

    print(sentiments)
    threshold = 0.3 # if score is better than this, considered positive
    
    pos_score = 0
    neg_score = 0
    neut_score = 0
    for s in sentiments:
        print(s)
        item = s[0] #it's a nested list [ [item], [item],... [item] ], where item is a dict
        if item['label'] == 'positive':
            pos_score += item['score']
        elif item['label'] == 'negative':
            neg_score += item['score']
        else:
            neut_score += item['score']

    score = (pos_score - neg_score) / len(sentiments)
    if score > threshold:
        res = "positive"
    elif score < 0:
        res = "negative"
    else:
        res = "neutral"

    return (res, score)

