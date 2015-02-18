from bs4 import BeautifulSoup
from django.http import HttpRequest
from django.template import Context, RequestContext

from helpers import TestCase


class PollPluginRenderTest(TestCase):
    def render(self, plugin, ctx=None):
        return plugin.render_plugin(ctx or Context())

    def test_template_render(self):
        plugin = self.add_plugin(poll=self.poll)
        # Switch on template debug to catch all template errors
        with self.settings(TEMPLATE_DEBUG=True):
            self.render(plugin)

    def test_form_action(self):
        plugin = self.add_plugin(poll=self.poll)
        html = self.render(plugin)
        soup = BeautifulSoup(html)
        self.assertEqual(soup.form['action'], '/polls/vote')
        self.assertEqual(soup.form['method'], 'POST')

    def get_request(self, path=''):
        request = HttpRequest()
        request.current_page = None
        request.path = path
        return request

    def test_form_hidden_fields(self):
        plugin = self.add_plugin(poll=self.poll)
        context = RequestContext(self.get_request('/foo/bar/'))
        html = self.render(plugin, ctx=context)

        soup = BeautifulSoup(html)
        hidden = {i['name']: i for i in soup.form.find_all(type='hidden')}

        self.assertIn('poll', hidden)
        self.assertEqual(int(hidden['poll']['value']), self.poll.id)

        self.assertIn('next', hidden)
        self.assertEqual(hidden['next']['value'], '/foo/bar/')

    def test_choices(self):
        self.add_choice('Yes')
        self.add_choice('No')
        self.add_choice('This is not the choice you are looking for')
        plugin = self.add_plugin(poll=self.poll)

        html = self.render(plugin)
        soup = BeautifulSoup(html)
        choices = {int(i['value']) for i in soup.form.find_all(type='radio')}
        self.assertEqual(
            choices, set(self.poll.choice_set.values_list('id', flat=True)))
