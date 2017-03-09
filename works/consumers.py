import json

from channels import Group

from . import models as work_models
from . import serializers as work_serializers


# The "pk" keyword argument here comes from the regex capture group in
# routing.py.
def connect_work(message, pk):
    """When the user opens a WebSocket to a work stream, adds them to the
    group for that stream so they receive new post notifications.
    The notifications are actually sent in the Work model on save.
    """
    # Try to fetch the liveblog by pk; if that fails, close the socket.
    try:
        work = work_models.Work.objects.get(pk=pk)
    except work_models.Work.DoesNotExist:
        # You can see what messages back to a WebSocket look like in the spec:
        # http://channels.readthedocs.org/en/latest/asgi.html#send-close
        # Here, we send "close" to make Daphne close off the socket, and some
        # error text for the client.
        message.reply_channel.send({
            # WebSockets send either a text or binary payload each frame.
            # We do JSON over the text portion.
            "text": json.dumps({"error": "bad_pk"}),
            "close": True,
        })
        return
    message.reply_channel.send({"accept": True})
    # Each different client has a different "reply_channel", which is how you
    # send information back to them. We can add all the different reply channels
    # to a single Group, and then when we send to the group, they'll all get the
    # same message.
    Group(work.group_name).add(message.reply_channel)


def disconnect_work(message, pk):
    """Removes the user from the work group when they disconnect.
    Channels will auto-cleanup eventually, but it can take a while, and having old
    entries cluttering up your group will reduce performance.
    """
    try:
        work = work_models.Work.objects.get(pk=pk)
    except work_models.Work.DoesNotExist:
        # This is the disconnect message, so the socket is already gone; we can't
        # send an error back. Instead, we just return from the consumer.
        return
    # It's called .discard() because if the reply channel is already there it
    # won't fail - just like the set() type.
    Group(work.group_name).discard(message.reply_channel)

"""
def save_work(message, pk):
    Saves work to the database.
    
    work = json.loads(message['text'])['post']
    liveblog = work_models.Work.objects.get(pk=pk)
    Post.objects.create(liveblog=liveblog, body=post)
"""