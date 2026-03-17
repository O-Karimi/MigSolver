from django.contrib import admin
from .models import WikiArticle

@admin.register(WikiArticle)
class WikiArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'last_updated')
    search_fields = ('title',)
    filter_horizontal = ('categories',) # Makes selecting multiple categories look much cleaner