from core.api_response_parser import bad_request_response
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.messages import MSG
from user.models import CustomUsers
from web_api_service.configuration.all_config_service import \
    ReadConfigurationMaster
from web_api_service.helpers.all_config_func import get_user_instance, get_language_uuid


class LanguageManageService:
    """this LanguageManageService class is used to manage the language management service
    """

    def __init__(self, **kwargs):
        self.auth_instance = kwargs.get('auth_instance', None)
        self.config_req_data = kwargs.get('config_req_data', None)
        self.final_response = final_response()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()

    def get_language_list(self):
        """get_language_list this mehod used to get the langugae details from list
        """
        try:
            self.final_response['data'] = ReadConfigurationMaster.get_language_data()
            return self.final_response
        except Exception as e:
            print(e)
            self.bad_request_response['message'] = str(e)
            return self.bad_request_response

    def change_user_language(self):
        """change the user language
        """
        if self.auth_instance is None:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        print('dffffffffffff', self.auth_instance.user_auth)

        user_instance = get_user_instance(
            {
                'is_active': True,
                'auth_user': self.auth_instance
            }
        )

        print('userinstance', user_instance)
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        print('fdfff', self.config_req_data)

        try:
            CustomUsers.objects.filter(
                id=user_instance.id,
            ).update(language_id=get_language_uuid(self.config_req_data['language']))
        except Exception as e:
            print(e)
            self.bad_request_response['message'] = str(e)
            return self.bad_request_response

        self.final_response['data'] = {'language_changed': True}
        return self.final_response
