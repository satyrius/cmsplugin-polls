from helpers import TestCase


class VoteViewTest(TestCase):
    def setUp(self):
        super(VoteViewTest, self).setUp()
        self.url = '/polls/vote'

    def test_get_not_allowed(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 405)

    def post(self, assert_code=200, *args, **kwargs):
        res = self.client.post(self.url, *args, **kwargs)
        self.assertEqual(res.status_code, assert_code)
        return res

    def vote(self, *args, **kwargs):
        kwargs.setdefault('data', {})['poll'] = self.poll.id
        return self.post(*args, **kwargs)

    def test_vote_for_unknown_poll(self):
        self.post(data={'poll': 0}, assert_code=400)
        self.post(data={'poll': 'foo'}, assert_code=400)

    def test_redirect_on_success(self):
        server = 'http://testserver'

        # The use will be redirected to the 'next' url if specified
        url = '/foo/bar/'
        res = self.vote(data={'next': url}, assert_code=302)
        self.assertEqual(res['Location'], server + url)

        # Otherwise the HTTP_REFERER will be used to redirect user back
        ref = '/bla/bla/'
        res = self.vote(assert_code=302, **{'HTTP_REFERER': ref})
        self.assertEqual(res['Location'], server + ref)

        # If nothig above, he just got an OK page
        res = self.vote()
        self.assertEqual(res.content, 'OK')
