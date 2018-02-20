from django.conf.urls import url
from .bot_handle import webhook

urlpatterns = [
    url(r'^webhook/', webhook),
]