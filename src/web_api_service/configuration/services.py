"""
all configuration Services
"""
from rest_framework import status

from configuration.models import Departments
from configuration.models import Topics
from core.api_response_parser import bad_request_response
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.constants import ACCESS_STATUS
from core.messages import MSG, ITALIAN_MSG
from core.serializer_getter import SerializerManipulationService
# import user mapping
from user.models import UserDepartmentMapping
from user.models import UserTopicMapping
# from web_api_service.configuration.delete_auth_user_task import collect_auth_user_id_list
from web_api_service.configuration.delete_auth_user_task import delete_auth_user_from_department_id
#  all serializer models
from web_api_service.configuration.serializers import DepartmentsSerializer
from web_api_service.configuration.serializers import TopicsSerializer
# import user mapping serializer
from web_api_service.configuration.serializers import UserDepartmentMappingSerializer
from web_api_service.configuration.serializers import UserTopicMappingSerializer
from web_api_service.helpers.all_config_func import already_exist_check_for_department
from web_api_service.helpers.all_config_func import already_exist_check_for_topic
from web_api_service.helpers.all_config_func import (
    get_user_instance,
    get_department_instance,
    get_topic_instance
)
from web_api_service.notification.notification_all import notification_to_all_members

from task_management.models import Tasks


class ConfigService:
    """
    all ConfigService
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
        self.msg = None
        self.notification_services_names = {
            'topic_added': '__TOPICADDEDD__',
            'topic_deleted': '__TOPICDELETED__'
        }

    @staticmethod
    def mutual_serializer_manipulation(serializer_params):
        """
        This mutual_serializer_manipulation used to manage
        all serializer callable data
        """
        serializer = SerializerManipulationService(**serializer_params)
        return serializer()

    def department_detail(self):
        """
        this topic_detail get the topic details
        """
        user_instance = get_user_instance(
            {
                'is_active': True,
                'auth_user': self.auth_instance
            }
        )
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        _department_instance = Departments.objects.filter(
            id=self.query_params,
        ).last()
        department_serializer = DepartmentsSerializer(
            _department_instance,
            context={
                'user_instance': user_instance
            }
        )
        self.final_response['data'] = (
            department_serializer.data if department_serializer else {}
        )
        return self.final_response

    def department_detail_list_update_task(self):
        """this department_details method used to get department related data 
        in this method we get department details with in two db table single department master query 
        with alow access all parameters and add on user department mapping query
        params: auth_user_instance
        return: department_master_data (json)
        """
        user_instance = get_user_instance(
            {'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        _department_instance = Departments.objects.filter(
            is_active=True,
            access_status=ACCESS_STATUS[0][0]).order_by('department_name')
        if not _department_instance:
            self.department_master_data = []
        department_serializer = DepartmentsSerializer(
            _department_instance,
            context={'user_instance': user_instance}, 
            many=True
        )
        self.department_master_data = (
            department_serializer.data 
            if department_serializer else 
            []
        )

        user_department_serializer = SerializerManipulationService(
            type='__single__',
            model_class=UserDepartmentMapping,
            serializer_class=UserDepartmentMappingSerializer,
            query_params_var={
                'is_active': True,
                'user': self.auth_instance.user_auth
            },
        )

        try:
            task_department_data = []
            task_instance = Tasks.objects.filter(
                id=self.query_params.get("task_id")).last()
            if task_instance:
                task_department_instance = task_instance.department
                if task_department_instance:
                    department_serializer = DepartmentsSerializer(
                        task_department_instance,
                        context={'user_instance': user_instance},
                        # many=True
                    )
                    task_department_data = [department_serializer.data]
                else:
                    task_department_data = []
        except Exception as e:
            task_department_data = []
            print("TaskDepartmentExceptionError")
            print(e)

        try:
            self.department_master_data += task_department_data
        except Exception as e:
            print("departmentMasterErr")
            print(e)

        try:
            self.department_master_data += user_department_serializer(

            ).get('departments')
            self.department_master_data = [
                i for n, i in enumerate(self.department_master_data)
                if i not in self.department_master_data[n + 1:]
            ]
            self.department_master_data = sorted(
                list(self.department_master_data), 
                key=lambda x: x["department_name"],
                reverse=False
            )
        except Exception as e:
            print('user_department_serializer.exception')
            print(e)

        return {
            'success': True,
            'message': MSG['DONE'],
            'keyname': 'departments',
            'data': self.department_master_data,
            'status_code': status.HTTP_201_CREATED
        } if self.department_master_data else self.not_acceptable_response


    def department_detail_list(self):
        """this department_details method used to get department related data 
        in this method we get department details with in two db table single department master query 
        with alow access all parameters and add on user department mapping query
        params: auth_user_instance
        return: department_master_data (json)
        """
        user_instance = get_user_instance(
            {'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        _department_instance = Departments.objects.filter(
            is_active=True,
            access_status=ACCESS_STATUS[0][0],
        ).order_by('department_name')
        if not _department_instance:
            self.department_master_data = []
        department_serializer = DepartmentsSerializer(_department_instance, many=True)
        self.department_master_data = department_serializer.data if department_serializer else []

        user_department_serializer = SerializerManipulationService(
            type='__single__',
            model_class=UserDepartmentMapping,
            serializer_class=UserDepartmentMappingSerializer,
            query_params_var={'is_active': True,
                              'user': self.auth_instance.user_auth},
        )

        try:
            print('ddddd', user_department_serializer().get('departments'))
            self.department_master_data += user_department_serializer().get('departments')
            self.department_master_data = [
                i for n, i in enumerate(self.department_master_data)
                if i not in self.department_master_data[n + 1:]
            ]
            self.department_master_data = sorted(list(self.department_master_data),
                                                 key=lambda x: x["department_name"],
                                                 reverse=False)
        except Exception as e:
            print('user_department_serializer.exception')
            print(e)
        return {
            'success': True,
            'message': MSG['DONE'],
            'keyname': 'departments',
            'data': self.department_master_data,
            'status_code': status.HTTP_201_CREATED
        } if self.department_master_data else self.not_acceptable_response

    def assign_user_department(self, department_serializer_data):
        """
        this assign_user_topic method used to assign the topic with user only
        """
        user_query_params = {
            'user': self.auth_instance.user_auth
        }
        self.department_id_list.append(
            department_serializer_data.get('id', None))
        mapping_instance = UserDepartmentMapping.objects.filter(**user_query_params).first()
        if not mapping_instance:
            mapping_instance = UserDepartmentMapping.objects.create(**user_query_params)

        if mapping_instance:
            # mapping_instance.departments.set(self.department_id_list, clear=True)
            mapping_instance.departments.add(*self.department_id_list)
            self.final_response['keyname'] = "departments"
            self.final_response['data'] = department_serializer_data
            return self.final_response
        else:
            return self.not_acceptable_response

    def create_department_detail(self):
        """this create_department_detail method is used to create department details
        """
        if not self.config_req_data.get('access_status'):
            self.bad_request_response['message'] = MSG.get('ACCESS_STATUS_PROVIDE')
            return self.bad_request_response

        if 'Y' != self.config_req_data.get('access_status') and 'N' != self.config_req_data.get('access_status'):
            self.bad_request_response['message'] = MSG.get('VALID_CHOICE')
            return self.bad_request_response

        # department_name = self.config_req_data['department_name'].strip().capitalize().strip()

        department_name = self.config_req_data['department_name'].title()
        department_name = " ".join(department_name.strip().split())

        if already_exist_check_for_department(department_name, 'allow_to_all'):
            try:
                if self.auth_instance.user_auth.language.language_code == 'ENG':
                    self.msg = MSG.get('DEPARTMENT_ALREADY_EXISTS')
                else:
                    self.msg = ITALIAN_MSG.get('DEPARTMENT_ALREADY_EXISTS')
            except Exception as e:
                print('Exception')
                print(e)
                self.msg = MSG.get('DEPARTMENT_ALREADY_EXISTS')
            self.bad_request_response['message'] = self.msg
            return self.bad_request_response

            # check email already exists.
        if already_exist_check_for_department(department_name, 'self_only'):
            try:
                if self.auth_instance.user_auth.language.language_code == 'ENG':
                    self.msg = MSG.get('DEPARTMENT_ALREADY_EXISTS_PRIVATE')
                else:
                    self.msg = ITALIAN_MSG.get('DEPARTMENT_ALREADY_EXISTS_PRIVATE_ITL')
            except Exception as e:
                print('Exception')
                print(e)
                self.msg = MSG.get('DEPARTMENT_ALREADY_EXISTS_PRIVATE')
            self.bad_request_response['message'] = self.msg
            return self.bad_request_response

        department_serializer_data = self.mutual_serializer_manipulation({
            'serializer_class': DepartmentsSerializer,
            'type': '__create__',
            'request_data': {
                'department_name': department_name,
                'access_status': (
                    ACCESS_STATUS[0][0]
                    if self.config_req_data['access_status'] == 'Y' else
                    ACCESS_STATUS[1][0]
                )
            },
        })
        if not department_serializer_data:
            self.not_acceteptable_response['message'] = MSG.get('SERIALIZER_NOT_FOUND')
            return self.not_acceptable_response

        if self.config_req_data['access_status'] == 'N':
            return self.assign_user_department(department_serializer_data)
        self.final_response['keyname'] = "departments"
        self.final_response['data'] = department_serializer_data
        return self.final_response

    def topic_detail(self):
        """
        this topic_detail get the topic details
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        _topic_instance = Topics.objects.filter(
            id=self.query_params,
        ).last()

        topic_serializer = TopicsSerializer(_topic_instance)
        self.final_response['data'] = topic_serializer.data if topic_serializer else [
        ]
        return self.final_response

    def topic_detail_list_task_update(self):
        """this topic detail list task update api
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        _topic_instance = Topics.objects.filter(
            is_active=True,
            access_status=ACCESS_STATUS[0][0],
        ).order_by('topic_name')
        if not _topic_instance:
            self.topic_master_data = []
        topic_serializer = TopicsSerializer(_topic_instance, many=True)
        self.topic_master_data = topic_serializer.data if topic_serializer else []

        user_topic_serializer = SerializerManipulationService(
            type='__single__',
            model_class=UserTopicMapping,
            serializer_class=UserTopicMappingSerializer,
            query_params_var={'is_active': True,
                              'user': self.auth_instance.user_auth},
        )


        try:
            task_topic_data = []
            task_instance = Tasks.objects.filter(
                id=self.query_params.get("task_id")).last()
            if task_instance:
                task_topic_instance = task_instance.topic
                if task_topic_instance:
                    topic_serializer = TopicsSerializer(
                        task_topic_instance
                    )
                    task_topic_data = [topic_serializer.data]
                else:
                    task_topic_data = []
        except Exception as e:
            task_topic_data = []
            print("TaskTopicExceptionError")
            print(e)

        try:
            self.topic_master_data += task_topic_data
        except Exception as e:
            print("topicMasterErr")
            print(e)


        try:
            self.topic_master_data += user_topic_serializer().get('topics')
            self.topic_master_data = [
                i for n, i in enumerate(self.topic_master_data)
                if i not in self.topic_master_data[n + 1:]
            ]
            self.topic_master_data = sorted(list(self.topic_master_data),
                                            key=lambda x: x["topic_name"],
                                            reverse=False)
        except Exception as e:
            print('user_topic_serializer.exception')
            print(e)
        return {
            'success': True,
            'message': MSG['DONE'],
            'keyname': 'topics',
            'data': self.topic_master_data,
            'status_code': status.HTTP_201_CREATED
        } if self.topic_master_data else self.not_acceptable_response

    def topic_detail_list(self):
        """this topic_details method used to get topics related data
        params: auth_user_instance
        return: data
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        _topic_instance = Topics.objects.filter(
            is_active=True,
            access_status=ACCESS_STATUS[0][0],
        ).order_by('topic_name')
        if not _topic_instance:
            self.topic_master_data = []
        topic_serializer = TopicsSerializer(_topic_instance, many=True)
        self.topic_master_data = topic_serializer.data if topic_serializer else []

        user_topic_serializer = SerializerManipulationService(
            type='__single__',
            model_class=UserTopicMapping,
            serializer_class=UserTopicMappingSerializer,
            query_params_var={'is_active': True,
                              'user': self.auth_instance.user_auth},
        )
        try:
            self.topic_master_data += user_topic_serializer().get('topics')
            self.topic_master_data = [
                i for n, i in enumerate(self.topic_master_data)
                if i not in self.topic_master_data[n + 1:]
            ]
            self.topic_master_data = sorted(list(self.topic_master_data),
                                            key=lambda x: x["topic_name"],
                                            reverse=False)
        except Exception as e:
            print('user_topic_serializer.exception')
            print(e)
        return {
            'success': True,
            'message': MSG['DONE'],
            'keyname': 'topics',
            'data': self.topic_master_data,
            'status_code': status.HTTP_201_CREATED
        } if self.topic_master_data else self.not_acceptable_response

    def assign_user_topic(self, topic_serializer_data):
        """this assign_user_topic method used to assign the topic with user only
        """
        user_query_params = {
            'user': self.auth_instance.user_auth
        }
        self.topic_id_list.append(topic_serializer_data.get('id', None))
        mapping_instance = UserTopicMapping.objects.filter(**user_query_params).first()
        if not mapping_instance:
            mapping_instance = UserTopicMapping.objects.create(**user_query_params)
        if mapping_instance:
            mapping_instance.topics.add(*self.topic_id_list)
            self.final_response['keyname'] = 'topics'
            self.final_response['data'] = topic_serializer_data
            return self.final_response
        else:
            return self.not_acceptable_response

    def create_topic_detail(self):
        """this create_topic_detail method is used to create topics details
        """
        # topic_name = self.config_req_data['topic_name'].strip().capitalize().strip()

        # topic_name = " ".join(self.config_req_data['topic_name'].strip().split())
        topic_name = self.config_req_data['topic_name'].title()
        topic_name = " ".join(topic_name.strip().split())

        # check already exists.
        if already_exist_check_for_topic(topic_name, 'allow_to_all'):
            try:
                if self.auth_instance.user_auth.language.language_code == 'ENG':
                    self.msg = MSG.get('TOPIC_ALREADY_EXISTS')
                else:
                    self.msg = ITALIAN_MSG.get('TOPIC_ALREADY_EXISTS')
            except Exception as e:
                print('Exception')
                print(e)
                self.msg = MSG.get('TOPIC_ALREADY_EXISTS')

            self.bad_request_response['message'] = self.msg
            return self.bad_request_response

        # check already exists.
        if already_exist_check_for_topic(topic_name, 'self_only'):
            try:
                if self.auth_instance.user_auth.language.language_code == 'ENG':
                    self.msg = MSG.get('TOPIC_ALREADY_EXISTS_PRIVATE')
                else:
                    self.msg = ITALIAN_MSG.get('TOPIC_ALREADY_EXISTS_PRIVATE')
            except Exception as e:
                print('Exception')
                print(e)
                self.msg = MSG.get('TOPIC_ALREADY_EXISTS_PRIVATE')

            self.bad_request_response['message'] = self.msg
            return self.bad_request_response

        if self.config_req_data['access_status'] == 'Y' or self.config_req_data['access_status'] == 'y':
            try:
                notification_to_all_members(
                    api_service_name=self.notification_services_names['topic_added'],
                    topic_name=str(topic_name)
                )
            except Exception as e:
                print('NotificationToAllMemberExpErr')
                print(e)

        topic_serializer_data = self.mutual_serializer_manipulation(
            {
                'type': '__create__',
                'serializer_class': TopicsSerializer,
                'request_data': {
                    'topic_name': topic_name,
                    'description': self.config_req_data.get('description', None),
                    'access_status': (ACCESS_STATUS[0][0]
                                      if self.config_req_data['access_status'] == 'Y' else
                                      ACCESS_STATUS[1][0]),
                },
            }
        )
        if not topic_serializer_data:
            self.not_acceteptable_response['message'] = MSG.get('SERIALIZER_NOT_FOUND')
            return self.not_acceptable_response

        if self.config_req_data['access_status'] == 'N':
            return self.assign_user_topic(topic_serializer_data)
        self.final_response['keyname'] = 'topics'
        self.final_response['data'] = topic_serializer_data
        return self.final_response

    def delete_department_db(self, serializer_params):
        """
        this delete_department_db method used to delete the department from db
        """
        serializer_data = self.mutual_serializer_manipulation(serializer_params)
        self.final_response['data'] = ({'is_deleted': True} if serializer_data
                                       else {'is_deleted': False})
        return self.final_response

    def delete_department_db_v2(self, department_id):
        """
        this delete_department_db method used to delete the department from db
        """
        try:
            delete_auth_user = delete_auth_user_from_department_id(department_id)
            is_deleted_instance = Departments.objects.filter(id=department_id).delete()
            self.final_response['data'] = ({'is_deleted': True}
                                           if is_deleted_instance else
                                           {'is_deleted': False})
            return self.final_response
        except Exception as e:
            print('Departments.DoesNotDeleted')
            print(e)
            self.final_response['data'] = {'is_deleted': False}
            return self.final_response

    def update_department_remove_mapping(self, department_id):
        """
        update_department_remove_mapping
        """
        user_department_obj = UserDepartmentMapping.objects.filter(user=self.auth_instance.user_auth).first()
        user_department_obj.departments.remove(department_id)

    def update_department_detail(self):
        """update_department_detail
        """
        if self.config_req_data.get('access_status'):
            if 'Y' != self.config_req_data.get('access_status') \
                    and 'N' != self.config_req_data.get('access_status'):
                self.bad_request_response['message'] = MSG.get('VALID_CHOICE')
                return self.bad_request_response

        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        department_instance = get_department_instance({'id': self.config_req_data['department_id']})
        if not department_instance:
            self.bad_request_response['message'] = MSG.get('DEPARTMENT_ID_ERROR')
            return self.bad_request_response

        serializer_params = {
            'serializer_class': DepartmentsSerializer,
            'request_data': self.config_req_data,
            "model_instance": department_instance,
            "type": '__update__'
        }

        is_deleted_department = self.config_req_data.get('is_deleted', None)
        if is_deleted_department:
            return self.delete_department_db_v2(self.config_req_data['department_id'])

        try:
            self.config_req_data['access_status'] = (
                ACCESS_STATUS[0][0]
                if self.config_req_data['access_status'] == 'Y' else
                ACCESS_STATUS[1][0]
            )
        except Exception as e:
            print('errr')
            print(e)
            self.config_req_data['access_status'] = ACCESS_STATUS[0][0]

        department_serializer_data = self.mutual_serializer_manipulation(serializer_params)
        if not department_serializer_data:
            self.not_acceptable_response['message'] = MSG.get('DEPARTMENT_SERIALIZER_NOT_UPDATE')
            return self.not_acceptable_response

        self.final_response['data'] = department_serializer_data
        if self.config_req_data['access_status'] == 'self_only':
            return self.assign_user_department(department_serializer_data)

        try:
            self.update_department_remove_mapping(self.config_req_data.get('department_id'))
        except Exception as e:
            print('updateMemberMappingExpErr')
            print(e)

        return self.final_response

    def delete_topic_db(self, serializer_params):
        """
        this delete_topic_db method used to delete the department from db
        """
        serializer_data = self.mutual_serializer_manipulation(serializer_params)
        self.final_response['data'] = {'is_deleted': True} if serializer_data else {'is_deleted': False}
        return self.final_response

    def delete_topic_db_v2(self, topic_id):
        """
        this delete_topic_db method used to delete the department from db
        """
        try:
            try:
                topic_obj = Topics.objects.get(id=topic_id)
            except Exception as e:
                print('Topics.DoesNotExist')
                print(e)
                try:
                    if topic_obj.access_status == 'allow_to_all' or topic_obj.access_status == 'Y':
                        notification_to_all_members(
                            api_service_name=self.notification_services_names['topic_deleted'],
                            topic_name=str(topic_obj.topic_name)
                        )
                except Exception as e:
                    print('NotificationToAllMemberExpErr')
                    print(e)
            is_deleted_instance = Topics.objects.get(id=topic_id).delete()
            self.final_response['data'] = {'is_deleted': True} if is_deleted_instance else {'is_deleted': False}
            return self.final_response
        except Exception as e:
            print('Topics.DoesNot.Delete')
            print(e)
            self.final_response['data'] = {
                'is_deleted': False
            }
            return self.final_response

    def update_topic_remove_mapping(self, topic_id):
        """
        update_topic_remove_mapping
        """
        user_topic_obj = UserTopicMapping.objects.filter(user=self.auth_instance.user_auth).first()
        user_topic_obj.topics.remove(topic_id)

    def update_topic_detail(self):
        """this update_topic_detail method used update the all topics details with delete status
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        topic_instance = get_topic_instance({'id': self.config_req_data['topic_id']})
        if not topic_instance:
            self.bad_request_response['message'] = MSG.get('TOPIC_ID_ERROR')
            return self.bad_request_response

        serializer_params = {
            'serializer_class': TopicsSerializer,
            'request_data': self.config_req_data,
            'model_instance': topic_instance,
            'type': '__update__'
        }

        is_deleted_topic = self.config_req_data.get('is_deleted', None)
        if is_deleted_topic:
            return self.delete_topic_db_v2(self.config_req_data['topic_id'])

        self.config_req_data['access_status'] = (
            ACCESS_STATUS[0][0]
            if self.config_req_data['access_status'] == 'Y' else
            ACCESS_STATUS[1][0]
        )
        self.config_req_data['description'] = self.config_req_data.get('description', None)
        topic_serializer_data = self.mutual_serializer_manipulation(serializer_params)
        if not topic_serializer_data:
            self.not_acceptable_response['message'] = MSG.get('TOPIC_SERIALIZER_NOT_UPDATE')
            return self.not_acceptable_response

        self.final_response['data'] = topic_serializer_data
        if self.config_req_data['access_status'] == 'self_only':
            return self.assign_user_topic(topic_serializer_data)

        try:
            self.update_topic_remove_mapping(self.config_req_data.get('topic_id'))
        except Exception as e:
            print('updateMemberMappingExpErr')
            print(e)

        return self.final_response
