from django.test import TestCase, override_settings
from django.urls import reverse

TEST_VERIFY_TOKEN = 'test_verify_token'


@override_settings(MESSENGER_VERIFY_TOKEN=TEST_VERIFY_TOKEN)
class MessengerWebhookViewTest(TestCase):
    def test_get_verifies_token_successfully(self):
        response = self.client.get(
            '{url}?hub.mode=subscribe&hub.verify_token={token}&hub.challenge=challenge_text'.format(
                url=reverse('index'),
                token=TEST_VERIFY_TOKEN,
            ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"challenge_text")

    def test_get_forbidden_when_incorrect_mode(self):
        response = self.client.get(
            '{url}?hub.mode=other_mode&hub.verify_token={token}&hub.challenge=challenge_text'.format(
                url=reverse('index'),
                token=TEST_VERIFY_TOKEN,
            ))
        self.assertEqual(response.status_code, 403)

    def test_get_forbidden_when_incorrect_token(self):
        response = self.client.get(
            '{url}?hub.mode=subscribe&hub.verify_token={token}&hub.challenge=challenge_text'.format(
                url=reverse('index'),
                token='incorrect_token',
            ))
        self.assertEqual(response.status_code, 403)

    def test_forbidden_when_no_get_parameters(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 403)
