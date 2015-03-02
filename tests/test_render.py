from bs4 import BeautifulSoup
from django.http import HttpRequest
from django.template import Context, RequestContext
from mock import patch

from cmsplugin_polls.models import Poll
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

    def test_results(self):
        self.add_choice('Yes', votes=10)
        self.add_choice('No', votes=2)
        plugin = self.add_plugin(poll=self.poll)

        with patch.object(Poll, 'can_vote', return_value=False):
            html = self.render(plugin)
            soup = BeautifulSoup(html)

        yes = soup.find_all('span', class_='label', text='Yes')[0]
        quantity = yes.find_parent('div').find_all('div', class_='result-quantity')[0]
        self.assertEqual(int(quantity.find(text=True)), 10)
        bar = yes.find_parent('div').find_all('div', class_='result-bar')[0]
        self.assertEqual(bar['style'], 'width: 100%')

        no = soup.find_all('span', class_='label', text='No')[0]
        quantity = no.find_parent('div').find_all('div', class_='result-quantity')[0]
        self.assertEqual(int(quantity.find(text=True)), 2)
        bar = no.find_parent('div').find_all('div', class_='result-bar')[0]
        self.assertEqual(bar['style'], 'width: 20%')
