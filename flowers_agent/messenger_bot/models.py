from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import TimeTrackable


class MessengerUser(TimeTrackable):
    # See more https://developers.facebook.com/docs/messenger-platform/reference/webhook-events
    page_id = models.CharField(
        max_length=50,
        verbose_name=_('Page ID'),
        help_text=_('Facebook page ID')
    )
    # See more https://developers.facebook.com/docs/pages/access-tokens/psid-api
    psid = models.CharField(
        max_length=50,
        verbose_name=_('User ID'),
        help_text=_('Page scoped user ID')
    )

    class Meta:
        unique_together = ('page_id', 'psid')

    def __str__(self):
        return 'User {}'.format(self.psid)


class Flower(TimeTrackable):
    user = models.ForeignKey(MessengerUser, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name=_('Flower\'s name'),
        max_length=50,
    )
    image = models.URLField(
        verbose_name=_('Image'),
        help_text=_('An image of the flower'),
        blank=True
    )
    period = models.DurationField(
        verbose_name=_('Water period'),
        help_text=_('Defines how frequently water the flower')
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Flower {user}/{flower}'.format(user=self.user.psid, flower=self.id)
