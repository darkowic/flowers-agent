from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse

from flowers_agent.messenger_bot.helpers import FbMeProfileAPI


class Command(BaseCommand):
    '''
    Reference https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/domain
    -whitelisting
    '''
    help = 'Set messenger whitelist urls'

    def handle(self, *args, **options):
        api = FbMeProfileAPI(getattr(settings, 'MESSENGER_ACCESS_TOKEN'))
        payload = {
            "whitelisted_domains": [
                settings.PUBLIC_URL
            ]
        }
        result = api.post(payload)
        if result.get('result') == 'success':
            self.stdout.write(self.style.SUCCESS('Successfully set whitelist domains.'))
        else:
            self.stderr.write(self.style.ERROR('Something went wrong. Details: ${}'.format(result)))
