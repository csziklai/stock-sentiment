# Load model directly
# from transformers import AutoTokenizer, AutoModelForSequenceClassification

# tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
# model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
# Use a pipeline as a high-level helper
import os
from transformers import pipeline
import finnhub
from datetime import date
#import requests
from newspaper import Article
import torch

pipe = pipeline(task="sentiment-analysis", model="ProsusAI/finbert") #ignore error

def get_articles(ticker : str):
    finnhub_client = finnhub.Client(api_key=os.getenv("API_KEY"))
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    text_results = []

    results = finnhub_client.company_news(ticker, _from=today_str, to=today_str)
    # play around with timeframe - will there be enough news for 24h? or make it
    # a week if it's a lesser known company?
    for a in results[:5]: #limit to the first 5 results for now
        # might not be able to visit all articles (paywalls, etc.)
        if a["source"] in ["Bloomberg", "WSJ", "Financial Times"]:
            continue
        article = Article(a["url"]) 
        article.download()
        article.parse()

        text = (article.text)[:2000] # truncate to 2000 chars for finbert
        text_results.append(text)

    return text_results

def analyze_sentiment(stock : str):
    sentiments = []

    article_texts = get_articles(stock)
    # brute force version, might need to do some sort of batching
    for a in article_texts:
        res = pipe(a)
        sentiments.append(res)

    print(sentiments)

    # compute whether it's overall positive or negative
    # TODO come up with a better algorithm
    pos_score = 0
    neg_score = 0
    neut_score = 0
    for s in sentiments:
        if s['label'] == 'POSITIVE':
            pos_score += s['score'] # could there by python floating error?
        elif s['label'] == 'NEGATIVE':
            neg_score += s['score']
        else:
            neut_score += s['score']

    # just to see what it outputs
    return {'pos' : pos_score, 'neg' : neg_score, 'neut' : neut_score, 'sentiments' : sentiments}

