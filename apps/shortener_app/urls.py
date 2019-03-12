from django.urls import path
from .views import frontend, backend, api

app_name = 'shortener_app'

urlpatterns = [
    # Frontend
    path('', frontend.index, name='index'),
    path('<slug:short_url_uid>/', frontend.url_redirect, name='url_redirect'),
    path('info/<slug:short_url_uid>', frontend.info, name='info'),
    path('shorten', frontend.shorten, name='shorten'),
    path('pricing', frontend.pricing, name='pricing'),

    # Backend
    path('delete/<slug:short_url_uid>', backend.delete, name='delete'),
    path('stats/<slug:short_url_uid>', backend.stats, name='stats'),
    path('myurls', backend.list_urls, name='urls'),
    path('profile', backend.profile, name='profile'),
    path(
        'upgrade_to_premium',
        backend.upgrade_to_premium,
        name='upgrade_to_premium'),
    path(
        'create_api_access',
        backend.create_api_access,
        name='create_api_access'),
    path(
        'delete_api_access/<int:api_access_id>',
        backend.delete_api_access,
        name='delete_api_access'),

    # API
    path('api/url/create', api.api_url_create, name='api_create_url'),
    path(
        'api/url/delete/<slug:uid>', api.api_url_delete, name='api_delete_url'),
    path('api/url/list', api.api_url_list, name='api_list_urls'),
]
