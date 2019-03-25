# users/urls.py
from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path(
        'signup/',
        cache_page(settings.CACHE_MIDDLEWARE_SECONDS)(views.SignUp.as_view()),
        name='signup'),
    path(
        'login/',
        cache_page(settings.CACHE_MIDDLEWARE_SECONDS)(views.Login.as_view()),
        name='login'),
]
