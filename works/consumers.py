from channels import Group


def connect_work(message, pk):
    """When the user opens a WebSocket to a work stream, adds them to the
    group for that stream so they receive new post notifications.
    The notifications are actually sent in the Work model on save.

    @TODO: Connect socket to correct group depending on user id
    """
    message.reply_channel.send({"accept": True})
    Group("user-2").add(message.reply_channel)


def disconnect_work(message, pk):
    """Removes the user from the work group when they disconnect.
    Channels will auto-cleanup eventually, but it can take a while, and having old
    entries cluttering up your group will reduce performance.

    @TODO: Disconnect socket to correct group depending on user id
    """
    Group("user-2").discard(message.reply_channel)
