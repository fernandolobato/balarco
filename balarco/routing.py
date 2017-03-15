"""The channel routing defines what channels get handled by what consumers,
including optional matching on message attributes. WebSocket messages of all
types have a 'path' attribute, so we're using that to route the socket.
While this is under stream/ compared to the HTML page, we could have it on the
same URL if we wanted; Daphne separates by protocol as it negotiates with a browser.
"""

from channels import route
from works.consumers import connect_work, disconnect_work


channel_routing = [
    # @TODO: Correct urls
    # Called when incoming WebSockets connect
    route("websocket.connect", connect_work, path=r'^/works/works/(?P<pk>[^/]+)/stream/$'),

    # Called when the client closes the socket
    route("websocket.disconnect", disconnect_work, path=r'^/works/works/(?P<pk>[^/]+)/stream/$'),
]