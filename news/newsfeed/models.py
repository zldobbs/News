from django.db import models

# Create your models here.
class Article(models.Model):
    news_source = models.CharField(max_length=100)
    source_url = models.URLField(max_length=300) 
    date_published = models.DateField()
