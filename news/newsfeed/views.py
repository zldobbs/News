from django.shortcuts import render
import newsfeed.utils.broker as broker 
from .models import Source, Author, Article

# /newsfeed/
# Populate page of recent posts 
# FIXME right now this is where we fetch all new posts, this should be handled using a scheduler 
def index(request): 
    broker.check_broker()

    # Get the 10 latest articles 
    latest_articles = Article.objects.order_by('-date_published')[:30].values()

    # Populate relevant information for the articles
    for article in latest_articles:
        try: 
            source = Source.objects.get(id=article['source_id'])
            article['source'] = source
        except:
            print("Error: No source ID: " + str(article['source_id']))
        try: 
            author = Author.objects.get(id=article['author_id'])
            article['author'] = author
        except:
            print("Error: No author ID: " + str(article['author_id']))

    context = { 'feed': latest_articles }
    return render(request, 'newsfeed/index.html', context)