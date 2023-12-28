
# Gour@vSh@rm@(^_^):

from datetime import datetime

# thread for mail waiter
from _thread import start_new_thread

# smtp mailer settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# user models
from user.models import CustomUsers

# email notification type
from web_api_service.notification.notification_main_type import BCR_EMAIL_TYPE

# notification models
from notification.models import NotificationConfiguration

# email sender host
from duende.settings.development import EMAIL_HOST_USER

# notification saver func
from web_api_service.notification.notification_saver import notification_saver

# EMAIL_HOST_USER = 'gousha711@gmail.com'


class Mailer:

    def __init__(self, **kwargs):
        """
        Initialization all constructor values for using  eisenhower, BCR and BEM         
        kwargs:
        """
        self.kwargs = kwargs
        self.email_html_template = kwargs.get('email_html_template', None)
        self.notification_data = kwargs.get('notification_data', {})
        self.template_data = kwargs.get('template_data', {})
        self.sender_emails = kwargs.get('sender_emails', [])
        self.status = False
        self.reason_for_failed = None
        self.message_content = ''
        self.notification_type = None
        self.api_service_name = kwargs.get('api_service_name', None)
        self.message_title = ''
        self.notification_category = 'EMAIL'
        self.notification_for = kwargs.get('notification_to', 'admin')
        self.notification_main_type = None
        self.notification_configuration_id = None
        self.user = kwargs.get('user', None)

    def notification_record(self):
        """this notification_record_saved: all notification records data genrate 
        the history return: notify_record_data
        """
        notification_saver_status = notification_saver({
            'notification_category': self.notification_category,
            'notification_type': self.notification_configuration_id,
            'user': self.user,
            'notification_to': self.notification_for,
            'reason_for_failed': self.reason_for_failed,
            'message_body': self.message_content,
            'is_read': 0
        })
        if notification_saver_status:
            print(True)
        else:
            print(False)

    def mail_sender(self):
        try:
            subject = self.message_title
            from_email = EMAIL_HOST_USER
            to = self.sender_emails

            html_content = render_to_string(
                self.email_html_template,
                template_data
            )
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, to,
                cc=['pycodertest@gmail.com']
            )
            msg.attach_alternative(html_content, "text/html")

            self.status = True if msg.send() else False
            self.reason_for_failed = (
                "Email Service Not Configured"
                if not self.status else
                None)
            print("SUCCESS")
        except Exception as msg:
            print(msg)

    def notification_type_from_api_name(self):
        """notification_type_from_api_name: get the notification type ID 
        using API's Name
        return: Notification_type_id
        """
        self.notification_main_type = BCR_EMAIL_TYPE[self.api_service_name]

    def notification_message_content(self):
        """this notification_message_content this methods used to get the content of all
        notification message according to user's notification  types
        return: notification meassage
        """
        try:
            self.notification_type_from_api_name()
            try:
                _notification = NotificationConfiguration.objects.get(
                    notification_main_type=self.notification_main_type,
                    is_active=True)

                self.notification_configuration_id = _notification.id
                self.message_title = _notification.notification_type
                self.message_content = _notification.sample_content

                if (self.message_content and
                        self.notification_main_type == BCR_EMAIL_TYPE['SEND_CARD_TEXT']):
                    self.message_content = str(self.message_content).replace(
                        "[USER]", str(self.notification_data['username']))

            except Exception as e:
                print('NotificationConfiguration.DoesNotExist')
                print(e)
                self.message_content = str('Notification Type not Exist')
                self.reason_for_failed = str(e)
        except Exception as msg:
            print('msg {}'.format(msg))
            self.message_content = 'Notification-Type-not-Exist'

    def __call__(self):
        """
        call function call with class instance ..
        """
        self.notification_message_content()
        start_new_thread(self.mail_sender, ())
        self.notification_record()
