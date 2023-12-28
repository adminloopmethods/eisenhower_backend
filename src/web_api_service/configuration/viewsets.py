"""
all configuration apis
"""
import http
from web_api_service.configuration.language_service import LanguageManageService
from rest_framework import status
# import rest apps
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

# all helper apps
from core.api_response_parser import APIResponseParser, request_not_found
from core.messages import API_RESPONSE_MSG, MSG, ITALIAN_MSG

# import department service
from web_api_service.configuration.services import ConfigService
from web_api_service.configuration.config_filter_service import ConfigFilterService
from web_api_service.configuration.import_export_service import ImportExportService



class DepartmentTaskUpdateApi(LoggingMixin, APIView):
    """
    
    """
    def get(self, request):
        """DepartmentListApi
        usage:this get method used to get the all department of as per system logic
        path: /api/v1/config/department/task/update/?id=
        Authorization: YES
        Method: GET
        response: {
            "departments": [
                {
                    "id": "5164ec0e-63f0-4d0b-b017-ae67516e9863",
                    "created_at": "2022-08-23T09:41:28.729641Z",
                    "updated_at": "2022-08-23T09:41:28.729700Z",
                    "is_active": true,
                    "department_name": "Development",
                    "description": ""
                },
                {
                    "id": "c5208922-52b0-4e8c-9498-367e9eed09a7",
                    "created_at": "2022-08-18T10:27:56.281243Z",
                    "updated_at": "2022-08-23T09:41:33.270580Z",
                    "is_active": true,
                    "department_name": "IT",
                    "description": ""
                }
            ],
            "success": true,
            "message": "Done"
        }
        """
        response = ConfigService(
            auth_instance=request.user,
            query_params=request.query_params
        ).department_detail_list_update_task()
        return APIResponseParser.response(**response)





class DepartmentApi(LoggingMixin, APIView):
    """CreateGetDepartment
    usage: this enpoint used to create department and access with all or self user.
    path: /api/v1/config/department/
    Method: GET/POST
    Auth: YES
    """
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}
        self.request_not_found = request_not_found()

    def get(self, request):
        """DepartmentListApi
        usage:this get method used to get the all department of as per system logic
        path: /api/v1/config/department/
        Authorization: YES
        Method: GET
        response: {
            "departments": [
                {
                    "id": "5164ec0e-63f0-4d0b-b017-ae67516e9863",
                    "created_at": "2022-08-23T09:41:28.729641Z",
                    "updated_at": "2022-08-23T09:41:28.729700Z",
                    "is_active": true,
                    "department_name": "Development",
                    "description": ""
                },
                {
                    "id": "c5208922-52b0-4e8c-9498-367e9eed09a7",
                    "created_at": "2022-08-18T10:27:56.281243Z",
                    "updated_at": "2022-08-23T09:41:33.270580Z",
                    "is_active": true,
                    "department_name": "IT",
                    "description": ""
                }
            ],
            "success": true,
            "message": "Done"
        }
        """
        response = ConfigService(auth_instance=request.user).department_detail_list()
        return APIResponseParser.response(**response)

    def post(self, request):
        """CreateDepartmentApi
        usage: this post method used to post department of as per system logic
        path: /api/v1/config/department/
        Authorization: YES
        method: POST
        request: {
            "department_name": "manager",
            "access_status": "A"
        }
        response: {
            "departments": [],
            "success": true,
            "message": "Department status update"
        }
        """
        if not request.data:
            return APIResponseParser.response(**self.request_not_found)

        if not request.data.get('department_name'):
            self.errors.append(
                {'department_name': API_RESPONSE_MSG['PLEASE_PROVIDE_DEPARTMENT_NAME']}
            )

        if not request.data.get('access_status'):
            self.errors.append(
                {'access_status': API_RESPONSE_MSG['PLEASE_PROVIDE_ACCESS_STATUS']}
            )

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['ERRORS'],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        self.service_req_data = {
            'auth_instance': request.user,
            'config_req_data': request.data.copy()
        }
        resp = ConfigService(**self.service_req_data).create_department_detail()
        return APIResponseParser.response(**resp)

    def put(self, request):
        """UpdateDepartmentApi
        usage: this put method used to update department of as per system logic
        path: /api/v1/config/department/
        Authorization: YES
        method: PUT
        request: {
            "department_id": "76a13ef9-c48a-4741-8d78-520b1e59a5f5",
            "department_name": "systems adminstrative",
            "access_status": "Y"
        }
        or request: {
            "department_id": "76a13ef9-c48a-4741-8d78-520b1e59a5f5",
            "is_deleted": "1/0"
        }
        response: {
            "data": {
                "id": "3aeeecf3-32ae-4f95-a3f6-7b1cd46849a3",
                "created_at": "2022-08-29T10:57:29.946404Z",
                "updated_at": "2022-08-29T10:57:29.946440Z",
                "is_active": true,
                "department_name": "systems adminstrative",
                "description": null,
                "access_status": "allow_to_all",
                "is_deleted": false
            },
            "success": true,
            "message": "Done"
        } or response: {
            "data": {
                "is_deleted": true
            },
            "success": true,
            "message": "Done"
        }
        """
        if not request.data:
            return APIResponseParser.response(**self.request_not_found)
        self.service_req_data = {
            'auth_instance': request.user,
            'config_req_data': request.data.copy()
        }
        resp = ConfigService(**self.service_req_data).update_department_detail()
        return APIResponseParser.response(**resp)


