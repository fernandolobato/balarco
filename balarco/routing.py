"""The channel routing defines what channels get handled by what consumers,
including optional matching on message attributes. WebSocket messages of all
types have a 'path' attribute, so we're using that to route the socket.
While this is under stream/ compared to the HTML page, we could have it on the
same URL if we wanted; Daphne separates by protocol as it negotiates with a browser.
"""

from channels import route
from works import consumers as work_consumers
from users import consumers as user_consumers


channel_routing = [
    # @TODO: Correct urls
    # Called when incoming WebSockets connect
    route("websocket.connect", work_consumers.connect_work, path=r'^/dashboard/(?P<pk>[^/]+)/stream/$'),
    # Called when the client closes the socket
    route("websocket.disconnect", work_consumers.disconnect_work, path=r'^/dashboard/(?P<pk>[^/]+)/stream/$'),

    route("websocket.connect", user_consumers.connect_users_table,
    	  path=r'^/users/stream/$'),
    route("websocket.disconnect", user_consumers.disconnect_users_table,
    	  path=r'^/users/stream/$'),
]
