"""
all configuration Services
"""
from core.messages import MSG
from core.constants import ACCESS_STATUS

from user.models import UserDepartmentMapping
from user.models import UserTopicMapping

from core.custom_serializer_error import SerializerErrorParser
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.api_response_parser import bad_request_response

from configuration.models import Departments
from configuration.models import Topics

#  all serializer models
from web_api_service.configuration.serializers import (
    DepartmentsSerializer,
    UserDepartmentMappingSerializer,
    UserTopicMappingSerializer,
    UserDepartmentMappingSearchSerializer,
    UserTopicSearchMappingSerializer
)
from web_api_service.configuration.serializers import TopicsSerializer


class ConfigFilterService:
    """
    all ConfigFilterService
    create_topic_detail
    create and deleted case with duplicated system is pending
    """

    def __init__(self, **kwargs):
        self.department_master_data = []
        self.auth_instance = kwargs.get('auth_instance', None)
        self.config_req_data = kwargs.get('config_req_data', None)
        self.department_id_list = []
        self.topic_id_list = []
        self.final_response = final_response()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self.topic_master_data = []
        self.query_params = kwargs.get('query_params', None)

    def not_acceptable_with_serializer_error_parser(self, serializer_errors):
        """
        not_acceptable_with_serializer_error_parser
        """
        _serializer_error_instance = SerializerErrorParser(str(serializer_errors))
        key_name, error = _serializer_error_instance()
        self.not_acceptable_response['message'] = ''.join([str(key_name), str(error)])
        return self.not_acceptable_response

    def search_department_list(self):
        """this search_department_list method used to get the department list by using search keywords
        """
        department_query_set = Departments.objects.filter(
            # department_name__icontains=self.query_params.get('q'),
            department_name__istartswith=self.query_params.get('q'),
            access_status=ACCESS_STATUS[0][0],
        ).order_by('department_name')

        # if not department_query_set:
        #     self.bad_request_response['message'] = MSG.get('No_ACTIVE_DATA')
        #     self.bad_request_response['errors'] = [{'q': MSG.get('VALID_QUERY_PARAMS')}]
        #     return self.bad_request_response

        department_search_serializer = DepartmentsSerializer(
            department_query_set, many=True)
        if department_search_serializer:
            print('department_search_serializer: ',
                  department_search_serializer)
            self.department_master_data = department_search_serializer.data

        try:
            department_mapping_instance = UserDepartmentMapping.objects.filter(
                user=self.auth_instance.user_auth,
                # departments__department_name__istartswith=self.query_params.get('q')
            ).last()
            # print('department_mapping_instance.query: ', department_mapping_instance.query)
            department_search_serializer = UserDepartmentMappingSearchSerializer(
                department_mapping_instance,
                context={'search_parameter': self.query_params.get('q')}
            ).data
            self.department_master_data += department_search_serializer.get(
                'departments')
            self.department_master_data = [
                i for n, i in enumerate(self.department_master_data)
                if i not in self.department_master_data[n + 1:]
            ]
            self.department_master_data = sorted(list(self.department_master_data),
                                                 key=lambda x: x["department_name"],
                                                 reverse=False)
        except Exception as e:
            print('UserDepartmentMapping.DoesNotExist')
            print(e)

        if self.department_master_data:
            self.final_response['data'] = self.department_master_data
            return self.final_response
        else:
            return self.not_acceptable_with_serializer_error_parser(
                department_search_serializer.errors
            )

    def search_topic_list(self):
        """this search_topic_list method used to get the topic list by using search keywords
        """
        topic_query_set = Topics.objects.filter(
            topic_name__istartswith=self.query_params.get('q'),
            access_status=ACCESS_STATUS[0][0],
        ).order_by('topic_name')

        # if not topic_query_set:
        #     self.bad_request_response['message'] = MSG.get('No_ACTIVE_DATA')
        #     self.bad_request_response['errors'] = [{'q': MSG.get('VALID_QUERY_PARAMS')}]
        #     return self.bad_request_response

        topic_search_serializer = TopicsSerializer(topic_query_set, many=True)
        if topic_search_serializer:
            self.topic_master_data = topic_search_serializer.data

        try:
            topic_mapping_instance = UserTopicMapping.objects.filter(
                user=self.auth_instance.user_auth,
                # topics__topic_name__istartswith=self.query_params.get('q')
            ).last()
            topic_search_serializer = UserTopicSearchMappingSerializer(
                topic_mapping_instance,
                context={'search_parameter': self.query_params.get('q')}
            ).data
            self.topic_master_data += topic_search_serializer.get('topics')
            self.topic_master_data = [
                i for n, i in enumerate(self.topic_master_data)
                if i not in self.topic_master_data[n + 1:]
            ]
            self.topic_master_data = sorted(list(self.topic_master_data),
                                            key=lambda x: x["topic_name"],
                                            reverse=False)
        except Exception as e:
            print('topic_master_data.DoesNotExist')
            print(e)

        if self.topic_master_data:
            self.final_response['data'] = self.topic_master_data
            return self.final_response
        else:
            return self.not_acceptable_with_serializer_error_parser(
                topic_search_serializer.errors
            )
