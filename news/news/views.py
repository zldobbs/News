# High level views for root app 
from django.shortcuts import render

# / 
# Landing page of application
def index(request):
    return render(request, 'news/index.html')

# 404
# Handle 404 responses 
def handle404(request, *args, **kargs):
    return render(request, 'news/404.html')

# 500
# Handle 500 responses
def handle500(request, *args, **kargs):
    return render(request, 'news/500.html')