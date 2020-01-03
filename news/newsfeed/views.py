from django.shortcuts import render
from django.http import HttpResponse
import newsfeed.utils.broker as broker 
from .models import Source, Author, Article

# TODO Implement pagination for all views 
# FIXME Sources for articles by "Unknown" are all returning "Unknown"

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
            article['source'] = "Unknown"
        try: 
            author = Author.objects.get(id=article['author_id'])
            article['author'] = author
        except:
            print("Error: No author ID: " + str(article['author_id']))
            article['author'] = "Unknown"

    context = { 
        'page': {
            'headline': "Today's headlines"
        },
        'feed': latest_articles 
    }
    return render(request, 'newsfeed/index.html', context)

# /newsfeed/<source_id>/
# Show information on the specified source
# Populate all articles by this source 
def source(request, source_id):
    # Check if source exists
    try:
        # Fill info for the given source
        source = Source.objects.get(id=source_id)
        # FIXME Shouldn't be retrieving all articles at once
        articles = source.article_set.all().values()
        for article in articles: 
            article['source'] = source.name
            try: 
                author = Author.objects.get(id=article['author_id'])
                article['author'] = author
            except:
                print("Error: No author ID: " + str(article['author_id']))
                article['author'] = "Unknown"
        context = {
            'page': {
                'headline': source.name,
                'description': "WIP",
                'leftVotes': "WIP",
                'middleVotes': "WIP",
                'rightVotes': "WIP"
            },
            'feed': articles
        }
    except: 
        # TODO Do the 404 here
        print("Requested source does not exist: " + str(source_id)) 
        context = {
            'page': {
                'headline': "Unknown source. Should raise a 404 here."
            }
        }

    return render(request, 'newsfeed/index.html', context)

# /newsfeed/<author_id>/
# Show information on the specified author
# Populate all articles by this author 
def author(request, author_id):
    # Check if author exists
    try:
        # Fill info for the given author
        author = Author.objects.get(id=author_id)
        # FIXME Shouldn't be retrieving all articles at once
        articles = author.article_set.all().values()
        for article in articles: 
            article['author'] = author.name
            try: 
                source = Source.objects.get(id=article['source_id'])
                article['source'] = author
            except:
                print("Error: No author ID: " + str(article['source_id']))
                article['source'] = "Unknown"
        context = {
            'page': {
                'headline': author.name,
                'description': "WIP",
                'leftVotes': "WIP",
                'middleVotes': "WIP",
                'rightVotes': "WIP"
            },
            'feed': articles
        }
    except: 
        # TODO Do the 404 here
        print("Requested author does not exist: " + str(author_id)) 
        context = {
            'page': {
                'headline': "Unknown author. Should raise a 404 here."
            }
        }

    return render(request, 'newsfeed/index.html', context)