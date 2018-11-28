from django.urls import path
from . import views

app_name = 'shortener_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:short_url_uid>/', views.url_redirect, name='url_redirect'),
    path('info/<slug:short_url_uid>', views.info, name='info'),
    path('delete/<slug:short_url_uid>', views.delete, name='delete'),
    path('myurls', views.list_urls, name='urls'),
    path('profile', views.profile, name='profile'),
    path('create_api_access', views.create_api_access, name='create_api_access'),
    path('delete_api_access/<int:api_access_id>', views.delete_api_access, name='delete_api_access'),
    path('shorten', views.shorten, name='shorten'),
    path('stats/<slug:short_url_uid>', views.stats, name='stats'),

    path('api/url/create', views.api_url_create, name='api_delete_create'),
    path('api/url/delete/<slug:uid>', views.api_url_delete, name='api_delete_url'),
    path('api/url/list', views.api_url_list, name='api_list_urls'),
]
