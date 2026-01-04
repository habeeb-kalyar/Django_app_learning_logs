from django.urls import path, include
from . import views  # This imports the views.py file

urlpatterns = [
    # Include default auth urls
    path('', include('django.contrib.auth.urls')),
    # Registration page
    path('register/', views.register, name='register'), # No quotes around views.register
]