from django.conf import settings
from django.urls import reverse

from .payloads import SHOW_ALL_FLOWERS

ADD_FLOWER_BUTTON = {
    "title": "Dodaj nowy kwiatek",
    "type": "web_url",
    "url": settings.PUBLIC_URL + reverse('front'),
    "messenger_extensions": True
}

SHOW_ALL_FLOWERS_BUTTON = {
    "title": "Pokaż wszystkie kwiatki",
    "type": "postback",
    "payload": SHOW_ALL_FLOWERS
}
