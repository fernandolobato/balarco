"""The channel routing defines what channels get handled by what consumers,
including optional matching on message attributes. WebSocket messages of all
types have a 'path' attribute, so we're using that to route the socket.
While this is under stream/ compared to the HTML page, we could have it on the
same URL if we wanted; Daphne separates by protocol as it negotiates with a browser.
"""

from channels import route
from works import consumers as work_consumers
from users import consumers as user_consumers
from clients import consumers as client_consumers


channel_routing = [
    # @TODO: Correct urls
    # Called when incoming WebSockets connect
    route("websocket.connect", work_consumers.connect_work,
          path=r'^/api/works/stream/(?P<pk>[^/]+)$'),
    # Called when the client closes the socket
    route("websocket.disconnect", work_consumers.disconnect_work,
          path=r'^/api/works/stream/(?P<pk>[^/]+)$'),

    route("websocket.connect", user_consumers.connect_users_table,
          path=r'^/api/users/stream/$'),
    route("websocket.disconnect", user_consumers.disconnect_users_table,
          path=r'^/api/users/stream/$'),

    route("websocket.connect", client_consumers.connect_clients_table,
          path=r'^/api/clients/stream/$'),
    route("websocket.disconnect", client_consumers.disconnect_clients_table,
          path=r'^/api/clients/stream/$'),

    route("websocket.connect", client_consumers.connect_contacts_table,
          path=r'^/api/contacts/stream/$'),
    route("websocket.disconnect", client_consumers.disconnect_contacts_table,
          path=r'^/api/contacts/stream/$'),

    route("websocket.connect", work_consumers.connect_igualas_table,
          path=r'^/api/igualas/stream/$'),
    route("websocket.disconnect", work_consumers.disconnect_igualas_table,
          path=r'^/api/igualas/stream/$'),
]
