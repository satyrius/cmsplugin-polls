from helpers import TestCase
from django.http import HttpRequest
from mock import patch
from cmsplugin_polls.models import Poll


class PollTest(TestCase):
    def test_votes(self):
        self.add_choice('Yes', votes=10)
        self.add_choice('No', votes=2)
        self.add_choice('Not sure', votes=0)
        self.assertEqual(self.poll.choice_set.count(), 3)
        self.assertEqual(self.poll.total_votes, 12)
        self.assertEqual(self.poll.max_votes, 10)

    def test_voted_key(self):
        poll1 = self.create_poll(question='Foo')
        k1 = poll1._voted_key
        self.assertIn(str(poll1.id), k1)

        poll2 = self.create_poll(question='Bar')
        k2 = poll2._voted_key
        self.assertIn(str(poll2.id), k2)

        self.assertNotEqual(k1, k2)

    def test_can_vote(self):
        # Can vote by default
        self.assertTrue(self.poll.can_vote())

        # Even if request has no session
        request = HttpRequest()
        self.assertTrue(self.poll.can_vote(request))

        # And if not voted yet
        request.session = {self.poll._voted_key: False}
        self.assertTrue(self.poll.can_vote(request))

        # But cannot vote if user has already voted
        request.session = {self.poll._voted_key: True}
        self.assertFalse(self.poll.can_vote(request))

    def test_cannot_vote_if_not_active(self):
        self.assertTrue(self.poll.is_active)
        self.assertTrue(self.poll.can_vote())

        self.poll.is_active = False
        self.assertFalse(self.poll.can_vote())

    @patch.object(Poll, 'can_vote', return_value=True)
    def test_vote(self, can_vote):
        yes = self.add_choice('Yes')
        self.assertEqual(yes.votes, 0)
        no = self.add_choice('No')
        self.assertEqual(no.votes, 0)
        request = HttpRequest()
        request.session = {}

        # Invalid choice id
        self.assertEqual(self.poll.vote('yes'), 0)
        self.assertFalse(can_vote.called)
        self.assertEqual(self.poll.total_votes, 0)

        can_vote.return_value = False
        self.assertEqual(self.poll.vote(yes.id, request), 0)
        can_vote.assert_called_once_with(request)
        self.assertEqual(self.poll.total_votes, 0)

        can_vote.return_value = True
        can_vote.reset_mock()
        self.assertEqual(self.poll.vote(yes.id, request), 1)
        can_vote.assert_called_once_with(request)
        self.assertEqual(self.poll.total_votes, 1)
        self.assertEqual(self.reload_choice(yes).votes, 1)
        self.assertEqual(self.reload_choice(no).votes, 0)

        self.assertTrue(request.session[self.poll._voted_key])
