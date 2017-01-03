from django.db import models
from django.contrib.auth.models import User
import requests
import json
from datetime import datetime, timedelta
import dateutil.parser

# Create your models here.

class Streak(models.Model):
    user = models.ForeignKey(User)
    streak = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now())

    def check_streak(self):
        ACCEPTED_EVENTS = ["ForkEvent"]
        GITHUB_API = "https://api.github.com/users/{0}/events".format(self.user.username)
        events = json.loads(requests.get(GITHUB_API).text)
        for event in events:
            if event["type"] in ACCEPTED_EVENTS and self.date < dateutil.parser.parse(event["created_at"]):
                self.streak+=1
                self.date=datetime.now()
                break
            else:
                print(event["created_at"])
