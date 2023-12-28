from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG
from web_api_service.helpers.all_config_func import get_user_instance
from web_api_service.notification.notification_service import NotificationService


# import service


class NotificationCountApi(APIView):
    """
    NotificationCountApi
    usage: this endpoint used to get the notification count.
    endpoint: /api/v1/notification/count/
    response: {
        "data": 0,
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """this method get the notification count
        endpoint: /api/v1/notification/count/
        response: {
            "data": 0,
            "success": true,
            "message": "Done"
        }
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': request.user})
        if not user_instance:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST)

        user_instance = get_user_instance({'auth_user': request.user})        
        if not user_instance:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST)

        if user_instance.role.role == 'DUMMY':
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST)

        try:
            notification_count_response = NotificationService(
                auth_instance=request.user
            ).notification_count()
            return APIResponseParser.response(**notification_count_response) 
        except Exception as e:
            notification_count_response = None
            print('NotificationServiceExceptionErr')
            print(e)
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST)


class NotificationRecordApi(APIView):
    """
    NotificationRecordApi
    usage: this endpoint is used to get the all notification history
    endpoint: /api/v1/notification/record/
    response: {
        "data": [
            {
                "id": "892a7fe8-ce62-4c7d-a3c3-3e84d00cb8f8",
                "notification_type": "Task Assign",
                "notification_category": "PUSH",
                "notification_to": "admin",
                "reason_for_failed": "",
                "message_body": "Hi, hhhhhggggggg, you added on task by sonal",
                "is_read": true,
                "notify_at": "2022-11-29T09:43:43.195780Z",
                "user": "a8c1c071-153c-459b-97a0-e6a5e702b3a7"
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        this get method used to update the api service
        """
        user_instance = get_user_instance(
            {'is_active': True, 'auth_user': request.user})
        if not user_instance:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST)

        try:
            notification_record_response = NotificationService(
                auth_instance=request.user
            ).notification_record()
            return APIResponseParser.response(**notification_record_response)
        except Exception as e:
            notification_record_response = None
            print('NotificationServiceExceptionErr')
            print(e)
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST)
