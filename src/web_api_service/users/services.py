"""
all configuration Services
"""

# from django.contrib.auth.models import User
from account.models import User


from rest_framework import status

from core.api_response_parser import not_acceptable_response
from core.messages import MSG, ITALIAN_MSG
from core.serializer_getter import SerializerManipulationService
from core.third_party_consume_service import TPAPIService
from user.models import CustomUsers
# import cognito services
from web_api_service.cognito.aws_cognito_auth import AWSCognito
from web_api_service.helpers.all_config_func import already_exist_check
from web_api_service.helpers.all_config_func import get_language_uuid
# all helper functions
from web_api_service.helpers.all_config_func import get_user_instance
#  all serializer models
from web_api_service.users.serializers import CustomUsersSerializer
from web_api_service.users.serializers import UpdateUsersSerializer

from cognitojwt import jwt_sync


EXLUDE_USER_LIST = [
    434, 405, 406, 407, 408, 425, 409, 410, 412, 426, 413, 414, 433, 427,
    416, 313, 435, 417, 442, 411, 418, 415, 432, 312, 428, 429, 419, 430,
    420, 431, 421, 422, 196, 422, 424, 423
]


def test_queryset():
    """for create delete query
    """
    User.objects.exclude(id__in=EXLUDE_USER_LIST).filter()


