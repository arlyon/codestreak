from django.contrib import admin
from .models import AcceptedEvent, Language, Session, Streak

# Register your models here.

admin.site.register(AcceptedEvent)
admin.site.register(Language)
admin.site.register(Session)
admin.site.register(Streak)
