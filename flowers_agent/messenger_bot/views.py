import json

from django import views
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .helpers import handle_message, handle_message_reads


# Create your views here.


class MessengerWebhookView(views.View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        # in get method facebook api subscribes to the webhook
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        if mode == 'subscribe' and token == getattr(settings, 'MESSENGER_VERIFY_TOKEN'):
            return HttpResponse(request.GET.get('hub.challenge'))
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if not request.content_type == 'application/json':
            raise Http404
        body = json.loads(request.body)
        print('request body', body)
        # Check the webhook event is from a Page subscription
        if body.get('object', None) == 'page':
            # Iterate over each entry - there may be multiple if batched
            for entry in body.get('entry', []):
                # Get the webhook event. entry.messaging is an array, but
                # will only ever contain one event, so we get index 0
                webhook_event = entry['messaging'][0]
                sender_psid = webhook_event['sender']['id']
                print('test webhook_event', webhook_event)
                if (webhook_event.get('message')):
                    handle_message(sender_psid, webhook_event.get('message'))
                elif (webhook_event.get('read')):
                    handle_message_reads(sender_psid, webhook_event.get('message_reads'))
                else:
                    print('Not recognized webhook event', webhook_event)
            return HttpResponse('EVENT_RECEIVED')
        raise Http404


messenger_webhook_view = csrf_exempt(MessengerWebhookView.as_view())
