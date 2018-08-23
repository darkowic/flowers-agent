from django.core.exceptions import ImproperlyConfigured
from pymessenger.bot import Bot
from django.conf import settings

MESSENGER_ACCESS_TOKEN = getattr(settings, 'MESSENGER_ACCESS_TOKEN')

if not MESSENGER_ACCESS_TOKEN:
    raise ImproperlyConfigured('MESSENGER_ACCESS_TOKEN has to be defined')

bot = Bot(MESSENGER_ACCESS_TOKEN)


def handle_message(sender_psid, message):
    print('handle message!', sender_psid, message)
    if message.get('text'):
        bot.send_text_message(sender_psid, message.get('text'))


def handle_message_reads(sender_psid, received_message):
    print('handle message reads!', sender_psid, received_message)
