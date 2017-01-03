from huey.contrib.djhuey import crontab, db_periodic_task
from codestreak.models import Streak

@db_periodic_task(crontab(hour="20", minute="0"))
def update_streak():
    for streaker in Streak.objects.all():
        streaker.check_streak()