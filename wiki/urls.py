from django.urls import path
from . import views

app_name = 'wiki'

urlpatterns = [
    # Route: migsolver.com/wiki/
    path('', views.article_list, name='article_list'),
    
    # Route: migsolver.com/wiki/1/
    path('<int:article_id>/', views.article_detail, name='article_detail'),
]