import requests
from django.core.exceptions import ImproperlyConfigured
from pymessenger.bot import Bot
from django.conf import settings

from .models import MessengerUser, Flower
from .payloads import (GET_STARTED, SHOW_ALL_FLOWERS)

MESSENGER_ACCESS_TOKEN = getattr(settings, 'MESSENGER_ACCESS_TOKEN')

if not MESSENGER_ACCESS_TOKEN:
    raise ImproperlyConfigured('MESSENGER_ACCESS_TOKEN has to be defined')

bot = Bot(MESSENGER_ACCESS_TOKEN)

DEFAULT_API_VERSION = 3.1


class WebhookHandler(object):
    supported_event = ['message', 'postback']

    def __init__(self, page_id, sender_psid):
        self.page_id = page_id
        self.sender_psid = sender_psid

    @property
    def user(self):
        return MessengerUser.objects.get(
            page_id=self.page_id,
            psid=self.sender_psid
        )

    def handle(self, event):
        for event_name in self.supported_event:
            # iterate supported event and execute first supported
            if event.get(event_name):
                # call handler
                handler = getattr(self, 'handle_{}'.format(event_name))
                return handler(event.get(event_name))
        raise ValueError('Could not handle event: {}. Not supported.'.format(event))

    def handle_message(self, event):
        # TODO: This is temporary - create user when connect with hello message
        MessengerUser.objects.get_or_create(
            psid=self.sender_psid,
            page_id=self.page_id
        )
        bot.send_text_message(self.sender_psid, 'Przepraszam, ale nie rozumiem co do mnie piszesz :(')

    def handle_postback(self, event):
        payload = event.get('payload')
        bot.send_text_message(self.sender_psid, 'Received postback: {}'.format(payload))
        # here handle all postbacks defined in payloads
        if (payload == GET_STARTED):
            # get or create new user's account
            MessengerUser.objects.get_or_create(
                psid=self.sender_psid,
                page_id=self.page_id
            )
            from .buttons import ADD_FLOWER_BUTTON  # cross import
            bot.send_button_message(
                self.sender_psid,
                'Cześć! Jestem tutaj dla Ciebie by pomóc Ci zadbać o Twoje kwiatki. '
                'Kliknij w przycisk poniżej lub wybierz opcje z menu aby dodać kwiatek '
                'o którego podlewaniu mam Ci przypomnieć :)',
                [ADD_FLOWER_BUTTON]
            )

        elif (payload == SHOW_ALL_FLOWERS):
            # messenger limitation - you can list max 10 elements in the list
            flowers = Flower.objects.filter(user=self.user)[:9]

            if flowers.count() == 0:
                # User has no flower - inform him about it
                bot.send_text_message(self.sender_psid, 'Nie masz żadnych dodanych kwiatków :(')
                return

            elements = []

            for flower in flowers:
                elements.append({
                    'title': 'Kwiatek',
                    'image_url': flower.image
                })
            bot.send_generic_message(self.sender_psid, elements)
        else:
            # TODO: logger
            print('Payload not recognized: {}'.format(payload))


class FbMeAPIBase(object):
    def __init__(self, access_token, **kwargs):
        '''
            @required:
                access_token
            @optional:
                api_version
                app_secret
        '''
        self.api_version = kwargs.get('api_version') or DEFAULT_API_VERSION
        # Not used for now - may be used for appsecret_proof
        # https://developers.facebook.com/docs/graph-api/securing-requests/#appsecret_proof
        self.app_secret = kwargs.get('app_secret')
        self.graph_url = 'https://graph.facebook.com/v{0}'.format(self.api_version)
        self.access_token = access_token

    @property
    def auth_args(self):
        if not hasattr(self, '_auth_args'):
            auth = {
                'access_token': self.access_token
            }
            self._auth_args = auth
        return self._auth_args

    def post(self, api, payload):
        request_endpoint = '{graph_url}/me/{api}'.format(
            graph_url=self.graph_url,
            api=api
        )
        response = requests.post(
            request_endpoint,
            params=self.auth_args,
            json=payload
        )
        result = response.json()
        return result


class FbMeProfileAPI(FbMeAPIBase):
    def post(self, payload):
        return super(FbMeProfileAPI, self).post('messenger_profile', payload)
