# import json

from channels import Group

# from . import models as work_models
# from . import serializers as work_serializers


# The "pk" keyword argument here comes from the regex capture group in
# routing.py.
def connect_work(message, pk):
    """When the user opens a WebSocket to a work stream, adds them to the
    group for that stream so they receive new post notifications.
    The notifications are actually sent in the Work model on save.
    """
    message.reply_channel.send({"accept": True})
    Group("user-1").add(message.reply_channel)


def disconnect_work(message, pk):
    """Removes the user from the work group when they disconnect.
    Channels will auto-cleanup eventually, but it can take a while, and having old
    entries cluttering up your group will reduce performance.
    """
    Group("user-1").discard(message.reply_channel)

"""
def save_work(message, pk):
    Saves work to the database.

    work = json.loads(message['text'])['post']
    liveblog = work_models.Work.objects.get(pk=pk)
    Post.objects.create(liveblog=liveblog, body=post)
"""
