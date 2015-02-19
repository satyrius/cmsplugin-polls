from helpers import TestCase


class PollTest(TestCase):
    def test_votes(self):
        self.add_choice('Yes', votes=10)
        self.add_choice('No', votes=2)
        self.add_choice('Not sure', votes=0)
        self.assertEqual(self.poll.choice_set.count(), 3)
        self.assertEqual(self.poll.total_votes, 12)
        self.assertEqual(self.poll.max_votes, 10)
