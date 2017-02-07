from django.db import models
from django.contrib.auth.models import User
import requests
import json
from datetime import datetime, timedelta
import dateutil.parser
from pushbullet import PushBullet
from settings_local import PUSHBULLET_KEY, GITLAB_KEY, GITLAB_URL
import html5lib
from django.utils.crypto import get_random_string
from django.core import urlresolvers

# Create your models here.


class AcceptedEvent(models.Model):
    name = models.TextField()


class Language(models.Model):
    name = models.TextField()


class Session(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    language = models.ForeignKey(Language)


class Streak(models.Model):
    uuid = models.CharField(default=get_random_string(length=10), max_length=10, primary_key=True)
    user = models.ForeignKey(User)
    streak = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()
    utc_offset = models.PositiveIntegerField(default=0)
    lost = models.BooleanField(default=False)
    sessions = models.ManyToManyField(Session)

    def update_streak(self, test_for_success=False):
        """Updates the streak. Run by huey at midnight. True means streak is incremented, false means failure.

        Attribute:
            test_for_success: when true the result is simulated but not saved."""

        pb = PushBullet(PUSHBULLET_KEY)

        def github():
            """Checks if a commit has been made in the last 24 hours."""
            try:
                GITHUB_API = "https://api.github.com/users/{0}/events".format(self.user.username)

                accepted_events = AcceptedEvent.objects.values_list("name", flat=True)
                events = json.loads(requests.get(GITHUB_API).text)
                for event in events:
                    # it needs to be either a commit or a pull request
                    # it must also be after the last update.
                    if event["type"] in accepted_events \
                            and self.date < dateutil.parser.parse(event["created_at"]):
                        return True
                else:
                    return False
            except:
                return False

        def freecodecamp():
            """Checks your freecodecamp profile for progress matching today's date."""
            try:
                CODECAMP_URL = "https://www.freecodecamp.com/{0}".format(self.user.username)
                document = html5lib.parse(requests.get(CODECAMP_URL).text)
                if document.findtext((datetime.now()-timedelta(days=1)).strftime("%b %d, %Y"), default=None) is None:
                    return False
                return True
            except:
                return False

        def gitlab():
            try:
                repos_endpoint = "/api/v3/projects"
                repos = json.loads(requests.get(
                    "{0}{1}?order_by=last_activity_at&private_token={2}".format(GITLAB_URL, repos_endpoint, GITLAB_KEY)).text)

                commits_endpoint = "/api/v3/projects/{0}/repository/commits"
                for repo in repos:
                    commits = json.loads(requests.get(
                        "{0}{1}?order_by=last_activity_at&private_token={2}".format(GITLAB_URL,
                                                                                    commits_endpoint.format(repo["id"]),
                                                                                    GITLAB_KEY)).text)

                    # if we get to a repo hasn't been updated in the last 24 hours, return false
                    # (they are ordered by latest activity)
                    if self.date > dateutil.parser.parse(repo["last_activity_at"]):
                        return False

                    for commit in commits: # if the date is not in the last day, break
                        if self.date < dateutil.parser.parse(commit["created_at"]):
                            # if we have the right guy, return true
                            if commit["author_name"] == self.user.username:
                                return True
                        else:
                            break
            except:
                return False

        def session():
            date_from = datetime.now() - timedelta(days=1)

            if self.sessions.objects.filter(start__gte=date_from):
                return True

            return False

        successful = gitlab() or github() or freecodecamp() or session()

        if test_for_success is False:
            self.streak += (1*int(successful)*int(self.lost))  # stops you getting more points after losing.
            self.lost = not successful or self.lost  # if you lost, it will stay until you open the app.
            self.date = datetime.now()
            if self.lost:
                push = pb.push_link(urlresolvers.resolve("codestreak:root"), "Your streak is over! Visit the app to reset.")
            self.save()
        else:
            if successful:
                push = pb.push_note("Well done. You made a commit today.", ":)")
            else:
                push = pb.push_note("You're risking your streak!", "It's quite late and you still haven't made a commit. Hurry!")

        return True if successful else False

    def notify_streak(self):
        self.update_streak(test_for_success=True)

