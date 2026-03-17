from django.db import models
from django.conf import settings
from basics.models import Category

class WikiArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True) # Auto-updates every time you save!
    
    # Notice we use SET_NULL instead of CASCADE here. 
    # If an Admin leaves the team and their account is deleted, 
    # we don't want the database to automatically delete all their Wiki articles!
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='wiki_articles'
    )
    
    categories = models.ManyToManyField(Category, related_name='wiki_articles')

    def __str__(self):
        return self.title