import json
from django.test import RequestFactory
from django.http import HttpResponse
from django.views.generic import View
from mock import patch

from helpers import TestCase
from cmsplugin_polls.models import Poll
from cmsplugin_polls.views import Vote


class ViewTest(TestCase):
    def setUp(self):
        super(ViewTest, self).setUp()
        self.view = Vote.as_view()
        self.factory = RequestFactory()
        self.url = '/polls/vote'

    def test_get_not_allowed(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, 405)

    def test_invalid_poll(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

        request = self.factory.post(self.url, {'poll': 'foo'})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    @patch.object(Poll, 'can_vote', return_value=False)
    def test_cannot_vote(self, can_vote):
        request = self.factory.post(self.url, {'poll': self.poll.id})
        response = self.view(request)
        can_vote.assert_canned_once_with(request)
        self.assertEqual(response.status_code, 403)

    @patch.object(Poll, 'can_vote', return_value=True)
    def test_no_choice(self, can_vote):
        request = self.factory.post(self.url, {'poll': self.poll.id})
        response = self.view(request)
        can_vote.assert_canned_once_with(request)
        self.assertEqual(response.status_code, 400)

    @patch.object(Poll, 'can_vote', return_value=True)
    def test_vote_error(self, can_vote):
        request = self.factory.post(self.url, {
            'poll': self.poll.id, 'choice': 123
        })
        with patch.object(Poll, 'vote', return_value=0) as vote:
            response = self.view(request)
            vote.assert_canned_once_with(123, request)
        can_vote.assert_canned_once_with(request)
        self.assertEqual(response.status_code, 400)

    @patch.object(Poll, 'can_vote', return_value=True)
    def test_vote_ok(self, can_vote):
        request = self.factory.post(self.url, {
            'poll': self.poll.id, 'choice': 123
        })
        with patch.object(Poll, 'vote', return_value=1) as vote:
            response = self.view(request)
            vote.assert_canned_once_with(123, request)
        can_vote.assert_canned_once_with(request)
        self.assertEqual(response.status_code, 200)

    def test_json(self):
        message = 'got it!'
        response = HttpResponse(content=message, status=123)
        res = Vote().to_json(response)
        self.assertEqual(res.status_code, response.status_code)
        self.assertEqual(res['Content-Type'], 'application/json')
        data = json.loads(res.content)
        self.assertEqual(data['status'], response.status_code)
        self.assertEqual(data['message'], message)

    def test_is_ajax(self):
        request = self.factory.post(self.url)
        view = Vote(request=request)
        with patch.object(request, 'is_ajax') as is_ajax:
            is_ajax.return_value = True
            self.assertTrue(view.is_ajax())
            is_ajax.assert_called_once()

            is_ajax.reset_mock()
            is_ajax.return_value = False
            self.assertFalse(view.is_ajax())
            is_ajax.assert_called_once()

    @patch.object(Vote, 'is_ajax')
    def test_next_page(self, is_ajax):
        view = Vote(request=self.factory.post(self.url))
        is_ajax.return_value = True
        self.assertIsNone(view.next_page())

        is_ajax.return_value = False
        request = self.factory.post(self.url)
        request.META['HTTP_REFERER'] = '/foo/bar/'
        view = Vote(request=request)
        self.assertEqual(view.next_page(), '/foo/bar/')

        view = Vote(request=self.factory.post(self.url, {'next': '/w/t/f/'}))
        self.assertEqual(view.next_page(), '/w/t/f/')

    @patch.object(Vote, 'is_ajax', return_value=True)
    @patch.object(Vote, 'to_json')
    @patch.object(View, 'dispatch')
    def test_dispatch_ajax(self, dispatch, to_json, is_ajax):
        request = self.factory.post(self.url)
        response = self.view(request)
        is_ajax.assert_called_once()
        to_json.assert_called_once_with(dispatch.return_value)
        self.assertEqual(response, to_json.return_value)

    @patch.object(Vote, 'is_ajax', return_value=False)
    @patch.object(Vote, 'next_page', return_value='/foo/bar/')
    @patch.object(Vote, 'to_json')
    @patch.object(View, 'dispatch')
    def test_dispatch_returns_redirect(self, dispatch, to_json, next_page, is_ajax):
        request = self.factory.post(self.url)
        response = self.view(request)
        is_ajax.assert_called_once()
        self.assertFalse(to_json.called)
        next_page.assert_called_once()
        self.assertEqual(response['Location'], '/foo/bar/')

    @patch.object(Vote, 'is_ajax', return_value=False)
    @patch.object(Vote, 'next_page', return_value=None)
    @patch.object(Vote, 'to_json')
    @patch.object(View, 'dispatch')
    def test_dispatch_without_redirect(self, dispatch, to_json, next_page, is_ajax):
        request = self.factory.post(self.url)
        response = self.view(request)
        is_ajax.assert_called_once()
        self.assertFalse(to_json.called)
        next_page.assert_called_once()
        self.assertEqual(response, dispatch.return_value)
