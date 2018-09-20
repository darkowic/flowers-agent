import json

from django.views import generic as views
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .helpers import WebhookHandler


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
                handler = WebhookHandler(
                    webhook_event['recipient']['id'],
                    webhook_event['sender']['id']
                )
                try:
                    handler.handle(webhook_event)
                except ValueError:
                    print('Not supported webhook event', webhook_event)

            return HttpResponse('EVENT_RECEIVED')
        raise Http404


messenger_webhook_view = csrf_exempt(MessengerWebhookView.as_view())


class IndexView(views.TemplateView):
    template_name = 'messenger_bot/index.html'

    def get_context_data(self, **kwargs):
        context_data = super(IndexView, self).get_context_data(**kwargs)
        context_data['data'] = {
            "APP_ID": settings.MESSENGER_APP_ID
        }
        return context_data


index_view = IndexView.as_view()
