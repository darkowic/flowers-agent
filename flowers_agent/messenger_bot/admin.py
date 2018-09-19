from django.contrib import admin

from .models import MessengerUser, Flower


@admin.register(MessengerUser)
class MessengerUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    pass
