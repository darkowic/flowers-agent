from django.urls import path

from . import views

urlpatterns = [
    path('', views.messenger_webhook_view, name='index'),
]
