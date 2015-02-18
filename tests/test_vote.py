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

    def reload(self, obj):
        return obj.__class__.objects.get(pk=obj.pk)

    def test_choice(self):
        yes = self.add_choice('Yes')
        no = self.add_choice('No')
        self.vote(data={'choice': yes.id})

        yes = self.reload(yes)
        self.assertEqual(yes.votes, 1)

        no = self.reload(no)
        self.assertEqual(no.votes, 0)

    def test_invalid_choice(self):
        yes = self.add_choice('Yes')
        foo = yes.id + 1
        res = self.vote(data={'choice': foo}, assert_code=400)
        self.assertEqual(res.content, 'Invalid choice')

        res = self.vote(data={'choice': 'bar'}, assert_code=400)
        self.assertEqual(res.content, 'Invalid choice')