class TopicApi(LoggingMixin, APIView):
    """TopicApi
    usage: this enpoint used to create topics and access with all or self user.
    path: /api/v1/config/topic/
    Authorization: YES
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}
        self.request_not_found = request_not_found()

    def get(self, request):
        """
        TopicListApi
        this get method used to get the all topic of as per system logic
        path: /api/v1/config/topic/
        Method: GET
        Authorization: YES
        response: {
            "topics": [
                {
                    "id": "5164ec0e-63f0-4d0b-b017-ae67516e9863",
                    "created_at": "2022-08-23T09:41:28.729641Z",
                    "updated_at": "2022-08-23T09:41:28.729700Z",
                    "is_active": true,
                    "topic_name": "Development",
                    "description": ""
                },
                {
                    "id": "c5208922-52b0-4e8c-9498-367e9eed09a7",
                    "created_at": "2022-08-18T10:27:56.281243Z",
                    "updated_at": "2022-08-23T09:41:33.270580Z",
                    "is_active": true,
                    "topic_name": "IT",
                    "description": ""
                }
            ],
            "success": true,
            "message": "Done"
        }
        """
        resp = ConfigService(auth_instance=request.user).topic_detail_list()
        return APIResponseParser.response(**resp)

    def post(self, request):
        """
        CreateTopicApi
        this post method used to post topics of as per system logic
        path: /api/v1/config/topic/
        Method: POST
        Authorization: YES
        request: {
            "topic_name": "manager",
            "access_status": "A",
            "description": "values"
        }
        response: {
            "topics": [],
            "success": true,
            "message": "Topics status update"
        }
        """
        if not request.data:
            return APIResponseParser.response(
                **self.request_not_found
            )
        if not request.data.get('topic_name'):
            self.errors.append(
                {'topic_name': API_RESPONSE_MSG['PLEASE_PROVIDE_TOPIC_NAME']}
            )

        if not request.data.get('access_status'):
            self.errors.append(
                {'access_status': API_RESPONSE_MSG['PLEASE_PROVIDE_ACCESS_STATUS']}
            )

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['ERRORS'],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        self.service_req_data = {
            'auth_instance': request.user,
            'config_req_data': request.data.copy()
        }
        resp = ConfigService(**self.service_req_data).create_topic_detail()
        return APIResponseParser.response(**resp)

    def put(self, request):
        """UpdateTopicApi
        this put method used to update topics of as per system logic
        path: /api/v1/config/topic/
        Method: PUT
        Authorization: YES
        request: {
            "topic_id": "c0be33a9-f4ba-49a1-83dc-008affa4bfcc",
            "topic_name": "data",
            "access_status": "Y"
        }
        or request {
            "topic_id": "c0be33a9-f4ba-49a1-83dc-008affa4bfcc",
            "is_deleted": "1"
        }
        response:{
                "data": {
            "data": {
                "is_deleted": true
            },
            "success": true,
            "message": "Done"
        }
        """
        if not request.data:
            return APIResponseParser.response(
                **self.request_not_found
            )
        self.service_req_data = {
            'auth_instance': request.user,
            'config_req_data': request.data.copy()
        }
        resp = ConfigService(**self.service_req_data).update_topic_detail()
        return APIResponseParser.response(**resp)


class DepartmentDetailApi(LoggingMixin, APIView):
    """DepartmentDetailApi
    usage: this enpoint used to get department details.
    method: GET
    path: /api/v1/config/department/detail/?id=5b0805ca-b150-4897-8bd6-e130f7cc3c25
    Authorization: YES
    response:
        Method: GET
        Authorization: YES
        response: {
            "data": {
                "id": "5b0805ca-b150-4897-8bd6-e130f7cc3c25",
                "created_at": "2022-08-30T08:57:40.538214Z",
                "updated_at": "2022-08-30T08:57:40.538233Z",
                "is_active": true,
                "department_name": "It",
                "description": null,
                "access_status": "allow_to_all",
                "is_deleted": false
            },
            "success": true,
            "message": "Done"
        }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def get(self, request):
        """
        TopicListApi
        this get method used to get the all topic of as per system logic
        """
        service_req_data = {
            'auth_instance': request.user,
            'query_params': (
                None
                if request.query_params.get('id', None) == ""
                   or request.query_params.get('id', None) is None else
                request.query_params.get('id', None)
            )
        }

        resp = ConfigService(**service_req_data).department_detail()
        return APIResponseParser.response(**resp)

class TopicDetailTaskUpdateApi(LoggingMixin, APIView):
    """TopicDetailApi
    usage: this endpoint used to get topic details.
    path: /api/v1/config/topic/detail/task/update/?task_id=a946de3e-6329-4b9d-b28a-4bc0ead8c23a
    Authorization: YES
    method: GET
    response:{
        "data": {
            "id": "cf82a17b-d171-4f6a-b6ec-3aa2ff644952",
            "created_at": "2022-08-25T06:34:16.338382Z",
            "updated_at": "2022-08-25T06:34:16.338435Z",
            "is_active": true,
            "topic_name": "Pops",
            "description": null,
            "access_status": "allow_to_all",
            "is_deleted": false,
            "created_by": null,
            "updated_by": null
        },
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def get(self, request):
        """
        TopicListApi
        this get method used to get the all topic of as per system logic
        """

        service_req_data = {
            'auth_instance': request.user,
            'query_params': request.query_params
        }

        resp = ConfigService(**service_req_data).topic_detail_list_task_update()
        return APIResponseParser.response(**resp)


class TopicDetailApi(LoggingMixin, APIView):
    """TopicDetailApi
    usage: this endpoint used to get topic details.
    path: /api/v1/config/topic/detail/?id=cf82a17b-d171-4f6a-b6ec-3aa2ff644952
    Authorization: YES
    method: GET
    response:{
        "data": {
            "id": "cf82a17b-d171-4f6a-b6ec-3aa2ff644952",
            "created_at": "2022-08-25T06:34:16.338382Z",
            "updated_at": "2022-08-25T06:34:16.338435Z",
            "is_active": true,
            "topic_name": "Pops",
            "description": null,
            "access_status": "allow_to_all",
            "is_deleted": false,
            "created_by": null,
            "updated_by": null
        },
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def get(self, request):
        """
        TopicListApi
        this get method used to get the all topic of as per system logic
        """

        service_req_data = {
            'auth_instance': request.user,
            'query_params': (
                None
                if request.query_params.get('id', None) == ""
                   or request.query_params.get('id', None) is None else
                request.query_params.get('id', None)
            )
        }

        resp = ConfigService(**service_req_data).topic_detail()
        return APIResponseParser.response(**resp)


class DepartmentSearchApi(LoggingMixin, APIView):
    """DepartmentSearchApi
    usage: this endpoint used to get the department values search by user
    path: /api/v1/config/department/search/?q=ya
    Authorization: YES
    method: GET
    response:{
        "data": {
            "id": "cf82a17b-d171-4f6a-b6ec-3aa2ff644952",
            "created_at": "2022-08-25T06:34:16.338382Z",
            "updated_at": "2022-08-25T06:34:16.338435Z",
            "is_active": true,
            "topic_name": "Pops",
            "description": null,
            "access_status": "allow_to_all",
            "is_deleted": false,
            "created_by": null,
            "updated_by": null
        },
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def get(self, request):
        """
        TopicListApi
        this get method used to get the all topic of as per system logic
        """

        self.service_req_data = {
            'auth_instance': request.user,
            'query_params': request.query_params
        }
        resp = ConfigFilterService(
            **self.service_req_data).search_department_list()
        return APIResponseParser.response(**resp)


class TopicSearchApi(LoggingMixin, APIView):
    """TopicSearchApi
    usage: this endpoint used to get topic details.
    path: /api/v1/config/topic/search/?q=oo
    Authorization: YES
    method: GET
    response:{
        "data": [
            {
                "id": "88b18b56-a8a1-4495-a77b-eb82d68f86a1",
                "created_at": "2022-08-25T06:31:37.070025Z",
                "updated_at": "2022-08-31T12:36:45.896728Z",
                "is_active": true,
                "topic_name": "oopsasbsdsds",
                "description": null,
                "access_status": "self_only",
                "is_deleted": false,
                "created_by": null,
                "updated_by": null
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def get(self, request):
        """
        TopicListApi
        this get method used to get the all topic of as per system logic
        """

        self.service_req_data = {
            'auth_instance': request.user,
            'query_params': request.query_params
        }
        resp = ConfigFilterService(**self.service_req_data).search_topic_list()
        return APIResponseParser.response(**resp)


class DepartmentSampleSheetApi(LoggingMixin, APIView):
    """DepartmentSampleSheet
    usage: this endpoint used to download department sample sheet.
    path: /api/v1/config/department/sample/sheet/
    Authorization: YES
    method: GET
    response:{
        "data": [
            {
                "id": "88b18b56-a8a1-4495-a77b-eb82d68f86a1",
                "created_at": "2022-08-25T06:31:37.070025Z",
                "updated_at": "2022-08-31T12:36:45.896728Z",
                "is_active": true,
                "topic_name": "oopsasbsdsds",
                "description": null,
                "access_status": "self_only",
                "is_deleted": false,
                "created_by": null,
                "updated_by": null
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def get(self, request):
        """
        TopicListApi
        this get method used to get the all topic of as per system logic
        """

        self.service_req_data = {
            'auth_instance': request.user,
        }
        return ImportExportService(**self.service_req_data).export_department_sample()


class DepartmentImportSheetApi(APIView):
    """DepartmentSampleSheet
    usage: this endpoint used to download department sample sheet.
    path: /api/v1/config/department/import/sheet/
    Authorization: YES
    method: POST
    request: 
        import_file: media_file 
    response:{
        "data": {
            "new_created_ids": [
                {
                    "id": "3bf98131-a8c9-48e9-a5d5-42bf2080e7b6",
                    "department_name": "Towards"
                }
            ],
            "data_pool_list": []
        },
        "success": true,
        "message": "Done"
    }
    or {
        "data": {
            "new_created_ids": [],
            "data_pool_list": [
                "a6d55fb1-c5b6-446b-97b0-ee787f8fd180"
            ]
        },
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.config_req_data = {}
        self.service_req_data = {}
        self.request_not_found = request_not_found()

    def post(self, request):
        """
        DepartmentImportSheetApi
        this get method used to get the all topic of as per system logic
        """
        if not request.data:
            return APIResponseParser.response(
                **self.request_not_found)

        self.config_req_data = request.data
        self.config_req_data._mutable = True

        if not self.config_req_data.get('import_file', None):
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG['IMPORT_FILE_NAME_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST)

        try:
            self.service_req_data = {
                'auth_instance': request.user,
                'config_req_data': self.config_req_data
            }
            resp = ImportExportService(**self.service_req_data).import_department_list()
            return APIResponseParser.response(**resp)
        except Exception as e:
            print('ImportExportService.DoesNotExist: %s' % e)
            return APIResponseParser.response(
                success=False,
                # message='please resolved  %s' % str(e),
                message=MSG["CORRECT_SHEET_ERROR"],
                status_code=status.HTTP_400_BAD_REQUEST
            )


class LanguageApi(LoggingMixin, APIView):
    """LanguageApi
    usage: this endpoint used to get and create language with change status.
    path: /api/v1/config/language/
    Authorization: YES
    method: POST
    request: 
        import_file: media_file 
    response:{
        "data": {
            "new_created_ids": [
                {
                    "id": "3bf98131-a8c9-48e9-a5d5-42bf2080e7b6",
                    "department_name": "Towards"
                }
            ],
            "data_pool_list": []
        },
        "success": true,
        "message": "Done"
    }
    or {
        "data": {
            "new_created_ids": [],
            "data_pool_list": [
                "a6d55fb1-c5b6-446b-97b0-ee787f8fd180"
            ]
        },
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.config_req_data = {}
        self.service_req_data = {}
        self.request_not_found = request_not_found()

    def get(self, request):
        """This GET method used to get the list of lanaguage list
        path: /api/v1/config/language/
        response: {
        "data": [
            {
                "id": "f950d8bb-955f-4322-ac01-f51354067a03",
                "created_at": "2022-09-26T09:01:02.635118Z",
                "updated_at": "2022-09-26T09:01:02.635154Z",
                "is_active": true,
                "language_code": "ENG",
                "language_name": "English",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "8715db8d-cfee-48e2-86b2-cddcbc51c3de",
                "created_at": "2022-09-26T09:01:10.356198Z",
                "updated_at": "2022-09-26T09:01:10.356282Z",
                "is_active": true,
                "language_code": "ITL",
                "language_name": "Italian",
                "created_by": 1,
                "updated_by": null
            }
        ],
        "success": true,
        "message": "Done"
        }
        """
        return APIResponseParser.response(**LanguageManageService().get_language_list()
        )

    def post(self, request):
        """
        DepartmentImportSheetApi
        this get method used to get the all topic of as per system logic
        path:
        request: {
            "language": "f950d8bb-955f-4322-ac01-f51354067a03"
        }
        response: {
            "data": {
                "language_changed": true
            },
            "success": true,
            "message": "Done"
        }
        """
        try:
            self.service_req_data = {
                'auth_instance': request.user,
                'config_req_data': request.data.copy()
            }
            return APIResponseParser.response(
                **LanguageManageService(**self.service_req_data).change_user_language()
            )
        except Exception as e:
            print('LanguageChangeApi.ExceptionError', e)
            return APIResponseParser.response(
                status=False,
                messages=str(e),
                status_code=status.HTTP_400_BAD_REQUEST)
