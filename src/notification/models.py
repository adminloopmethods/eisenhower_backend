import uuid

from django.db import models

# import the helpful module for using notification
from core.constants import NOTIFICATION_FOR, DEVICE_TYPE, NOTIFICATION_CATEGORY

# import abstract modules
from core.models import ABSTRACTDateModel
from core.models import ABSTRACTStatusModel
from core.models import ABSTRACTCreateUpdateByModel

# import User
from user.models import CustomUsers


# Create your models here.

class NotificationConfiguration(ABSTRACTDateModel,
                                ABSTRACTStatusModel,
                                ABSTRACTCreateUpdateByModel):
    """
    NotificationConfiguration
    this model manage all
    notification configuration types
    """
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # Notification main types.
    notification_main_type = models.CharField(max_length=100)  # for backend use
    notification_type = models.CharField(max_length=100)

    # Notification sample content use for trigger notification.
    description = models.CharField(max_length=200, null=True, blank=True)
    notification_for = models.CharField(max_length=50, choices=NOTIFICATION_FOR)
    sample_content = models.TextField()

    class Meta:
        verbose_name = ' Notification Configuration'
        verbose_name_plural = ' Notification Configuration'
        db_table = 'notification_configuration'

    def __str__(self):
        return str(self.notification_type)


class NotificationRecord(models.Model):
    """
    NotificationRecord
    all types of users
    notification history
    """
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    notification_category = models.CharField(
        choices=NOTIFICATION_CATEGORY, max_length=20)
    notification_to = models.CharField(choices=NOTIFICATION_FOR, max_length=50)
    notification_type = models.ForeignKey(
        NotificationConfiguration,
        on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    reason_for_failed = models.TextField(
        verbose_name='Reason For Non Delivery',
        null=True, blank=True)
    message_body = models.TextField(verbose_name='Notification Content')
    is_read = models.BooleanField(default=False)

    notify_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Notification Date & Time')

    class Meta:
        verbose_name = 'Notification History'
        verbose_name_plural = 'Notification History'
        db_table = 'notification_record'

    def __str__(self):
        return str(self.notification_type)


class NotificationFirebaseToken(ABSTRACTStatusModel):
    """
    NotificationFirebaseToken
    store all types of user
    notification firebase token
    """
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    device_token = models.TextField(verbose_name='Fire base Token')
    device_type = models.CharField(
        choices=DEVICE_TYPE,
        max_length=30,
        verbose_name="Device Type")
    user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Notification Firebase'
        verbose_name_plural = 'Notification Firebase'

    def __str__(self):
        return self.device_token
