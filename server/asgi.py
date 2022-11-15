"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""
from channels.routing import ProtocolTypeRouter


application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        # "websocket": AuthMiddlewareStack(URLRouter(pink.routing.websocket_urlpatterns)),
    }
)
