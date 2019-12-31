from django.db import models
import datetime

# Broker will manage the articles being retrieved and distributed
# TODO create a scheduler to force broker to auto-fetch on a defined interval 
class Broker(models.Model):
    # FIXME ensure that timezones between us and the API are consistent 
    # NOTE is this the best way to be storing a single value..?
    last_fetch_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Last fetch: " + self.last_fetch_datetime.strftime('%H:%M:%S %m/%d/%Y')

# A source provides articles (i.e. CNN, FOX, MSNBC...)
class Source(models.Model):
    # NOTE can name be used here or is it protected?
    name = models.CharField(max_length=100)
    # NOTE should be able to fetch all articles associated with a single source using the foreign key relationship 

    def __str__(self):
        return self.name

# Authors are associated with sources and articles 
class Author(models.Model):
    name = models.CharField(max_length=100, default="Unknown")

    def __str__(self):
        return self.name

# Articles are a single news story
class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400, default="...")
    url = models.URLField(max_length=300) 
    imgUrl = models.URLField(max_length=300, null=True)
    date_published = models.DateField()

    def __str__(self):
        return self.title