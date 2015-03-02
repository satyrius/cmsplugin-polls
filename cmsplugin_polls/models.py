from cms.models import CMSPlugin
from django.db import models
from django.db.models import F


class Poll(models.Model):
    question = models.CharField(max_length=200)

    def __unicode__(self):
        return self.question

    @property
    def total_votes(self):
        return self.choice_set.aggregate(models.Sum('votes'))['votes__sum']

    @property
    def max_votes(self):
        return self.choice_set.aggregate(models.Max('votes'))['votes__max']

    @property
    def _voted_key(self):
        return 'cmsplugin_poll_voted_{i}'.format(i=self.id)

    def can_vote(self, request=None):
        if not request or not hasattr(request, 'session'):
            return True
        return not request.session.get(self._voted_key, False)

    def vote(self, choice, request=None):
        try:
            choice = int(choice)
        except ValueError:
            return 0
        if not self.can_vote(request):
            return 0
        rows = self.choice_set.filter(id=choice).update(votes=F('votes') + 1)
        if rows and request and hasattr(request, 'session'):
            request.session[self._voted_key] = True
        return rows


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)


class PollPlugin(CMSPlugin):
    poll = models.ForeignKey(Poll)
