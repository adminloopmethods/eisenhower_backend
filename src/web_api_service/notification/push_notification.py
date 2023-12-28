# Gour@vSh@rm@(^_^):

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from duende.settings.development import EMAIL_HOST_USER
from notification.models import NotificationConfiguration
from web_api_service.notification.notification_main_type import MAIN_TYPE
from web_api_service.notification.notification_saver import notification_saver


# EMAIL_HOST_USER = 'gousha711@gmail.com'

class PushNotifications:
    """this PushNotifications module call the push notification using calling
    """

    def __init__(self, **kwargs):
        """
        Initialization all constructor values for using duende user class
        kwargs:
        """
        self.notification_configuration_id = None
        self.kwargs = kwargs
        self.user = kwargs.get('user')
        self.user_notification_data = kwargs.get('user_notification_data')
        self.status = False
        self.reason_for_failed = None
        self.message_content = ''
        self.main_type = None
        self.notification_type = None
        self.api_service_name = kwargs.get('api_service_name', None)
        self.message_title = ''
        self.notification_category = 'PUSH'
        self.notification_for = kwargs.get('TO', 'admin')

    def notification_record(self):
        """
        notification_record_saved: all notification records data genrate the history
        return: notify_record_data
        """
        data = {
            'notification_category': self.notification_category,
            'notification_type': str(self.notification_configuration_id),
            'user': self.user,
            'notification_to': self.notification_for,
            'reason_for_failed': self.reason_for_failed,
            'message_body': self.message_content,
            'is_read': 0
        }
        notification_saver_status = notification_saver(data)
        if notification_saver_status:
            print(True)
        else:
            print(False)

    def email_send_module(self):
        try:
            subject = self.message_title
            from_email = EMAIL_HOST_USER
            to = self.email_ids_list

            html_content = render_to_string(
                self.email_html_template, 
                {
                    "OTP": self.kwargs['OTP'],
                    "username": self.passenger_details['username']
                }
            )
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, 
                text_content, 
                from_email, 
                to, 
                cc=['pycodertest@gmail.com']
            )
            msg.attach_alternative(html_content, "text/html")

            self.status = True if msg.send() else False
            self.reason_for_failed = "Email Service Not Configured" if not self.status else None
            print("!!!!!!!!!!!!!!!!!! --SUCCESS-- !!!!!!!!!!!!!!!!!")
        except Exception as msg:
            print(msg)

    def notification_type_from_api_name(self):
        """
        notification_type_from_api_name: get the notification type ID using API's Name
        return: Notification_type_id
        """
        api_name_dict = {
            '__TASKASSIGN__': MAIN_TYPE['TASK_ASSIGN'],
            '__TASKSTATUSDONE__': MAIN_TYPE['TASK_STATUS_DONE'],
            '__MEMBERADD__': MAIN_TYPE['ADD_MEMBER'],
            '__IMPORTTASK__': MAIN_TYPE['IMPORT_TASK'],
            '__TASKASSIGNE__': MAIN_TYPE['TASK_ASSIGNE'],
            '__OVERDUEDATE__': MAIN_TYPE['OVER_DUE_DATE'],
            '__TOPICADDEDD__': MAIN_TYPE['TOPIC_ADDEDD'],
            '__TOPICDELETED__': MAIN_TYPE['TOPIC_DELETED'],

        }

        self.main_type = api_name_dict[self.api_service_name]

    def notification_message_content(self):
        """ this methods used to get the content of all
        notification message according to user's notification  types
        return: notification meassage
        """
        self.notification_type_from_api_name()
        try:
            _notification = NotificationConfiguration.objects.get(
                notification_main_type=self.main_type,
                is_active=True)

            self.notification_configuration_id = _notification.id
            self.message_title = _notification.notification_type
            self.message_content = _notification.sample_content

            if self.message_content and self.main_type == MAIN_TYPE['TASK_ASSIGN']:
                self.message_content = str(self.message_content).replace(
                    "[USER]", str(self.user_notification_data['username'])).replace(
                    "[TASK]", str(self.user_notification_data['task_name']))

            if self.message_content and self.main_type == MAIN_TYPE['TASK_STATUS_DONE']:
                self.message_content = str(self.message_content).replace(
                    "[USER]", str(self.user_notification_data['username'])).replace(
                    "[TASK]", str(self.user_notification_data['task_name'])).replace(
                    "[BY-USER]", str(self.user_notification_data['done_by_username']))

            if self.message_content and self.main_type == MAIN_TYPE['TASK_ASSIGNE']:
                self.message_content = str(self.message_content).replace(
                    "[USER]", str(self.user_notification_data['username'])).replace(
                    "[TASK]", str(self.user_notification_data['task_name']))

            if self.message_content and self.main_type == MAIN_TYPE['OVER_DUE_DATE']:
                self.message_content = str(self.message_content).replace(
                    "[USER]", str(self.user_notification_data['username'])).replace(
                    "[TASK]", str(self.user_notification_data['task_name'])).replace(
                    "[DUE-DATE]", str(self.user_notification_data['due_datetime']))

            if self.message_content and self.main_type == MAIN_TYPE['TOPIC_ADDEDD']:
                self.message_content = str(self.message_content).replace(
                    "[USER]", str(self.user_notification_data['username'])).replace(
                    "[TOPIC]", str(self.user_notification_data['topic_name']))

            if self.message_content and self.main_type == MAIN_TYPE['TOPIC_DELETED']:
                self.message_content = str(self.message_content).replace(
                    "[USER]", str(self.user_notification_data['username'])).replace(
                    "[TOPIC]", str(self.user_notification_data['topic_name']))

            if self.message_content and self.main_type == MAIN_TYPE['IMPORT_TASK']:
                self.message_content = "Task has been added successfully"

        except Exception as e:
            print('NotificationConfiguration.DoesNotExist')
            print(e)
            self.message_content = str('Notification Type not Exist')
            self.reason_for_failed = str(e)

    def __call__(self):
        """
        call function call with class instance ..
        """
        self.notification_message_content()
        # start_new_thread(self.email_send_module, ())
        self.notification_record()
