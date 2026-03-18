from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'basics'

urlpatterns = [
    # Our custom registration view
    path('register/', views.register_view, name='register'),
    
    # Django's built-in secure Login view (we just tell it which HTML file to use)
    path('login/', auth_views.LoginView.as_view(template_name='basics/login.html'), name='login'),
    
    # Django's built-in Logout view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]