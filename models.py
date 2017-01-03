from django.db import models
from django.contrib.auth.models import User
import requests
import json
from datetime import datetime, timedelta
import dateutil.parser
from pushbullet import PushBullet
from settings_local import PUSHBULLET_KEY

# Create your models here.

class AcceptedEvent(models.Model):
    name = models.TextField()

class Streak(models.Model):
    user = models.ForeignKey(User)
    streak = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now())

    def update_streak(self, test_for_fail=False):
        """Updates the streak. Run by huey at midnight."""
        GITHUB_API = "https://api.github.com/users/{0}/events".format(self.user.username)

        accepted_events = AcceptedEvent.objects.values_list("name", flat=True)
        events = json.loads(requests.get(GITHUB_API).text)
        for event in events:
            # it needs to be either a commit or a pull request
            # it must also be after the last update.
            if event["type"] in accepted_events \
                    and self.date < dateutil.parser.parse(event["created_at"]):
                if test_for_fail is False:
                    self.streak += 1
                    self.date = datetime.now()
                    self.save()
                else:
                    return(False)
        else:
            # no commits, streak broken :(
            if test_for_fail is False:
                self.streak = 0
                self.date = datetime.now()
                self.save()
            else:
                return (True)

    def notify_streak(self):
        pb = PushBullet(PUSHBULLET_KEY)
        if self.update_streak(test_for_fail=True):
            push = pb.push_note("You're risking your streak!",
                                "It's quite late and you still haven't made a commit. Hurry!")
        else:
            push = pb.push_note("Well done. You comitted today.",
                                "You have done well.")
