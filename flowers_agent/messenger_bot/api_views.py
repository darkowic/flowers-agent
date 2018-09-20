from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from flowers_agent.messenger_bot.models import Flower, MessengerUser
from flowers_agent.messenger_bot.serializers import FlowerSerializer


class FlowerSet(viewsets.ModelViewSet):
    """
    API endpoint that allows flowers to be viewed or edited.
    """
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer

    @property
    def user_psid(self):
        return self.request.POST['psid']

    @property
    def user(self):
        return get_object_or_404(MessengerUser, psid=self.user_psid)

    def perform_create(self, serializer):
        serializer.save(user=self.user)
