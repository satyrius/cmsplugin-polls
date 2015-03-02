from helpers import TestCase
from django.http import HttpRequest


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
        k1 = poll1.voted_key
        self.assertIn(str(poll1.id), k1)

        poll2 = self.create_poll(question='Bar')
        k2 = poll2.voted_key
        self.assertIn(str(poll2.id), k2)

        self.assertNotEqual(k1, k2)

    def test_can_vote(self):
        # Can vote by default
        self.assertTrue(self.poll.can_vote())

        # Even if request has no session
        request = HttpRequest()
        self.assertTrue(self.poll.can_vote(request))

        # And if not voted yet
        request.session = {self.poll.voted_key: False}
        self.assertTrue(self.poll.can_vote(request))

        # But cannot vote if user has already voted
        request.session = {self.poll.voted_key: True}
        self.assertFalse(self.poll.can_vote(request))
