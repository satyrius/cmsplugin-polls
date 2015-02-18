from django.test import TestCase


class VoteViewTest(TestCase):
    def setUp(self):
        self.url = '/polls/vote'

    def test_get_not_allowed(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 405)
