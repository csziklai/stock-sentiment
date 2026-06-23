import os
from transformers import pipeline
import finnhub
from datetime import date, timedelta
from newspaper import Article
from dotenv import load_dotenv
from models.article import ArticleInfo

pipe = pipeline(task="sentiment-analysis", model="ProsusAI/finbert")

def get_articles(ticker : str):
    load_dotenv()
    finnhub_client = finnhub.Client(api_key=os.getenv("API_KEY"))
    today = date.today()
    week_ago = today - timedelta(days=7)
    today_str = today.strftime("%Y-%m-%d")
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    articles = []

    results = finnhub_client.company_news(ticker, _from=today_str, to=today_str)

    if len(results) < 5:
        results = finnhub_client.company_news(ticker, _from=week_ago_str, to=today_str)
        print("finnhub found " + str(len(results)) + " articles")
    for a in results[:7]: #limit to the first 7 results for now
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

        text = (article.text)[:1000] # truncate to 1000 chars for finbert
        art_obj = ArticleInfo(
            title=article.title,
            url= article.url,
            text = text,
            sentiment = "unset"
        )
        articles.append(art_obj)

    return articles

def analyze_sentiment(stock : str):
    sentiments = []

    articles = get_articles(stock)

    print("how many articles were retrieved: " + str(len(articles)))
    for a in articles:
        res = pipe(a.text)
        #print("res: " + res)
        sentiments.append(res)
        a.sentiment = res[0]['label']

    #print(sentiments)
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

    return (res, score, articles)

