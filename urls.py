from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='root'),
    url(r'^updatetimezone', views.update_timezone, name='update_timezone'),
    url(r'^quit', views.quit, name='quit'),
]
