from django.urls import path, include
from rest_framework import routers

from . import views
from . import api_views

router = routers.DefaultRouter()
router.register(r'flowers', api_views.FlowerSet)

urlpatterns = [
    path('', views.messenger_webhook_view, name='index'),
    path('front/', views.index_view, name='front'),
    path('api/', include(router.urls))
]
