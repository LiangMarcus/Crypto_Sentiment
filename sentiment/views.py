from django.shortcuts import render, redirect
from .models import CryptoData
from .forms import CryptoDataForm
from django.views.generic import ListView
from django.http import HttpResponse,Http404,HttpResponseRedirect,HttpResponseNotFound

from Sentiment_Analysis.crypto_finance import crypto_finance_info, get_dict, get_crypto_sentiment

import plotly.graph_objs as go
from plotly.offline import plot
import yfinance as yf


# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')

def search(request):
    q = request.GET['q']
    search_word = str(q).replace(" ", "").lower()
    info = crypto_finance_info(search_word)
    crypto_dict = get_dict()
    #Sentiment Score Gauge 
    sentiment_score = get_crypto_sentiment(search_word)
    gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = sentiment_score,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Sentiment Score"},
    gauge = {'axis': {'range': [0, 1]}}))

    gauge.update_layout(
    margin=dict(l=5, r=5, t=5, b=5), height=200, width=200)

    plot_div_guage = plot(gauge, output_type='div')

    
    #Candlestick Graph
    ticker = crypto_dict[search_word] + "-USD"
    data = yf.download(tickers=ticker, period = '5d', interval = '15m', rounding= True)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))
    fig.update_layout(title =  ticker+" Price", yaxis_title = "Price (USD)")
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
    buttons=list([
    dict(count=15, label='15m', step="minute", stepmode="backward"),
    dict(count=45, label='45m', step="minute", stepmode="backward"),
    dict(count=1, label='1h', step="hour", stepmode="backward"),
    dict(count=6, label='6h', step="hour", stepmode="backward"),
    dict(step='all')
    ])
    )
    )
    

    plot_div_candle = plot(fig, output_type='div')
    #Context for html
    context = {
        'search_term' : search_word,
        'name' : info['name'],
        'description' : info['description'],
        'current_price' : info["regularMarketPrice"],
        'candlestick' : plot_div_candle,
        'gauge' : plot_div_guage,
    }
    return render(request, 'dashboard/search_results.html', context)