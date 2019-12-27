from django.shortcuts import render

import requests

# TODO Hide this somehow
NEWS_KEY = '5fc766119a1e4ee8a20567bece674814'

# Create your views here.
def index(request): 
    url = ( 
        'https://newsapi.org/v2/top-headlines?'
        'country=us&'
        'category=business&'
        'apiKey=' + NEWS_KEY
    )
    response = requests.get(url)
    data = response.json()
    context = { 'feed': data['articles'] }
    return render(request, 'newsfeed/index.html', context)