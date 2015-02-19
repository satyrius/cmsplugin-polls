from cms.models import CMSPlugin
from django.db import models


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


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)


class PollPlugin(CMSPlugin):
    poll = models.ForeignKey(Poll)
