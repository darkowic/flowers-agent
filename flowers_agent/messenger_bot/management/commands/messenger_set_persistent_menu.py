from django.conf import settings
from django.core.management.base import BaseCommand

from flowers_agent.messenger_bot.helpers import FbMeProfileAPI
from flowers_agent.messenger_bot.buttons import ADD_FLOWER_BUTTON, SHOW_ALL_FLOWERS_BUTTON


class Command(BaseCommand):
    help = 'Set messenger persistent menu buttons'

    def handle(self, *args, **options):
        api = FbMeProfileAPI(getattr(settings, 'MESSENGER_ACCESS_TOKEN'))
        payload = {
            "persistent_menu": [
                {
                    "locale": "default",
                    "composer_input_disabled": False,
                    "call_to_actions": [
                        ADD_FLOWER_BUTTON,
                        SHOW_ALL_FLOWERS_BUTTON,
                    ]
                }
            ]
        }
        result = api.post(payload)
        if result.get('result') == 'success':
            self.stdout.write(self.style.SUCCESS('Successfully updated persistent menu.'))
        else:
            self.stderr.write(self.style.ERROR('Something went wrong. Details: ${}'.format(result)))
