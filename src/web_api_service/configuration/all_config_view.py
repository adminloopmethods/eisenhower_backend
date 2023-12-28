"""
all configuration apis
"""

# import rest apps
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

# all helper apps
from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG, MSG

from web_api_service.configuration.all_config_service import \
    ReadConfigurationMaster
from web_api_service.helpers.all_config_func import get_user_instance


class LanguageMasterApi(LoggingMixin, APIView):
    """language master api
    """

    def get(self, request):
        """get all language master data"""
        language_data = ReadConfigurationMaster.get_language_data()
        if not language_data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA']
            )
        return APIResponseParser.response(success=True,
                                          message=API_RESPONSE_MSG['DONE'],
                                          keyname='data',
                                          data=language_data)


class TopicsMasterApi(LoggingMixin, APIView):
    """topic master api
    """

    def get(self, request):
        """get all topics master data"""
        topics_data = ReadConfigurationMaster.get_topics_data()
        if not topics_data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA']
            )
        return APIResponseParser.response(keyname='data',
                                          data=topics_data,
                                          success=True,
                                          message=API_RESPONSE_MSG['DONE'])


class DepartmentMasterApi(LoggingMixin, APIView):
    """DepartmentMasterApi
    """

    def get(self, request):
        """get all DepartmentMasterApi master data"""
        department_data = ReadConfigurationMaster.get_departments_data()
        if not department_data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA']
            )
        return APIResponseParser.response(keyname='data',
                                          data=department_data,
                                          success=True,
                                          message=API_RESPONSE_MSG['DONE'])


class StatusMasterApi(LoggingMixin, APIView):
    """StatusMasterApi
    """

    def get(self, request):
        """get all Status Master data"""
        try:
            user_instance = get_user_instance(
                {'is_active': True, 'auth_user': request.user})
            if not user_instance:
                return APIResponseParser.response(
                    success=False,
                    message=MSG.get('USER_NOT_FOUND'))

            if user_instance.language.language_code == 'ITL':
                status_master_data = ReadConfigurationMaster.get_task_status_data_in_italian()
            if user_instance.language.language_code == 'ENG':
                status_master_data = ReadConfigurationMaster.get_task_status_data()

            if not status_master_data:
                return APIResponseParser.response(
                    success=False,
                    message=API_RESPONSE_MSG['No_ACTIVE_DATA']
                )
            return APIResponseParser.response(keyname='data',
                                              data=status_master_data,
                                              success=True,
                                              message=API_RESPONSE_MSG['DONE'])
        except Exception as e:
            print(e)
            return APIResponseParser.response(success=False,
                                              message=str(e))


class CurrencyMasterApi(LoggingMixin, APIView):
    """CurrencyMasterApi
    """

    def get(self, request):
        """get all currency Master data"""
        currency_master_data = ReadConfigurationMaster.get_currency_master_data()
        if not currency_master_data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA']
            )
        return APIResponseParser.response(keyname='data',
                                          data=currency_master_data,
                                          success=True,
                                          message=API_RESPONSE_MSG['DONE'])


