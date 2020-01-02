# Functions pertaining to the broker used to retrieve news articles 
from newsfeed.models import Broker, Source, Author, Article
from datetime import datetime
import requests
import pytz

# TODO Hide this somehow
NEWS_KEY = '5fc766119a1e4ee8a20567bece674814'

# Fetches new articles
def fetch_articles():
    # Need to see which new articles have appeared since the last fetch
    url = ( 
        'https://newsapi.org/v2/top-headlines?'
        'country=us&'
        'category=business&'
        'apiKey=' + NEWS_KEY
    )
    response = requests.get(url)
    data = response.json()

    # Keep a count of number of new articles
    count = 0 
    for article in data['articles']:
        # Convert the publishedAt to a valid datetime
        article_parsed_published_date = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")

        # Check if this article is already in the database
        check = Article.objects.filter(title=article['title'], date_published=article_parsed_published_date)
        if not check:
            # Create new article
            print("Saving article: " + article['title'])

            # Get the source 
            source = Source.objects.filter(name=article['source']['name'])
            if not source:
                source = Source(name=article['source']['name'])
                source.save()
            else:
                source = Source.objects.get(name=article['source']['name'])

            # Get the author
            if article['author'] is not None:
                author = Author.objects.filter(name=article['author'])
                if not author:
                    author = Author(name=article['author'])
                    author.save()
                else:
                    author = Author.objects.get(name=article['author'])
            else:
                author = Author.objects.filter(name="Unknown")
                if not author:
                    author = Author(name="Unknown")
                    author.save()
                else:
                    author = Author.objects.get(name="Unknown")

            new_article = Article()
            new_article.title = article['title']
            new_article.source = source
            new_article.author = author 
            new_article.description = article['description']
            new_article.url = article['url']
            new_article.imgUrl = article['urlToImage']
            new_article.date_published = article_parsed_published_date
            new_article.save()
            count += 1
        else:
            # Done
            print("Fetched " + str(count) + " new articles.")
            return


# Checks if the broker should request new articles 
def check_broker():
    # Get the most recent fetch date
    broker = Broker.objects.filter(id=1)
    if not broker:
        # Should only create a broker once, central authority here 
        print("Creating the broker...")
        broker = Broker()
        broker.save()
    else: 
        broker = Broker.objects.get(id=1)

    # Get time since last fetch in minutes
    time_since_last_fetch = (datetime.now(pytz.utc) - broker.last_fetch_datetime).total_seconds() / 60.0
    print("Minutes since last update: " + str(time_since_last_fetch))
    # News API allows 500 requests/day on free trial. Fetch every 3 minutes
    # FIXME change this to 3.0 when done testing
    if time_since_last_fetch > 3.0: 
        # Fetch new articles, update broker
        fetch_articles()
        broker.last_fetch_datetime = datetime.now(pytz.utc)
        broker.save()
