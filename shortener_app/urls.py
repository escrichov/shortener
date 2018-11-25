from django.urls import path
from . import views

app_name = 'shortener_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:short_url_uid>/', views.url_redirect, name='url_redirect'),
    path('info/<slug:short_url_uid>', views.info, name='info'),
    path('myurls', views.list_urls, name='urls'),
    path('shorten', views.shorten, name='shorten'),
]
