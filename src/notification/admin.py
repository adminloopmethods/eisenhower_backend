from django.contrib import admin

from notification.models import NotificationConfiguration, NotificationRecord

# Register your models here.


admin.site.register(NotificationConfiguration)
admin.site.register(NotificationRecord)