class UserService:
    """this UserService class service used to manage all user related data
    methods:
    """

    @staticmethod
    def get_user_details(auth_user_instance):
        """get all get_user_details master data

        arg: auth_user_instance: auth user login user instance

        return: {}: success response with dict or json format.
        """
        serializer_obj = SerializerManipulationService(model_class=CustomUsers,
                                                       serializer_class=CustomUsersSerializer,
                                                       type='__single__',
                                                       query_params_var={
                                                           'is_active': True,
                                                           'auth_user': auth_user_instance
                                                       }, )
        serializer_data = serializer_obj()
        result_dict = {
            'success': True,
            'message': MSG['DONE'],
            'keyname': 'user_details',
            'data': serializer_data,
            'status_code': status.HTTP_200_OK
        }
        return result_dict if serializer_data else not_acceptable_response()

    @staticmethod
    def create_auth_user(user_request_data):
        """create auth the user details data with profile pictures

        args: user_request_data: request input data for create auth user

        return: obj: auth_user_instance
        """
        try:
            return User.objects.create_user(**user_request_data)
        except Exception as e:
            print('User.Create.Exception')
            print(e)
            return None

    @staticmethod
    def delete_auth_user(auth_user_id):
        """delete_auth_user user details data with profile pictures

        args: auth_user_id: auth user uuid and id primary key

        return: True/False: deleteBooleanInstance
        """
        return User.objects.filter(id=auth_user_id).delete()

    @staticmethod
    def update_user_language(user_instance, language_uuid):
        """in this update_user_language method update user lanaguage id

        args: user_instance: user instance to get the user identify
                language_uuid: to update the language primary key

        return: None
        """
        try:
            CustomUsers.objects.filter(
                id=user_instance.id,
            ).update(language_id=language_uuid)
        except Exception as e:
            print(e)

    @staticmethod
    def cognito_access_token_update_to_user(user_instance,
                                            cognito_access_token,
                                            cognito_id_token):
        """in this cognito_access_token_update_to_user method 
        will update the cognito access token and id token with help 
        of user_instance object

        args: 
            user_instance: user instance to get the user identify
            cognito_access_token: from cognio login service
            cognito_id_token: from cognio login service

        return: None
        """
        if CustomUsers.objects.filter(
                id=user_instance.id
        ).update(cognito_access_token=cognito_access_token,
                 cognito_id_token=cognito_id_token):
            return True
        else:
            return False

    # @staticmethod
    def login(self, req_data):
        """in this login method we used to login with JWT Token and 
        manage all alogin api protectable with JWT token
        this method cover and manage both JWT and cognito token,
         cognito token used for call the all cognito and third party service 
         which provide by abby or etc client site

        args: req_data: {"email":"govind@gmail.com", "password": "Admin@123"}
        request data for login a valid user to use email and password keys

        return: {}: success and failer response according to the 
        user request and exception
        """
        user_instance = get_user_instance(
            {'email': req_data.get('email').lower()})
        if not user_instance:
            try:
                if req_data.get('language', None) == 'ENG':
                    does_not_message = MSG['USER_DOEST_NOT_EXIST']
                else:
                    does_not_message = ITALIAN_MSG['USER_DOEST_NOT_EXIST']
            except Exception as e:
                does_not_message = MSG['USER_DOEST_NOT_EXIST']
                print(e)
            return {
                'success': False,
                'message': does_not_message,
                'status_code': status.HTTP_400_BAD_REQUEST
            }

        print("====user_instance.application_type====",
              user_instance.application_type)
        # try:
        #     if user_instance.application_type == 'EISEN':
        #         application_type = 'emm'
        #     if user_instance.application_type == 'BCR':
        #         application_type = 'bcr'
        #     if user_instance.application_type == 'BEM':
        #         application_type = 'bem'
        # except Exception as e:
        #     print('eor')
        #     print(e)

        # if application_type != req_data.get('app_type').lower():
        #     try:
        #         if req_data.get('language', None) == 'ENG':
        #             does_not_message = MSG['USER_DOEST_NOT_EXIST']
        #         else:
        #             does_not_message = ITALIAN_MSG['USER_DOEST_NOT_EXIST']
        #     except Exception as e:
        #         does_not_message = MSG['USER_DOEST_NOT_EXIST']
        #         print(e)
        #     return {
        #         'success': False,
        #         'message': does_not_message,
        #         'status_code': status.HTTP_400_BAD_REQUEST
        #     }

        try:
            if user_instance.is_active is False:

                try:
                    if req_data.get('language', None) == 'ENG':
                        active_message = MSG['USER_ACTIVE_ERROR']
                    else:
                        active_message = ITALIAN_MSG['USER_ACTIVE_ERROR']
                except Exception as e:
                    active_message = MSG['USER_ACTIVE_ERROR']
                    print(e)
                return {
                    'success': False,
                    'message': active_message,
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
        except Exception as e:
            print('**user_instance.is_active.exception')
            print(e)

        try:
            if str(user_instance.role.role) == 'DUMMY':
                try:
                    if req_data.get('language', None) == 'ENG':
                        dummy_user_message = MSG['DUMMY_USER_NOT_FOUND']
                    else:
                        dummy_user_message = ITALIAN_MSG['DUMMY_USER_NOT_FOUND']
                except Exception as e:
                    dummy_user_message = MSG['DUMMY_USER_NOT_FOUND']
                    print(e)
                return {
                    'success': False,
                    'message': dummy_user_message,
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
        except Exception as e:
            print('#roleException')
            print(e)

        # try:
        #     if user_instance.is_cognito_user is False:
        #         try:
        #             if req_data.get('language', None) == 'ENG':
        #                 cognito_message = MSG['USER_DOEST_NOT_EXIST']
        #             else:
        #                 cognito_message = ITALIAN_MSG['USER_DOEST_NOT_EXIST']
        #         except Exception as e:
        #             cognito_message = MSG['USER_DOEST_NOT_EXIST']
        #             print(e)

        #         return {
        #             'success': False,
        #             'message': cognito_message,
        #             'status_code': status.HTTP_400_BAD_REQUEST
        #         }
        # except Exception as e:
        #     print('#roleException')
        #     print(e)

        # third party api consume services
        """ third_party_request_params = dict(
            api_url_path='/api/token/',
            api_method='__POST__',
            headers={'Content-Type': 'application/json'},
            api_post_data={
                'username': user_instance.auth_user.username,
                'password': req_data.get('password', 'Admin@123')
            }
        )
        third_party_api_instance = TPAPIService(**third_party_request_params)
        jwt_tokens = third_party_api_instance() """

        try:
            if req_data.get('language', None) == 'ENG':
                login_error_message = MSG['INCORRECT_USERNAME_PASSWORD']
            else:
                login_error_message = ITALIAN_MSG['INCORRECT_USERNAME_PASSWORD']
        except Exception as e:
            login_error_message = MSG['INCORRECT_USERNAME_PASSWORD']
            print(e)

        try:
            language_uuid = get_language_uuid(req_data.get('language', None))
        except Exception as e:
            language_uuid = None
            print(e)

        self.update_user_language(user_instance,
                                  language_uuid)

        token_data = {}

        try:
            cognito_response_data = AWSCognito(
                username=req_data.get('email').lower()
            ).authenticate_and_get_token(req_data.get('password'))

            print('cognito_response_data-----', cognito_response_data)
            print('-------------------------------------------------------------')
            token_data["id"] = cognito_response_data['AuthenticationResult']['AccessToken']
            token_data["access"] = cognito_response_data['AuthenticationResult']['IdToken']
            self.cognito_access_token_update_to_user(
                user_instance,
                cognito_response_data['AuthenticationResult']['AccessToken'],
                cognito_response_data['AuthenticationResult']['IdToken'])
        except Exception as e:
            print('AWSCognitoErr')
            print(e)

        try:
            if req_data.get('app_type').lower() == 'eisen':
                application_type = 'EMM'
            if req_data.get('app_type').lower() == 'bcr':
                application_type = 'BCR'
            if req_data.get('app_type').lower() == 'bem':
                application_type = 'BEM'
        except Exception as e:
            print('eor')
            print(e)

        try:
            cognito_group_data = AWSCognito(
                username=req_data.get('email').lower()
            ).list_groups_for_user()
            print('-------------------cognito_group_data-----------------------')
            print(cognito_group_data['Groups'])
            group_data = []
            for group in cognito_group_data['Groups']:
                group_data.append(group['GroupName'])

            print("group_data")
            print(group_data)
            if application_type not in group_data:
                try:
                    if req_data.get('language', None) == 'ENG':
                        does_not_message = MSG['USER_DOEST_NOT_EXIST']
                    else:
                        does_not_message = ITALIAN_MSG['USER_DOEST_NOT_EXIST']
                except Exception as e:
                    does_not_message = MSG['USER_DOEST_NOT_EXIST']
                    print(e)
                return {
                    'success': False,
                    'message': does_not_message,
                    'status_code': status.HTTP_400_BAD_REQUEST
                }
        except Exception as error:
            print(error)
            return {
                'success': False,
                'message': MSG['USER_DOEST_NOT_EXIST'],
                'status_code': status.HTTP_400_BAD_REQUEST
            }

        # try:
        #     application_type = str(user_instance.application_type)
        # except Exception as e:
        #     print('ApplicationTypeErr')
        #     print(e)
        #     application_type = 'BCR'
        print(token_data)
        return {
            'success': True,
            'message': MSG['DONE'],
            'keyname': 'user_tokens',
            'status_code': status.HTTP_200_OK,
            'data': {
                'tokens': token_data,
                'role': str(user_instance.role.role),
                'app_type': application_type,
                'user': str(user_instance.id)
            }} if cognito_response_data['AuthenticationResult'] else {'success': False,
                                                                      'message': login_error_message,
                                                                      'status_code': status.HTTP_406_NOT_ACCEPTABLE
                                                                      }

    @staticmethod
    def update_user_details(auth_user_instance, user_request_data):
        """update the user details data with profile pictures

        args: auth_user_instance : auth user instances 
              user_request_data : user_request_data

        return: update_user_response
        """
        user_instance = get_user_instance(
            {'is_active': True, 'auth_user': auth_user_instance})
        if not user_instance:
            return {
                'success': False,
                'message': MSG['USER_NOT_FOUND'],
                'status_code': status.HTTP_400_BAD_REQUEST
            }

        # check email already exists.
        if already_exist_check({'email': user_request_data.get('email')}):
            return {
                'success': False,
                'message': MSG['EMAIL_ALREADY_EXISTS'],
                'status_code': status.HTTP_400_BAD_REQUEST
            }

        print('user_request_data', user_request_data)
        serializer_instance = SerializerManipulationService(
            model_instance=user_instance,
            serializer_class=UpdateUsersSerializer,
            request_data=user_request_data,
            type='__update__')
        serializer_data = serializer_instance()
        return {
            'success': True,
            'message': MSG['DONE'],
            'keyname': 'user_details',
            'data': serializer_data,
            'status_code': status.HTTP_200_OK} if serializer_data else not_acceptable_response()
