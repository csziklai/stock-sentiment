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
        try:
            article.download()
            article.parse()
        except: 
            # skip past this article if we cannot open it
            continue

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
    threshold = 0.3 # if score is better than this, considered positive
    
    pos_score = 0
    neg_score = 0
    neut_score = 0
    for s in sentiments:
        print(s)
        item = s[0] #annoying that it's a nested list [ [item], [item],... [item] ], where item is a dict
        if item['label'] == 'POSITIVE':
            pos_score += item['score']
        elif item['label'] == 'NEGATIVE':
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

