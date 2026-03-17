from django.urls import path
from . import views

app_name = 'qanda'

urlpatterns = [
    # This means: migsolver.com/ -> triggers the challenge_list view
    path('', views.challenge_list, name='challenge_list'),
    path('ask/', views.ask_challenge, name='ask_challenge'),
    path('<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
path('solution/<int:solution_id>/vote/<int:value>/', views.vote_solution, name='vote_solution'),]