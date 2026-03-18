from django.shortcuts import render, get_object_or_404
from .models import WikiArticle

def article_list(request):
    # Fetch all articles, sorted by the most recently updated
    articles = WikiArticle.objects.all().order_by('-last_updated')
    return render(request, 'wiki/article_list.html', {'articles': articles})

def article_detail(request, article_id):
    # Fetch the specific article or throw a 404 error
    article = get_object_or_404(WikiArticle, id=article_id)
    return render(request, 'wiki/article_detail.html', {'article': article})