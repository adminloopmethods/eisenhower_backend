"""
all configuration Services
"""
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from core.constants import ACCESS_STATUS

from core.messages import MSG

from core.serializer_getter import SerializerManipulationService

from configuration.models import Language
from configuration.models import TaskStatusMaster
from configuration.models import CurrencyMaster
from configuration.models import ColorMaster
from configuration.models import UserRoleMaster
from configuration.models import Departments
from configuration.models import Topics

# import location
from location.models import CountryMaster

#  all serializer models
from web_api_service.configuration.serializers import LanguageSerializer, \
    TaskStatusMasterItalianSerializer, UserRoleMasterItalianSerializer
from web_api_service.configuration.serializers import TaskStatusMasterSerializer
from web_api_service.configuration.serializers import CurrencyMasterSerializer
from web_api_service.configuration.serializers import ColorMasterSerializer
from web_api_service.configuration.serializers import UserRoleMasterSerializer
from web_api_service.configuration.serializers import DepartmentsSerializer
from web_api_service.configuration.serializers import TopicsSerializer

# location serializer
from web_api_service.configuration.serializers import CountryMasterSerializer


class ReadConfigurationMaster:
    """this AllConfigurationMaster class service used to manage 
    all configuration master data
    methods:
        get_topics_data
        get_departments_data
        get_language_data
        get_task_status_data
        get_currency_master_data
        get_color_master_data
        get_user_role_master_data
        all methods are @staticmethod
    """

    @staticmethod
    def get_topics_data():
        """get all topics master data"""
        query_params_var = {
            'is_active': True,
            'access_status': ACCESS_STATUS[0][0]
        }
        serializer_instance = SerializerManipulationService(model_class=Topics,
                                                            serializer_class=TopicsSerializer,
                                                            query_params_var=query_params_var,
                                                            type='__multiple__')
        return serializer_instance()

    @staticmethod
    def get_departments_data():
        """get all departments master data"""
        query_params_var = {
            'is_active': True,
            'access_status': ACCESS_STATUS[0][0]
        }
        serializer_instance = SerializerManipulationService(model_class=Departments,
                                                            serializer_class=DepartmentsSerializer,
                                                            query_params_var=query_params_var,
                                                            type='__multiple__')
        return serializer_instance()

    @staticmethod
    def get_language_data():
        """get all language master data"""
        serializer_instance = SerializerManipulationService(model_class=Language,
                                                            serializer_class=LanguageSerializer,
                                                            query_params_var={'is_active': True},
                                                            type='__multiple__')
        return serializer_instance()

    @staticmethod
    def get_task_status_data():
        """get all task status master data"""
        serializer_instance = SerializerManipulationService(model_class=TaskStatusMaster,
                                                            serializer_class=TaskStatusMasterSerializer,
                                                            query_params_var={'is_active': True},
                                                            type='__multiple__')
        return serializer_instance()


    @staticmethod
    def get_task_status_data_in_italian():
        """get all task status master data"""
        serializer_instance = SerializerManipulationService(model_class=TaskStatusMaster,
                                                            serializer_class=TaskStatusMasterItalianSerializer,
                                                            query_params_var={'is_active': True},
                                                            type='__multiple__')
        return serializer_instance()

    @staticmethod
    def get_currency_master_data():
        """get all currency master data"""
        serializer_instance = SerializerManipulationService(model_class=CurrencyMaster,
                                                            serializer_class=CurrencyMasterSerializer,
                                                            query_params_var={'is_active': True},
                                                            type='__multiple__')
        return serializer_instance()

    @staticmethod
    def get_color_master_data():
        """get all color master data"""
        serializer_instance = SerializerManipulationService(model_class=ColorMaster,
                                                            serializer_class=ColorMasterSerializer,
                                                            query_params_var={'is_active': True},
                                                            type='__multiple__')
        return serializer_instance()

    @staticmethod
    def get_user_role_master_data():
        """get all user role master master data"""
        serializer_instance = SerializerManipulationService(model_class=UserRoleMaster,
                                                            serializer_class=UserRoleMasterSerializer,
                                                            query_params_var={'is_active': True},
                                                            type='__multiple__')
        return serializer_instance()


    @staticmethod
    def get_user_role_master_data_in_italian():
        """get all user role master master data"""
        serializer_instance = SerializerManipulationService(model_class=UserRoleMaster,
                                                            serializer_class=UserRoleMasterItalianSerializer,
                                                            query_params_var={'is_active': True},
                                                            type='__multiple__')
        return serializer_instance()


    @staticmethod
    def get_country_master_date():
        """get all user get_country_master_date data"""
        serializer_instance = SerializerManipulationService(model_class=CountryMaster,
                                                            serializer_class=CountryMasterSerializer,
                                                            query_params_var={'is_active': True},
                                                            type='__multiple__')
        return serializer_instance()
