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
"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
#from channels.auth import AuthMiddlewareStack
#from channels.routing import ProtocolTypeRouter, URLRouter
#from django.core.asgi import get_asgi_application
from channels.routing import get_default_application
#import SBFapp.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SBF.settings')
django.setup()
application = get_default_application()


#application = ProtocolTypeRouter({
 # "http": get_asgi_application(),
#  "websocket": AuthMiddlewareStack(
#        URLRouter(
 #           SBFapp.routing.websocket_urlpatterns
#        )
#    ),
#})

