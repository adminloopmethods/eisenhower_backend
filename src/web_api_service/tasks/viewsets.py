from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from configuration.models import TaskBulkDataExcelFiles

from core.api_response_parser import APIResponseParser, request_not_found
from core.messages import API_RESPONSE_MSG, MSG
from web_api_service.helpers.validations import APIValidation
from web_api_service.tasks.import_task_service import ImportExportTaskService

# import service
from web_api_service.tasks.services import TaskService
from web_api_service.tasks.tasksexportservice import ExportTasksService
from web_api_service.tasks.task_comments_service import TaskCommentService


class CreateTaskApi(LoggingMixin, APIView):
    """
    CreateTaskApi api
    usage: this end-point create the task for members.
    path: /api/v1/task/create/
    method: POST
    Authorization: YES
    request: {
        "task_name":"other test task name",
        "customer_name": "Gourav Sharma",
        "description": "test desc",
        "start_date":"2022-08-26T10:06:50.120917",
        "due_date":"2022-08-30T10:06:50.120917",
        "estimate": "20",
        "notes": "test nodes",
        "reminder":"2022-08-28T10:06:50.120917",
        "status": "f4f2493b-8108-4f7a-af6f-7d55238f6417",
        "department": "e0e06fd2-fbda-4854-b003-8a3e2487a56a",
        "topic":"88b18b56-a8a1-4495-a77b-eb82d68f86a1",
        "members":["af2cac3a-bec7-44dc-a0b7-5e3c33323db2", "e055dbae-13c9-4ea8-83a6-90f806cda1a8"],
        "task_owner":"7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
        "importance":"low",
        "urgency": "high"
    }
    Response:{
        "data": {
            "id": "da830e31-d26b-4a56-8399-b24413490674",
            "task_name": "other test task name",
            "customer_name": "Gourav Sharma",
            "description": "test desc",
            "start_date": "2022-08-26T10:06:50.120917Z",
            "due_date": "2022-08-30T10:06:50.120917Z",
            "estimate": "20",
            "notes": "test nodes",
            "comments": null,
            "reminder": "2022-08-28T10:06:50.120917Z",
            "status": "f4f2493b-8108-4f7a-af6f-7d55238f6417",
            "department": "e0e06fd2-fbda-4854-b003-8a3e2487a56a",
            "topic": "88b18b56-a8a1-4495-a77b-eb82d68f86a1",
            "members": [
                "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                "e055dbae-13c9-4ea8-83a6-90f806cda1a8"
            ],
            "task_owner": "7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
            "matrix_type_config": "67a34a11-c7b3-4cda-8216-21e931561535"
        },
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.task_req_data = {}

    def post(self, request):
        """
        get the user details using token
        """
        if not request.data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # all basic fields
        # if not request.data.get('task_owner'):
        #     self.errors.append({'task_owner': API_RESPONSE_MSG['PROVIDE_TASK_OWNER']})
        if not request.data.get("task_name"):
            self.errors.append({"task_name": API_RESPONSE_MSG["PROVIDE_TASK_NAME"]})
        # if not request.data.get('customer_name'):
        #     self.errors.append({'customer_name': API_RESPONSE_MSG['PROVIDE_CUSTOMER_NAME']})

        # all datetime fields
        # if not request.data.get('start_date'):
        #     self.errors.append({'start_date': API_RESPONSE_MSG['PROVIDE_START_DATE']})
        # if not request.data.get('due_date'):
        #     self.errors.append({'due_date': API_RESPONSE_MSG['PROVIDE_DUE_DATE']})
        # if not request.data.get('reminder'):
        #     self.errors.append({'reminder': API_RESPONSE_MSG['PROVIDE_REMINDER']})

        # all fk relation fields
        if not request.data.get("status"):
            self.errors.append({"status": API_RESPONSE_MSG["PROVIDE_STATUS"]})
        if not request.data.get("department"):
            self.errors.append(
                {"department": API_RESPONSE_MSG["PLEASE_PROVIDE_DEPARTMENT_ID"]}
            )
        # if not request.data.get('topic'):
        #     self.errors.append({'topic': API_RESPONSE_MSG['PLEASE_PROVIDE_TOPIC_ID']})

        # all m2m relation fields
        if not request.data.get("members"):
            self.errors.append({"members": API_RESPONSE_MSG["PROVIDE_MEMBERS"]})

        # all matrix config rule params
        # if not request.data.get('importance'):
        #     self.errors.append({'importance': API_RESPONSE_MSG['PROVIDE_MATRIX']})
        # if not request.data.get('urgency'):
        #     self.errors.append({'urgency': API_RESPONSE_MSG['PROVIDE_MATRIX']})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        self.task_req_data = {
            "auth_instance": request.user,
            "task_req_data": request.data.copy(),
        }
        print(request.data.copy())
        resp = TaskService(**self.task_req_data).create_task()
        return APIResponseParser.response(**resp)


class TaskListApi(LoggingMixin, APIView):
    """
    TaskListApi
    usage: this end-point get the task list as per user request status
    path: /api/v1/task/list/?status=all&matrix_id=0f167aea-92b0-46a4-bbbe-afc303e60f04
    method: GET
    Authorization: YES
    Response: {
        "data": [
            {
                "id": "0855a050-e285-432b-8874-287cb7197913",
                "task_name": "new test task name",
                "customer_name": "Gourav Sharma",
                "description": "test desc",
                "start_date": "2022-08-26T10:06:50.120917Z",
                "due_date": "2022-08-30T10:06:50.120917Z",
                "estimate": "20",
                "notes": "test nodes",
                "comments": null,
                "reminder": "2022-08-28T10:06:50.120917Z",
                "status": "Pending",
                "department": "yml",
                "topic": "oops",
                "members": [
                    {
                        "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                        "color": "#00FF00",
                        "role": "Member",
                        "created_at": "2022-08-25T12:34:50.336439Z",
                        "updated_at": "2022-08-26T09:04:51.908585Z",
                        "is_active": true,
                        "first_name": "Sumeet",
                        "last_name": "Singh",
                        "email": "sumeet@gmail.com",
                        "mobile": "8989209090",
                        "access_status": "allow_to_all",
                        "registration_type": "web",
                        "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                        "auth_user": 7
                    },
                    {
                        "id": "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                        "color": "#FFCCCB",
                        "role": "Member",
                        "created_at": "2022-08-25T12:29:09.245668Z",
                        "updated_at": "2022-08-26T09:05:10.062389Z",
                        "is_active": true,
                        "first_name": "Sameer",
                        "last_name": "Singh",
                        "email": "smaeersharma@gmail.com",
                        "mobile": "8989209090",
                        "access_status": "allow_to_all",
                        "registration_type": "web",
                        "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                        "auth_user": 6
                    }
                ],
                "task_owner": "Gourav",
                "matrix_type_config": "Priority 3"
            },
            {
                "id": "311e0fa2-2433-4ce0-b681-96e75955b1c8",
                "task_name": "high test task name",
                "customer_name": "Gourav Sharma",
                "description": "test desc",
                "start_date": "2022-08-26T10:06:50.120917Z",
                "due_date": "2022-08-30T10:06:50.120917Z",
                "estimate": "20",
                "notes": "test nodes",
                "comments": null,
                "reminder": "2022-08-28T10:06:50.120917Z",
                "status": "Pending",
                "department": "yml",
                "topic": "oops",
                "members": [
                    {
                        "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                        "color": "#00FF00",
                        "role": "Member",
                        "created_at": "2022-08-25T12:34:50.336439Z",
                        "updated_at": "2022-08-26T09:04:51.908585Z",
                        "is_active": true,
                        "first_name": "Sumeet",
                        "last_name": "Singh",
                        "email": "sumeet@gmail.com",
                        "mobile": "8989209090",
                        "access_status": "allow_to_all",
                        "registration_type": "web",
                        "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                        "auth_user": 7
                    },
                    {
                        "id": "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                        "color": "#FFCCCB",
                        "role": "Member",
                        "created_at": "2022-08-25T12:29:09.245668Z",
                        "updated_at": "2022-08-26T09:05:10.062389Z",
                        "is_active": true,
                        "first_name": "Sameer",
                        "last_name": "Singh",
                        "email": "smaeersharma@gmail.com",
                        "mobile": "8989209090",
                        "access_status": "allow_to_all",
                        "registration_type": "web",
                        "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                        "auth_user": 6
                    }
                ],
                "task_owner": "Gourav",
                "matrix_type_config": "Priority 1"
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.task_req_data = {}

    def get(self, request):
        """
        get_queryset the user details using token
        """
        if not request.query_params.get("status"):
            self.errors.append({"status": API_RESPONSE_MSG["PROVIDE_STATUS"]})
        if not request.query_params.get("matrix_id"):
            self.errors.append({"matrix_id": API_RESPONSE_MSG["PROVIDE_MATRIX"]})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.task_req_data = {
            "auth_instance": request.user,
            "task_list_params": request.query_params,
        }
        resp = TaskService(**self.task_req_data).task_list()
        return APIResponseParser.response(**resp)


class TaskStatusChangeApi(LoggingMixin, APIView):
    """TaskStatusChangeApi
    path: /api/v1/task/statusUpdate/?\
    status=b56d1bff-cc4b-4488-a9dd-d5fba4b7d1ed&task=9552eb41-31d7-49fe-846a-8d25f8b914ac
    Authorization: YES
    method: GET
    Response:{
        "data": {
            "is_status_changed": true
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
        get the team details using token
        """
        if not request.query_params:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not request.query_params.get("status"):
            self.errors.append({"status": API_RESPONSE_MSG["PLEASE_PROVIDE_STATUS"]})
        if not request.query_params.get("task"):
            self.errors.append({"task": API_RESPONSE_MSG["PLEASE_PROVIDE_TASK"]})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "task_list_params": request.query_params,
        }
        resp = TaskService(**self.service_req_data).task_status_update()
        return APIResponseParser.response(**resp)


class TaskFilterApi(LoggingMixin, APIView):
    """
        TaskFilterApi
        usage: this end-point create the task for members.
        path: /api/v1/task/filter/
        method: POST
        Authorization: YES
        request: {
            "matrix_id": "0f167aea-92b0-46a4-bbbe-afc303e60f04",
            "status": "all/To-do/In-progress/Done",
            "department": "e0e06fd2-fbda-4854-b003-8a3e2487a56a",
            "topic": "88b18b56-a8a1-4495-a77b-eb82d68f86a1",
            "members": ["581dc577-eb52-4990-8b8b-f4f007129ed6"],
            "start_datetime": "2022-08-26",
            "due_datetime": "2022-08-30"
        }
        Response:{
        "data": [
            {
                "id": "311e0fa2-2433-4ce0-b681-96e75955b1c8",
                "task_name": "high test task name",
                "customer_name": "Gourav Sharma",
                "description": "test desc",
                "start_date": "26-08-2022",
                "due_date": "30-08-2022",
                "estimate": "20",
                "notes": "test nodes",
                "comments": null,
                "reminder": "2022-08-28T10:06:50.120917Z",
                "status": "To-do",
                "department": "yml",
                "topic": "oopsasbsdsds",
                "members": [
                    {
                        "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                        "created_at": "2022-08-25T12:34:50.336439Z",
                        "updated_at": "2022-08-26T09:04:51.908585Z",
                        "is_active": true,
                        "first_name": "Sumeet",
                        "last_name": "Singh",
                        "email": "sumeet@gmail.com",
                        "mobile": "8989209090",
                        "access_status": "allow_to_all",
                        "registration_type": "web",
                        "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                        "color": "e026aa15-ec41-4b0c-aaac-e574b0856ed5",
                        "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                        "auth_user": 7
                    },
                    {
                        "id": "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                        "created_at": "2022-08-25T12:29:09.245668Z",
                        "updated_at": "2022-08-26T09:05:10.062389Z",
                        "is_active": false,
                        "first_name": "Sameer",
                        "last_name": "Singh",
                        "email": "smaeersharma@gmail.com",
                        "mobile": "8989209090",
                        "access_status": "allow_to_all",
                        "registration_type": "web",
                        "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                        "color": "996bfc3d-a329-42a5-9b09-72629716ce43",
                        "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                        "auth_user": 6
                    }
                ],
                "task_owner": "Gourav",
                "matrix_type_config": "Priority 1",
                "status_id": "f4f2493b-8108-4f7a-af6f-7d55238f6417"
            },
        ],
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def post(self, request):
        """
        get the user details using token
        """
        if not request.data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not request.data.get("status"):
            self.errors.append({"status": API_RESPONSE_MSG["PROVIDE_STATUS"]})
        if not request.data.get("matrix_id"):
            self.errors.append({"matrix_id": API_RESPONSE_MSG["PROVIDE_MATRIX"]})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "task_req_data": request.data.copy(),
        }
        resp = TaskService(**self.service_req_data).filter_task_list()
        return APIResponseParser.response(**resp)


class TaskDetailsApi(LoggingMixin, APIView):
    """
    TaskDetailsApi
    usage: this end-point get the task details as per user request status
    path: /api/v1/task/detail/?task_id=9552eb41-31d7-49fe-846a-8d25f8b914ac
    method: GET
    Authorization: YES
    Response: {
        "data": {
            "id": "9552eb41-31d7-49fe-846a-8d25f8b914ac",
            "task_name": "high test task name",
            "customer_name": "Gourav Sharma",
            "description": "test desc",
            "start_date": "26-08-2022",
            "due_date": "30-08-2022",
            "estimate": "20",
            "notes": "test nodes",
            "comments": "",
            "reminder": "2022-08-28T10:06:50Z",
            "status": "In-Progress",
            "department": "yml",
            "topic": "oopsasbsdsds",
            "members": [
                {
                    "id": "581dc577-eb52-4990-8b8b-f4f007129ed6",
                    "created_at": "2022-09-02T11:03:59.310699Z",
                    "updated_at": "2022-09-02T11:03:59.310739Z",
                    "is_active": true,
                    "first_name": "Ravi",
                    "last_name": "Kamlesh",
                    "email": "ravikamlesh@gmail.com",
                    "mobile": "8989209090",
                    "access_status": "self_only",
                    "registration_type": "web",
                    "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                    "color": "996bfc3d-a329-42a5-9b09-72629716ce43",
                    "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                    "auth_user": 53
                },
                {
                    "id": "f575a5d2-83c2-4370-9e20-6329f3e380dd",
                    "created_at": "2022-08-30T06:45:09.447903Z",
                    "updated_at": "2022-08-30T06:45:09.447939Z",
                    "is_active": true,
                    "first_name": "Khalid",
                    "last_name": "Khan",
                    "email": "khalid123@gmail.com",
                    "mobile": "9873198677",
                    "access_status": "allow_to_all",
                    "registration_type": "web",
                    "department": "fb7b6de9-b1de-49fb-b87c-6254663b92d2",
                    "color": null,
                    "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                    "auth_user": 38
                }
            ],
            "task_owner": "Gourav",
            "matrix_type_config": "Priority 1",
            "status_id": "b56d1bff-cc4b-4488-a9dd-d5fba4b7d1ed",
            "matrix_config_detail": {
                "Importance": "High",
                "Urgency": "High"
            }
        },
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def get(self, request):
        """
        get_queryset the user details using token
        """
        if not request.query_params.get("task_id"):
            self.errors.append({"status": API_RESPONSE_MSG["PLEASE_PROVIDE_TASK"]})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "task_list_params": request.query_params,
        }
        resp = TaskService(**self.service_req_data).task_details()
        return APIResponseParser.response(**resp)


class ExportTasks(LoggingMixin, APIView):
    """
    PATH: /api/v1/task/export/?all_id=76328c60-3921-4ec6-9029-38cbb233df80
    """

    # permission_classes = (IsAuthenticated,)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def get(self, request):
        if not request.query_params.get("all_id"):
            self.errors.append(
                {"status": API_RESPONSE_MSG["PLEASE_PROVIDE_TASK_FOR_EXPORT"]}
            )
        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        self.service_req_data = {
            "auth_instance": request.user,
            "task_list_params": request.query_params,
        }
        resp = ExportTasksService(**self.service_req_data).get_task_list_for_export()
        return resp


class TaskUpdateApi(LoggingMixin, APIView):
    """
    TaskUpdateApi
    usage: this end-point get the task details as per user request status
    path: /api/v1/task/update/
    method: PUT
    Authorization: YES
    request: {
        "task_name":"low update",
        "customer_name": "test Gourav",
        "description": "test",
        "start_date": "",
        "due_date": "",
        "estimate": "3",
        "department": "",
        "topic": "",
        "members": [],
        "status": "",
        "matrix_config_detail": {
            "importance": "High",
            "urgency": "High"
        },
        "task_id": "7bae4f83-b586-4cd0-bfc5-e7715a00bcf2"
    }
    Response: {
        "data": {
            "id": "7bae4f83-b586-4cd0-bfc5-e7715a00bcf2",
            "task_name": "low update",
            "customer_name": "test Gourav",
            "description": "",
            "start_date": "26-08-2022",
            "due_date": "30-08-2022",
            "estimate": "3",
            "notes": "test nodes",
            "comments": null,
            "reminder": "28-08-2022",
            "status": "To-do",
            "department": "yml",
            "topic": "oopsasbsdsds",
            "members": [
                {
                    "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                    "created_at": "2022-08-25T12:34:50.336439Z",
                    "updated_at": "2022-09-07T07:18:22.875772Z",
                    "is_active": true,
                    "first_name": "Sumeet",
                    "last_name": "Singh",
                    "email": "sumeet@gmail.com",
                    "mobile": "8989209090",
                    "isd": 91,
                    "access_status": "allow_to_all",
                    "registration_type": "web",
                    "color_hex_code": null,sudo apt-get install apache2
                    "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                    "color": "e026aa15-ec41-4b0c-aaac-e574b0856ed5",
                    "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                    "auth_user": 7
                },
                {
                    "id": "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                    "created_at": "2022-08-25T12:29:09.245668Z",
                    "updated_at": "2022-08-26T09:05:10.062389Z",
                    "is_active": true,
                    "first_name": "Sameer",
                    "last_name": "Singh",
                    "email": "smaeersharma@gmail.com",
                    "mobile": "8989209090",
                    "isd": null,
                    "access_status": "allow_to_all",
                    "registration_type": "web",
                    "color_hex_code": null,
                    "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
                    "color": "996bfc3d-a329-42a5-9b09-72629716ce43",
                    "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                    "auth_user": 6
                }
            ],
            "task_owner": "Gourav",
            "matrix_type_config": "Priority 7",
            "status_id": "f4f2493b-8108-4f7a-af6f-7d55238f6417",
            "matrix_config_detail": {
                "Importance": "Low",
                "Urgency": "High"
            }
        },
        "success": true,
        "message": "Done"
    }


    #######################################################
    #######################################################
    or delete api
    request :{
    "task_id": "7bae4f83-b586-4cd0-bfc5-e7715a00bcf2",
    "is_deleted": "1"
    }
    response: {
        "data": {
            "is_deleted": true
        },
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def put(self, request):
        """
        get_queryset the user details using token
        """
        if not request.data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "task_req_data": request.data.copy(),
        }
        resp = TaskService(**self.service_req_data).update_task_details()
        return APIResponseParser.response(**resp)


class TaskCommentsApi(LoggingMixin, APIView):
    """
    TaskCommentsApi
    usage: this end-point get the task details as per user request status
    path: /api/v1/task/comments/
    method: POST
    Authorization: YES
    request: {
        "task": "b50bdf31-d280-4b01-abec-90855e30a3c4",
        "comments": "this is good manners task"
    }
    response: {
        "data": {
            "id": "2390e5fc-7c4c-41c7-9088-70b24b5d1cb5",
            "created_at": "2022-09-12T10:37:36.642489Z",
            "updated_at": "2022-09-12T10:37:36.642521Z",
            "is_active": true,
            "comments": "this is good manners task",
            "created_by": null,
            "updated_by": null,
            "task": "b50bdf31-d280-4b01-abec-90855e30a3c4",
            "members": "c7d7d07c-92c8-4f06-9706-54f0c5e9ce07"
        },
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def post(self, request):
        """
        this post method used the user details using token
        """
        if not request.data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "task_req_data": request.data.copy(),
        }
        resp = TaskCommentService(**self.service_req_data).update_task_comments()
        return APIResponseParser.response(**resp)

    def get(self, request):
        """
        TaskCommentsApi
        usage: this end-point get the all comments given by all user
        method: GET
        Authorization: YES
        path: /api/v1/task/comments/?task=b50bdf31-d280-4b01-abec-90855e30a3c4
        response: {
            "data": [
                {
                    "id": "2390e5fc-7c4c-41c7-9088-70b24b5d1cb5",
                    "members": {
                        "id": "c7d7d07c-92c8-4f06-9706-54f0c5e9ce07",
                        "created_at": "2022-09-02T12:59:09.853762Z",
                        "updated_at": "2022-09-06T11:58:44.863961Z",
                        "is_active": true,
                        "first_name": "Sonal",
                        "last_name": "Aggarwal",
                        "email": "sonal@loopmethods.com",
                        "mobile": null,
                        "isd": null,
                        "access_status": "allow_to_all",
                        "registration_type": "android",
                        "color_hex_code": null,
                        "department": "b2996db9-a48b-45b3-8d45-ad6441d3d036",
                        "color": "10795573-c257-4790-8c41-5513c5c3c2b5",
                        "role": "ea01490e-c828-48c8-9cca-e2485d2c3762",
                        "auth_user": 81
                    },
                    "created_at": "2022-09-12T10:37:36.642489Z",
                    "updated_at": "2022-09-12T10:37:36.642521Z",
                    "is_active": true,
                    "comments": "this is good manners task",
                    "created_by": null,
                    "updated_by": null,
                    "task": "b50bdf31-d280-4b01-abec-90855e30a3c4"
                },
                {
                    "id": "e59d119c-810e-4184-a82d-36ef332907be",
                    "members": {
                        "id": "075cd848-46b2-4626-99d7-99db5c6b4af6",
                        "created_at": "2022-09-05T12:53:40.628117Z",
                        "updated_at": "2022-09-12T06:55:41.917952Z",
                        "is_active": true,
                        "first_name": "Parveen",
                        "last_name": "Prajapati",
                        "email": "pp@gmail.com",
                        "mobile": "8898298090",
                        "isd": 91,
                        "access_status": "allow_to_all",
                        "registration_type": "web",
                        "color_hex_code": "#36ce64",
                        "department": "bcce8faa-356f-4547-a562-492ef0ef975c",
                        "color": null,
                        "role": "65ca35d3-9ef0-4bff-8653-a74bdeb2fd74",
                        "auth_user": 91
                    },
                    "created_at": "2022-09-12T10:47:42.568789Z",
                    "updated_at": "2022-09-12T10:47:42.568823Z",
                    "is_active": true,
                    "comments": "yes its working",
                    "created_by": null,
                    "updated_by": null,
                    "task": "b50bdf31-d280-4b01-abec-90855e30a3c4"
                }
            ],
            "success": true,
            "message": "Done"
        }
        """
        self.service_req_data = {
            "auth_instance": request.user,
            "task_req_data": request.query_params,
        }
        resp = TaskCommentService(**self.service_req_data).get_task_comments()
        return APIResponseParser.response(**resp)

    def put(self, request):
        """
        this put method used the update the task values update and delete
        path: /api/v1/task/comments/
        auth: YES
        request: {
            "comment_id":"30ec4dc3-0b01-47cc-a721-adbaa68f5c9e",
            "is_deleted": "1"
        }
        Response: {
            "data": {
                "is_deleted": true
            },
            "success": true,
            "message": "Done"
        }OR
        request: {
            "comment_id":"e6fb14aa-c2ee-4d7d-9e38-e2746c1b6d02",
            "comments": "yeeeeeeeeee"
        }
        Response: {
        "data": {
            "id": "e6fb14aa-c2ee-4d7d-9e38-e2746c1b6d02",
            "members": {
                "id": "83c1983b-bcc1-4015-b876-7ebafe9d71a7",
                "created_at": "2022-09-13T08:47:49.773109Z",
                "updated_at": "2022-09-13T08:47:49.773132Z",
                "is_active": true,
                "first_name": "Sonu",
                "last_name": "Jha",
                "email": "sonujha@loopmethods.com",
                "mobile": "9091090923",
                "isd": 91,
                "access_status": "allow_to_all",
                "registration_type": "web",
                "color_hex_code": "#b03b3b",
                "department": "75e7dd05-f94c-4a1e-b74b-6a1653a497c6",
                "color": null,
                "role": "65ca35d3-9ef0-4bff-8653-a74bdeb2fd74",
                "auth_user": 147
            },
            "created_at": "2022-09-13T10:28:39.048876Z",
            "updated_at": "2022-09-21T12:09:06.730485Z",
            "is_active": true,
            "comments": "yeeeeeeeeee",
            "created_by": null,
            "updated_by": null,
            "task": "76328c60-3921-4ec6-9029-38cbb233df80"
        },
        "success": true,
        "message": "Done"
        }

        """
        if not request.data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "task_req_data": request.data.copy(),
        }
        resp = TaskCommentService(**self.service_req_data).edit_and_delete_task_comments()
        return APIResponseParser.response(**resp)


class TaskImportExcelSheetApi(APIView):
    """
    TaskImportApi
    api get the sample excel and upload details
    path: /api/v1/task/bulk/import/?user_id=40b0b1fa-5faa-43a6-9448-3ec5c796740e
    need to add details
    department
    topic
    member
    request: import_file: media
    response: {
        "data": {
            "exceptions": [],
            "task_list": [
                "aa6a629a-5217-4549-bb58-e78dcc805449",
                "eb4d592e-d5dd-4f04-968e-2f8660f11d2d"
            ]
        },
        "success": true,
        "message": "Task updated successfuly and [] task upload failed"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}
        self.task_req_data = {}
        self.request_not_found = request_not_found()

    def get(self, request):
        """
        this get method used to get the sample sheet
        of import task using excel
        for bulk upload uses
        """
        return ImportExportTaskService(
            auth_instance=request.user, 
            custom_user_id=request.query_params.get('user_id', None)
        ).export_task_sample()

    def post(self, request):
        """
        DepartmentImportSheetApi
        this get method used to get the all topic of as per system logic
        """
        if not request.data:
            return APIResponseParser.response(**self.request_not_found)

        self.task_req_data = request.data
        self.task_req_data._mutable = True

        if not self.task_req_data.get("import_file", None):
            return APIResponseParser.response(
                success=False, message=API_RESPONSE_MSG["IMPORT_FILE_NAME_NOT_FOUND"]
            )

        create_import_file_instance = TaskBulkDataExcelFiles.objects.create(
            file_save_path=self.task_req_data.get("import_file", None)
        )
        print('views--------------------')
        try:
            success, data, msg = ImportExportTaskService(
                excel_sheet_path=create_import_file_instance.file_save_path.path,
                auth_instance=request.user,
                task_req_data=self.task_req_data,
            ).import_task_list()

            if success:
                return APIResponseParser.response(
                    success=True,
                    keyname="data",
                    data=data,
                    message=msg,
                    status_code=status.HTTP_200_OK,
                )
            if success is False:
                return APIResponseParser.response(
                    success=False, message=msg, status_code=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print('EEEEEEEEEEEEEEEEEEEEEEE')
            print("ImportExportService.DoesNotExist: %s" % e)
            return APIResponseParser.response(
                success=False,
                message=MSG["CORRECT_SHEET_ERROR"],
                # message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
