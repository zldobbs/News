from django.contrib import admin
from .models import Broker, Source, Author, Article

# Register your models here.
admin.site.register(Broker)
admin.site.register(Source)
admin.site.register(Author)
admin.site.register(Article)