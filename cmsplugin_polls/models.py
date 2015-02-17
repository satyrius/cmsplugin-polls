from cms.models import CMSPlugin
from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=200)

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)


class PollPlugin(CMSPlugin):
    poll = models.ForeignKey(Poll)
