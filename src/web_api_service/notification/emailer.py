
# Gour@vSh@rm@(^_^):

from datetime import datetime
from _thread import start_new_thread
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from passenger.models import Passenger

from helper.response_parser import SerializerErrorParser

from web_api_service.notification.notification_main_type import (
    NOTIFICATION_MAIN_TYPE,)

from web_api_service.notification.serializers import (
    NotificationRecordSerializer, 
    NotificationHistorySaveSerializer)

from notifications.models import NotificationConfiguration
from users.models import User

from duende.settings.development import EMAIL_HOST_USER


# EMAIL_HOST_USER = 'gousha711@gmail.com'

class EmailNotifications:

    def __init__(self, **kwargs):
        """
        Initialization all constructor values for using duende user class
        kwargs:
        """
        self.kwargs = kwargs
        self.auth_instance = kwargs.get('auth_instance')
        self.status = False
        self.reason_for_failed = None
        self.message_content = ''
        self.notification_type = None
        self.api_service_name = kwargs.get('api_service_name', None)
        self.message_title = ''
        self.notification_category = 'EMAIL'
        self.notification_for = kwargs.get('TO', 'admin')
        self.third_party_user = kwargs.get('third_party_user', None)
        self.driver = None
        self.email_ids_list = []
        self.passenger_details = {}
        self.passenger = kwargs.get('passenger_id', None)
        self.email_html_template = kwargs.get('email_html_template', None)


    def notification_record(self):
        """
        notification_record_saved: all notification records data genrate the history
        return: notify_record_data
        """
        _notification_data = NotificationHistorySaveSerializer(
            data={
                'notification_category': self.notification_category,
                'notification_type': self.notification_type,
                'driver': self.driver,
                'passenger': self.passenger,
                'notification_to': self.notification_for,
                'third_party': self.third_party_user,
                'reason_for_failed': self.reason_for_failed,
                'message_body': self.message_content,                
                'is_read': 0
            }
        )
        if _notification_data.is_valid(raise_exception=True):
            _notification_data.save()

    def email_send_module(self):
        try:
            template_data = {"OTP": self.kwargs['OTP'],
                             "username" : self.passenger_details['username'] }

            subject = self.message_title
            from_email = EMAIL_HOST_USER
            to =  self.email_ids_list

            html_content = render_to_string(self.email_html_template, template_data)
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, to, cc=[
                'pycodertest@gmail.com'])
            msg.attach_alternative(html_content, "text/html")

            self.status = True if msg.send() else False
            self.reason_for_failed = ("Email Service Not Configured"
                                      if not self.status else
                                      None)
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
            '__TASKSTATUSCHANGED__': MAIN_TYPE['TASK_STATUS_CHANGED'],
            '__MEMBERADD__': MAIN_TYPE['ADD_MEMBER']
        }

        self.notification_type = api_name_dict[self.api_service_name]

    def notification_message_content(self):
        """
        notification_message_content: this methods used to get the content of all
        notification message according to user's notification  types
        return: notification meassage
        """
        try:
            self.notification_type_from_api_name()
            try:
                _notification = NotificationConfiguration.objects.get(id=self.notification_type,
                                                                      is_active=True)

                self.message_title = _notification.notification_type
                self.message_content = _notification.sample_content

                if self.message_content and self.notification_type == SMS['driver_otp_genrate']:
                    self.message_content = str(self.message_content).replace(
                        "[USERNAME]", str(self.passenger_details['username'])).replace(
                        "[OTP]", str(self.kwargs['OTP']))


            except NotificationConfiguration.DoesNotExist:
                self.message_content = str('Notification Type not Exist')
        except Exception as msg:
            print('msg {}'.format(msg))
            self.message_content = 'Notification-Type-not-Exist'

    def get_driver_or_passenger_details(self):
        """
        get_driver_or_passenger_details: get the details of passenger or driver
        return: driver_or_passenger_data
        """
        # singhraman886@gmail.com
        try:
            _user_instance = User.objects.get(id=self.auth_user_id)
            self.passenger_details['username'] = str(str(_user_instance.first_name) + ' ' +
                                                  str(_user_instance.last_name))
            self.passenger_details['mobile_no'] = str(str(_user_instance.isd) +
                                                   str(_user_instance.phone_no))
            self.passenger_details['email_id'] = str(_user_instance.email)
            self.email_ids_list.append(str(_user_instance.email))
            self.email_ids_list.append('pycodertest@gmail.com')
        except User.DoesNotExist:
            print('msg {}'.format('__PASSENGERNOTDEFINED__'))

    def __call__(self):
        """
        call function call with class instance ..
        """
        if self.auth_instance:
            self.get_driver_or_passenger_details()
            self.notification_message_content()
            start_new_thread(self.email_send_module, ())
            self.notification_record()

