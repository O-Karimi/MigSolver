from django.urls import path
from . import views

app_name = 'qanda'

urlpatterns = [
    # This means: migsolver.com/ -> triggers the challenge_list view
    path('', views.challenge_list, name='challenge_list'),
]