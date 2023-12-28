# import serializers
from core.api_response_parser import final_response, bad_request_response
from core.messages import MSG
from notification.models import NotificationRecord
from web_api_service.notification.serializers import NotificationRecordSerializer


class NotificationService:
    """
    NotificationService
    """

    def __init__(self, **kwargs):
        self.auth_instance = kwargs.get('auth_instance', None)
        self.final = final_response()
        self.bad_request = bad_request_response()

    def notification_count(self):
        """this method used to get the notification count
        """
        try:
            notification_count = NotificationRecord.objects.filter(
                user=self.auth_instance.user_auth.id,
                notification_category__in=[
                    'PUSH',
                    'SMS',
                    'EMAIL'
                ],
                is_read=False
            ).count()
        except Exception as e:
            notification_count = 0
            print('NotificationRecordCountErr')
            print(e)

        self.final['key'] = 'unread_notification_count'
        self.final['data'] = notification_count

        return self.final

    def notification_record(self):
        """this method used to get the notification record
        """
        try:
            _notification_records = NotificationRecord.objects.filter(
                user_id=self.auth_instance.user_auth.id,
                notification_category__in=['PUSH', 'SMS', 'EMAIL'],
            )

            _notification = _notification_records.order_by('-notify_at')
            if not _notification:
                self.bad_request['message'] = MSG['NOTIFICATION_NOT_FOUND']
                return self.bad_request

            if _notification_records:
                last_notification = _notification_records.last().id
                NotificationRecord.objects.filter(
                    id__lte=last_notification,
                    user=self.auth_instance.user_auth.id
                ).update(is_read=1)

                try:
                    notification_data = NotificationRecordSerializer(_notification,
                                                                    many=True).data
                except Exception as e:
                    notification_data = []
                    print('NotificationRecordSerializerErr')
                    print(e)

                self.final['key'] = 'notification_record'
                self.final['data'] = notification_data
                return self.final
            else:
                self.bad_request['message'] = MSG['NOTIFICATION_NOT_FOUND']
                return self.bad_request
        except Exception as error:
            self.bad_request['message'] = str(error)
            return self.bad_request


