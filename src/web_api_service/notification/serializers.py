from rest_framework import serializers

from notification.models import NotificationRecord


class NotificationRecordSerializer(serializers.ModelSerializer):
    """
    NotificationRecord serializer class
    """
    notification_type = serializers.SerializerMethodField()

    class Meta:
        """
        class container with some options attached to the model
        """
        model = NotificationRecord
        fields = ('id',
                  'notification_type',
                  'notification_category',
                  'notification_to',
                  'reason_for_failed',
                  'message_body',
                  'is_read',
                  'notify_at',
                  'user')

    def get_notification_type(self, instance):
        if instance.notification_type:
            return instance.notification_type.notification_type
        return 'Title'


class NotificationHistorySaveSerializer(serializers.ModelSerializer):
    """
    NotificationRecord serializer class
    """

    class Meta:
        """
        class container with some options attached to the model
        """
        model = NotificationRecord
        fields = ('id',
                  'notification_type',
                  'notification_category',
                  'notification_to',
                  'reason_for_failed',
                  'message_body',
                  'is_read',
                  'notify_at',
                  'user')

