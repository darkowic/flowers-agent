import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import TimeTrackable


class MessengerUser(TimeTrackable):
    # See more https://developers.facebook.com/docs/pages/access-tokens/psid-api
    psid = models.CharField(
        max_length=50,
        verbose_name=_('User ID'),
        help_text=_('Page scoped user ID')
    )

    def __str__(self):
        return 'User {}'.format(self.psid)


def flower_image_upload_to_handler(instance, filename):
    return os.path.join('flowers', str(instance.user.id), filename)


class Flower(TimeTrackable):
    user = models.ForeignKey(MessengerUser, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name=_('Flower\'s name'),
        max_length=50,
    )
    image = models.ImageField(
        verbose_name=_('Image'),
        help_text=_('An image of the flower'),
        blank=True,
        upload_to=flower_image_upload_to_handler
    )
    period = models.DurationField(
        verbose_name=_('Water period'),
        help_text=_('Defines how frequently water the flower')
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Flower {user}/{flower}'.format(user=self.user.psid, flower=self.id)
