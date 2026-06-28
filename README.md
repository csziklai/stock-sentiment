## About
Stock Sentiment Analyzer is a full-stack web application that analyzes financial news articles and generates sentiment scores for publicly traded companies using FinBERT
(https://huggingface.co/ProsusAI/finbert). Users can search for stocks, retrieve recent news, and view aggregated sentiment insights to gauge market sentiment. This project performs sentiment analysis for a given stock, Users can search for stocks, see a real-time score that represents
how positive or negative the current sentiment is, and see the top news articles that 
contributed to this score.

## Video Demo


https://github.com/user-attachments/assets/9ff9924c-4c5b-4860-916d-82d9509eb103


## Getting Started

First, run the development server for the frontend:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Then in another shell, start the backend:
```bash
cd backend
fastapi dev main.py
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the 
project.

## Features

- Search publicly traded companies by ticker symbol
- Retrieve recent financial news articles and analyze their sentiment using FinBERT
- Aggregate sentiment scores across multiple articles using a weighted average formula
- Display bullish, bearish, and neutral sentiment indicators
- Display links to selected articles that contributed to the score
- Responsive frontend built with Next.js

## Tech Stack

Frontend
- Next.js
- React
- Tailwind CSS

Backend
- FastAPI
- Python

Machine Learning
- FinBERT (Hugging Face Transformers)

Data Sources
- [Finnhub Company News API](https://finnhub.io/docs/api/company-news)
- Yahoo Finance Search [yfinance](https://ranaroussi.github.io/yfinance/reference/api/yfinance.Lookup.html#yfinance.Lookup)



