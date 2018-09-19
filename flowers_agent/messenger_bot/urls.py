from django.urls import path

from . import views

urlpatterns = [
    path('', views.messenger_webhook_view, name='index'),
    path('front/', views.index_view, name='front'),
]
