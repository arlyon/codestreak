from huey.contrib.djhuey import crontab, periodic_task
from codestreak.models import Streak
from timeit import default_timer as timer
from datetime import datetime


def huey_print(data, string, overwrite=False):
    if overwrite:
        print("[{0} - {2:2.0f}s] {1}".format(data["name"], string, timer() - data["start"]), end='\r')
    else:
        print("[{0} - {2:2.0f}s] {1}".format(data["name"], string, timer()-data["start"]))


@periodic_task(crontab(minute="0"))
def update_streak():
    data = {"start": timer(),
            "name": "Update Streak"}
    huey_print(data, "Initializing.")
    # -23 / +1 because at hour 00 (local time) we want offset one (utc) to be triggered. (0+1 = one)
    offset = datetime.now().hour+1 % 24
    for streaker in Streak.objects.filter(utc_offset=offset).all():
        if streaker.update_streak():
            huey_print(data, "{0} passed!".format(streaker.user.username))
        else:
            huey_print(data, "{0} failed.".format(streaker.user.username))
    huey_print(data, "Complete.")


@periodic_task(crontab(minute="0"))
def notify_streak():
    data = {"start": timer(),
            "name": "Notify Streak"}
    huey_print(data, "Initializing.")
    # -19 / +5 because at hour 20 we want offset one to be triggered. (20-19 = one)
    offset = datetime.now().hour+5 % 24
    for streaker in Streak.objects.filter(utc_offset=offset).all():
        streaker.notify_streak()
    huey_print(data, "Complete.")