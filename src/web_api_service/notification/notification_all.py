from _thread import start_new_thread

from user.models import CustomUsers
from web_api_service.notification.push_notification import PushNotifications


def notification_members_topics_updater(api_service_name, topic_name):
    """this notification_members_topics_updater method is used to update the topic
    moment delete and added the task
    """
    custom_user_obj = CustomUsers.objects.filter()
    for custom_user in custom_user_obj:
        push_notification_instance = PushNotifications(
            api_service_name=api_service_name,
            TO='admin',
            user=custom_user.id,
            user_notification_data={
                'username': ''.join([str(custom_user.first_name), ' ', str(custom_user.last_name)]),
                'topic_name': str(topic_name),
            },
        )
        push_notification = push_notification_instance()
        if push_notification:
            print('SUCCESS')
        else:
            print('FAILED')


def notification_to_all_members(**kwargs):
    """notification_to_all_members all parameters
    all notification call for topic caller section
    """
    if (kwargs.get('api_service_name') == '__TOPICADDEDD__' 
            or kwargs.get('api_service_name') == '__TOPICDELETED__'):
        # notification_members_topics_updater(kwargs.get('api_service_name'),
        #                                     kwargs.get('topic_name'))
        start_new_thread(
            notification_members_topics_updater, (kwargs.get('api_service_name'),
                                                  kwargs.get('topic_name')))
