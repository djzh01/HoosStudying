'''
***************************************************************************************
*  REFERENCES
*  Title: <YT-Django-Heroku-Deploy-Channels-Daphne>
*  Author: <veryacademy>
*  Date: <2020-09-o3>
*  Code version: <Latest>
*  URL: <https://github.com/veryacademy/YT-Django-Heroku-Deploy-Channels-Daphne>
*  Software License: <GNU License>
*
*
*
***************************************************************************************/
'''

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import SBFapp.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            SBFapp.routing.websocket_urlpatterns
        )
    ),
})
