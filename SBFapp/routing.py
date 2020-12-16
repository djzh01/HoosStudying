# chat/routing.py
'''
***************************************************************************************
*  REFERENCES
*  Title: <Channels tutorial>
*  Author: <Carlton Gibson>
*  Date: <2020-10-23>
*  Code version: <3.0.0>
*  URL: <https://github.com/django/channels/tree/master/docs/tutorial>
*  Software License: <GNU License>
*
*
*
***************************************************************************************/
'''
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
