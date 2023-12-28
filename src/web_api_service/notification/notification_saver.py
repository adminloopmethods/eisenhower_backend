from web_api_service.notification.serializers import NotificationHistorySaveSerializer


def notification_saver(data):
    """this notification saver used to update the notification configuration
    """
    _notification_data = NotificationHistorySaveSerializer(data=data)
    if _notification_data.is_valid(raise_exception=True):
        _notification_data.save()
        return True
    return False
