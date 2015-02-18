from cms.api import add_plugin
from cms.models import Placeholder
from django.test import TestCase as DjangoTestCase

from cmsplugin_polls.models import Poll
from cmsplugin_polls.cms_plugins import PollPlugin


class TestCase(DjangoTestCase):
    def setUp(self):
        self.placeholder = Placeholder.objects.create(slot='test')
        self.poll = Poll.objects.create(question='Do you like my plugin?')

    def add_choice(self, text, **kwargs):
        return self.poll.choice_set.create(text=text, **kwargs)

    def add_plugin(self, **kwargs):
        model_instance = add_plugin(
            self.placeholder,
            PollPlugin,
            'en',
            **kwargs)
        return model_instance