class ColorMasterApi(LoggingMixin, APIView):
    """ColorMasterApi
    path: /api/v1/config/colors/
    methods: GET
    Response: {
    "data": [
            {
                "id": "5f7d4ed5-bd90-4c4f-b581-3e1dfd282689",
                "created_at": "2022-08-18T10:03:58.012582Z",
                "updated_at": "2022-08-18T10:03:58.012616Z",
                "is_active": true,
                "color_name": "Red",
                "color_code": "RRR",
                "hex_symbol": "46jdasd",
                "description": "color code",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "e026aa15-ec41-4b0c-aaac-e574b0856ed5",
                "created_at": "2022-08-19T07:17:29.405302Z",
                "updated_at": "2022-08-19T07:17:29.405362Z",
                "is_active": true,
                "color_name": "Green",
                "color_code": "GRN",
                "hex_symbol": "#00FF00",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "892c0efc-9e02-4bec-b617-1d9fa2480499",
                "created_at": "2022-08-19T07:18:18.929225Z",
                "updated_at": "2022-08-19T07:18:18.929259Z",
                "is_active": true,
                "color_name": "Blue",
                "color_code": "blu",
                "hex_symbol": "#0000FF",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "58731589-fcc4-4af5-a734-f776374d66a2",
                "created_at": "2022-08-19T07:19:41.964408Z",
                "updated_at": "2022-08-19T07:19:41.964438Z",
                "is_active": true,
                "color_name": "Light Blue",
                "color_code": "LB",
                "hex_symbol": "#ADD8E6",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "996bfc3d-a329-42a5-9b09-72629716ce43",
                "created_at": "2022-08-19T07:20:38.034786Z",
                "updated_at": "2022-08-19T07:20:38.034822Z",
                "is_active": true,
                "color_name": "Light Red",
                "color_code": "LR",
                "hex_symbol": "#FFCCCB",
                "description": "",
                "created_by": 1,
                "updated_by": null
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    def get(self, request):
        """get all color Master  data"""
        color_master_data = ReadConfigurationMaster.get_color_master_data()
        if not color_master_data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA']
            )
        return APIResponseParser.response(keyname='data',
                                          data=color_master_data,
                                          success=True,
                                          message=API_RESPONSE_MSG['DONE'])


class UserRoleMasterApi(LoggingMixin, APIView):
    """UserRoleMasterApi
    path: /api/v1/config/userRoles/
    method: GET
    Response: {
        "data": [
            {
                "id": "bf9fa3fb-7bb4-4a13-8371-e8494952433f",
                "created_at": "2022-08-18T10:28:13.960769Z",
                "updated_at": "2022-08-18T10:28:13.960818Z",
                "is_active": true,
                "role_name": "Manager",
                "description": "",
                "role": "MANAGER",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "created_at": "2022-08-25T12:05:14.881192Z",
                "updated_at": "2022-08-25T12:05:14.881223Z",
                "is_active": true,
                "role_name": "Member",
                "description": "",
                "role": "MEMBER",
                "created_by": 1,
                "updated_by": null
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    def get(self, request):
        """get all user role Master master data"""
        try:
            user_instance = get_user_instance(
                {'is_active': True, 'auth_user': request.user})
            if not user_instance:
                return APIResponseParser.response(
                    success=False,
                    message=MSG.get('USER_NOT_FOUND'))

            if user_instance.language.language_code == 'ITL':
                user_role_master_data = ReadConfigurationMaster.get_user_role_master_data_in_italian()
            if user_instance.language.language_code == 'ENG':
                user_role_master_data = ReadConfigurationMaster.get_user_role_master_data()
            if not user_role_master_data:
                return APIResponseParser.response(
                    success=False,
                    message=API_RESPONSE_MSG['No_ACTIVE_DATA']
                )
            return APIResponseParser.response(keyname='data',
                                              data=user_role_master_data,
                                              success=True,
                                              message=API_RESPONSE_MSG['DONE'])
        except Exception as e:
            print(e)
            return APIResponseParser.response(success=False,
                                              message=str(e))


class CountryMasterApi(LoggingMixin, APIView):
    """CountryMasterApi
    path: /api/v1/config/countries/
    method: GET
    Response: {
        "data": [
            {
                "id": "1d84a5d8-8e17-45e3-b595-35d59939dab5",
                "created_at": "2022-09-07T05:29:49.465665Z",
                "updated_at": "2022-09-07T05:29:49.465727Z",
                "is_active": true,
                "country": "India",
                "isd": 91,
                "mobile_no_digits": 10,
                "code": null,
                "timezone": "asia/kolkata",
                "created_by": 1,
                "updated_by": null,
                "currency": null
            },
            {
                "id": "37368230-3d99-4074-bfda-fa3114d1b115",
                "created_at": "2022-09-07T05:31:20.738401Z",
                "updated_at": "2022-09-07T05:31:20.738432Z",
                "is_active": true,
                "country": "Itly",
                "isd": 39,
                "mobile_no_digits": 7,
                "code": null,
                "timezone": "asia/kolkata",
                "created_by": 1,
                "updated_by": null,
                "currency": null
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    def get(self, request):
        """get all user role Master master data"""
        country_master_data = ReadConfigurationMaster.get_country_master_date()
        if not country_master_data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA']
            )
        return APIResponseParser.response(keyname='data',
                                          data=country_master_data,
                                          success=True,
                                          message=API_RESPONSE_MSG['DONE'])
