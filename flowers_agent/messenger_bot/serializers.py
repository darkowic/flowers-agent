import json

from django.conf import settings
from requests_toolbelt import MultipartEncoder
from rest_framework import serializers

from flowers_agent.messenger_bot.helpers import FbMeMessagesAPI, bot
from flowers_agent.messenger_bot.models import Flower, MessengerUser
from flowers_agent.messenger_bot.payloads import PERIOD_MAP


class MessengerUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MessengerUser
        fields = ('psid',)


class FlowerSerializer(serializers.HyperlinkedModelSerializer):
    period = serializers.CharField(required=True)

    class Meta:
        model = Flower
        fields = ('name', 'image', 'period')

    def validate_period(self, value):
        period = PERIOD_MAP.get(value, None)

        if period is None:
            raise serializers.ValidationError("Incorrect period value")
        return period

    # TODO: try to save the image on fb servers...
    def save_image(self, image, psid):
        api = FbMeMessagesAPI(getattr(settings, 'MESSENGER_ACCESS_TOKEN'))

        image.seek(0)
        payload = {
            'recipient': json.dumps(
                {
                    'id': psid
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'file',
                        'payload': {}
                    }
                }
            ),
            'filedata': (image.name, image)
        }
        multipart_data = MultipartEncoder(payload)
        multipart_header = {
            'Content-Type': multipart_data.content_type
        }
        response = api.post(data=multipart_data, headers=multipart_header)
        return response['attachment_id']

    def create(self, validated_data):
        flower = super(FlowerSerializer, self).create(validated_data)
        psid = validated_data['user'].psid
        bot.send_generic_message(psid, [{
            "title": "Dodałeś kwiatek '{}'!".format(flower.name),
            "image_url": settings.PUBLIC_URL + flower.image.url,
        }])
        return flower

    #
    # def update(self, instance, validated_data):
    #     return instance
