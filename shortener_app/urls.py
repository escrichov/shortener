from django.urls import path
from . import views

app_name = 'shortener_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:short_url_id>/', views.url_redirect, name='url_redirect'),
    path('info/<int:short_url_id>', views.info, name='info'),
    path('shorten', views.shorten, name='shorten'),
]