from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from core.api_response_parser import APIResponseParser, request_not_found
from core.messages import API_RESPONSE_MSG, MSG, ITALIAN_MSG
from web_api_service.cognito.aws_cognito_auth import AWSCognito
from web_api_service.helpers.validations import APIValidation
from web_api_service.users.import_export_members import ImportExportMemberService

# import user service
from web_api_service.users.member_service import UserMemberService
from web_api_service.users.services import UserService
from web_api_service.users.team_service import TeamService
from web_api_service.users.user_filter_service import MemberFilterService


class UserDetails(LoggingMixin, APIView):
    """
    UserProfileDetailsApi
    Usage: this endpoint used to get and update the profile details
    path: /api/v1/user/detail/
    method: GET
    Authorization: YES
    Response: {
        "user_details": {
            "id": "7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
            "first_name": "gourav",
            "last_name": "sharma",
            "email": "govind@gmail.com",
            "mobile": "8287694556",
            "mobile_with_isd": "918287694556",
            "isd": 91,
            "profile_picture": null,
            "department": "c5208922-52b0-4e8c-9498-367e9eed09a7",
            "role": "Manager"
        },
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_request_data = {}

    def get(self, request):
        """
        get the user details using token
        """
        user_details_resp = UserService.get_user_details(request.user)
        return APIResponseParser.response(**user_details_resp)


class UserDetailsUpdate(APIView):
    """
    UserDetailsUpdateApi
    Usage: this endpoint used to update the profile details with media file.
    path: /api/v1/user/detail/update/
    method: PUT
    Authorization: YES
    Content-Type: MultiPartParser, FormParser
    request_data :
        first_name:Gourav
        last_name:Sharma
        mobile:8750752954
    Response: {
        "user_details": {
            "id": "7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
            "first_name": "Gourav",
            "last_name": "Sharma",
            "email": "govindsharma@gmail.com",
            "mobile": "8750752954",
            "mobile_with_isd": "918287694556",
            "isd": 91,
            "profile_picture": null,
            "department": "c5208922-52b0-4e8c-9498-367e9eed09a7"
        },
        "success": true,
        "message": "Done"
    }
    """

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    # permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_request_data = {}

    def put(self, request):
        """
        update the user details using token
        """
        self.user_request_data = request.data
        self.user_request_data._mutable = True
        resp = UserService.update_user_details(request.user, self.user_request_data)
        return APIResponseParser.response(**resp)


class LoginUser(LoggingMixin, APIView):
    """
    LoginUserApi
    usage: this endpoint used to login user with generate JWT token.
    path: /api/v1/user/login/
    method: POST
    request: {
        "email":"govind@gmail.com",
        "password": "Admin@123"
    }
    Response: {
        "user_tokens": {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MDkxOTQ4NSwiaWF0IjoxNjYwODMzMDg1LCJqdGkiOiI2NjdiOGZhZDk2MTg0Yjc1ODg1ZDA5MmNmM2Q5NDM1MCIsInVzZXJfaWQiOjJ9.3mtyiBLvTAuqWua3mpdp7vHOm1U9Y90_li_YWtm_Ows",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYwODMzMzg1LCJpYXQiOjE2NjA4MzMwODUsImp0aSI6ImIzNGMyOWVlZDdlMzQ5M2Q4NzBhZGQwY2VmZjVmMmUyIiwidXNlcl9pZCI6Mn0.WlIrnFTzsgDTA8HdCHGXQkMpZBdZ1mubOLgfkTuuzEI"
        },
        "success": true,
        "message": "Done"
    }
    """

    def post(self, request):
        """
        get the user details using token
        """
        if not request.data:
            return APIResponseParser.response(
                success=False, message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"]
            )
        if not request.data.get("email", None):
            try:
                if request.data.get("language", None) == "ENG":
                    post_email_msg = API_RESPONSE_MSG["PLEASE_POST_EMAIL"]
                else:
                    post_email_msg = ITALIAN_MSG["PLEASE_POST_EMAIL"]
            except Exception as e:
                print(e)
                post_email_msg = API_RESPONSE_MSG["PLEASE_POST_EMAIL"]
            return APIResponseParser.response(success=False, message=post_email_msg)
        if not request.data.get("password", None):
            try:
                if request.data.get("language", None) == "ENG":
                    post_password_msg = API_RESPONSE_MSG["PLEASE_PROVIDE_PASSWORD"]
                else:
                    post_password_msg = ITALIAN_MSG["PLEASE_PROVIDE_PASSWORD"]
            except Exception as e:
                print(e)
                post_password_msg = API_RESPONSE_MSG["PLEASE_PROVIDE_PASSWORD"]

            return APIResponseParser.response(success=False, message=post_password_msg)
        api_validation_instance = APIValidation()
        if not api_validation_instance.email_validation(
            request.data.get("email", None)
        ):
            try:
                if request.data.get("language", None) == "ENG":
                    _msg = API_RESPONSE_MSG["ENTER_VALID_EMAIL"]
                else:
                    _msg = ITALIAN_MSG["ENTER_VALID_EMAIL"]
            except Exception as e:
                print(e)
                _msg = API_RESPONSE_MSG["ENTER_VALID_EMAIL"]

            return APIResponseParser.response(success=False, message=_msg)
        return APIResponseParser.response(**UserService().login(request.data))


class MemberUserCreateApi(LoggingMixin, APIView):
    """LoginUser api
    path: /api/v1/user/create/
    method: POST
    request: {
        "first_name": "Gourav",
        "last_name": "sharma",
        "email": "Gourav@gmail.com",
        "mobile": "8989209090",
        "registration_type": "web",
        "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd", # department id
        "level": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b", # role id (member/manager/admin)
        "color": "#ffffh",
        "access_status": "Y" # Y/N
    }
    Response: {
        "data": {
            "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
            "created_at": "2022-08-25T12:34:50.336439Z",
            "updated_at": "2022-08-25T12:34:50.336458Z",
            "is_active": true,
            "first_name": "Sumeet",
            "last_name": "Singh",
            "email": "sumeet@gmail.com",
            "mobile": "8989209090",
            "mobile_with_isd": null,
            "isd": null,
            "access_status": "allow_to_all",
            "registration_type": "web",
            "device_id": null,
            "imei_no": null,
            "device_name": null,
            "code": null,
            "designation": null,
            "profile_picture": null,
            "country": null,
            "state": null,
            "city": null,
            "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
            "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
            "auth_user": 7
        },
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.member_req_data = {}

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

        if not request.data.get("first_name"):
            self.errors.append(
                {"first_name": API_RESPONSE_MSG["PLEASE_PROVIDE_FIRST_NAME"]}
            )
        if not request.data.get("last_name"):
            self.errors.append(
                {"last_name": API_RESPONSE_MSG["PLEASE_PROVIDE_LAST_NAME"]}
            )
        if not request.data.get("email"):
            self.errors.append({"email": API_RESPONSE_MSG["PLEASE_PROVIDE_EMAIL"]})
        if not request.data.get("department"):
            self.errors.append(
                {"department": API_RESPONSE_MSG["PLEASE_PROVIDE_DEPARTMENT_ID"]}
            )
        if not request.data.get("level"):
            self.errors.append({"level": API_RESPONSE_MSG["PLEASE_PROVIDE_LEVEL_ID"]})
        # if not request.data.get('color'):
        #     self.errors.append({'color': API_RESPONSE_MSG['PLEASE_PROVIDE_COLOR']})

        api_validation_instance = APIValidation()
        if not api_validation_instance.email_validation(
            request.data.get("email", None)
        ):
            self.errors.append({"email": API_RESPONSE_MSG["ENTER_VALID_EMAIL"]})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.member_req_data = {
            "auth_instance": request.user,
            "member_req_data": request.data.copy(),
        }
        resp = UserMemberService(**self.member_req_data).create_member_detail()
        return APIResponseParser.response(**resp)


class MemberUserListApi(LoggingMixin, APIView):
    """UserDetailsMembers api
    path: /api/v1/user/members/
    method: GET
    Authorization: YES
    Response: {
        "members": [
            {
                "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                "color": "#00FF00",
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
                "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "auth_user": 7
            },
            {
                "id": "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                "color": "#FFCCCB",
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
                "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "auth_user": 6
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_req_data = {}

    def get(self, request):
        """
        get the user details using token
        """
        self.member_req_data = {
            "auth_instance": request.user,
        }
        resp = UserMemberService(**self.member_req_data).member_detail_list()
        return APIResponseParser.response(**resp)


class UpdateTaskMemberUserListApi(LoggingMixin, APIView):
    """UserDetailsMembers API
    path: /api/v1/user/members/task/update/?task_id=a946de3e-6329-4b9d-b28a-4bc0ead8c23a
    method: GET
    Authorization: YES
    Response: {
        "members": [
            {
                "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                "color": "#00FF00",
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
                "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "auth_user": 7
            },
            {
                "id": "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                "color": "#FFCCCB",
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
                "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "auth_user": 6
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_req_data = {}

    def get(self, request):
        """
        get the user details using token
        """
        self.member_req_data = {
            "auth_instance": request.user,
            "query_params": request.query_params
        }
        resp = UserMemberService(**self.member_req_data).member_detail_list_for_task_update()
        return APIResponseParser.response(**resp)


class ActiveMemberUserListApi(LoggingMixin, APIView):
    """ActiveMemberUserListApi api
    path: /api/v1/user/active/members/
    method: GET
    Authorization: YES
    Response: {
        "members": [
            {
                "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                "color": "#00FF00",
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
                "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "auth_user": 7
            },
            {
                "id": "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                "color": "#FFCCCB",
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
                "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "auth_user": 6
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_req_data = {}

    def get(self, request):
        """
        get the user details using token
        """
        self.member_req_data = {
            "auth_instance": request.user,
        }
        resp = UserMemberService(**self.member_req_data).active_member_detail_list()
        return APIResponseParser.response(**resp)


class MemberUserListAddTaskApi(LoggingMixin, APIView):
    """MemberUserListAddTaskApi api
    path: /api/v1/user/members/add/task/?department=
    method: GET
    Authorization: YES
    Response: {
        "members": [
            {
                "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                "color": "#00FF00",
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
                "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "auth_user": 7
            },
            {
                "id": "af2cac3a-bec7-44dc-a0b7-5e3c33323db2",
                "color": "#FFCCCB",
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
                "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
                "auth_user": 6
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_req_data = {}
        self.errors = []

    def get(self, request):
        """
        get the user details using token
        """
        if not request.query_params:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not request.query_params.get("department"):
            self.errors.append(
                {"department": API_RESPONSE_MSG["PLEASE_PROVIDE_DEPARTMENT_ID"]}
            )

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.member_req_data = {
            "auth_instance": request.user,
            "query_params": request.query_params,
        }
        resp = UserMemberService(**self.member_req_data).member_list_by_department()
        return APIResponseParser.response(**resp)


class TeamMemberDetailsApi(LoggingMixin, APIView):
    """TeamMemberDetailsApi
    path: /api/v1/team/member/detail/?member_id=e055dbae-13c9-4ea8-83a6-90f806cda1a8
    Authorization: YES
    method: GET
    Response:{
        "data": {
            "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
            "color": "#00FF00",
            "role": "Member",
            "department": "Super system g",
            "team_association": [
                {
                    "team_name": "test team one"
                },
                {
                    "team_name": "test team one mores"
                },
                {
                    "team_name": "test team one more"
                }
            ],
            "created_at": "2022-08-25T12:34:50.336439Z",
            "updated_at": "2022-08-26T09:04:51.908585Z",
            "is_active": true,
            "first_name": "Sumeet",
            "last_name": "Singh",
            "email": "sumeet@gmail.com",
            "mobile": "8989209090",
            "access_status": "allow_to_all",
            "registration_type": "web",
            "auth_user": 7
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

        if not request.query_params.get("member_id"):
            self.errors.append(
                {"member_id": API_RESPONSE_MSG["PLEASE_PROVIDE_MEMBER_ID"]}
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
            "query_params": request.query_params,
        }
        resp = TeamService(**self.service_req_data).team_member_details()
        return APIResponseParser.response(**resp)


class TeamDetailApi(LoggingMixin, APIView):
    """TeamDetailApi
    path: /api/v1/team/
    Authorization: YES
    method: POST
        request: {
        "team_name": "test team one",
        "department":"fc18e5f4-c1ca-41d2-b750-ae2377368545",
        "members":["e055dbae-13c9-4ea8-83a6-90f806cda1a8", "63dfc90d-513d-4dbc-a1e0-5cd2964e719b"]
    }
    Response:{
        "data": {
            "id": "0bc5ac60-77f8-48ba-9dc1-1b2683d81f4a",
            "created_at": "2022-08-30T06:47:02.601665Z",
            "updated_at": "2022-08-30T06:47:02.601702Z",
            "is_active": true,
            "team_name": "test team one",
            "access_status": "allow_to_all",
            "created_by": null,
            "updated_by": null,
            "department": "fc18e5f4-c1ca-41d2-b750-ae2377368545",
            "members": [
                "63dfc90d-513d-4dbc-a1e0-5cd2964e719b",
                "e055dbae-13c9-4ea8-83a6-90f806cda1a8"
            ]
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
        path: /api/v1/team/
        method: GET
        Authorization: YES
        response: {
        "data": [
            {
                "id": "1a2d24b8-ed68-4258-b9eb-7ad5f6f65b96",
                "department": "system adminstratator",
                "created_at": "2022-08-30T07:16:46.854454Z",
                "updated_at": "2022-08-30T07:16:46.854474Z",
                "is_active": true,
                "team_name": "test team one more",
                "access_status": "allow_to_all",
                "created_by": null,
                "updated_by": null,
                "user": "7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
                "members": [
                    "63dfc90d-513d-4dbc-a1e0-5cd2964e719b",
                    "e055dbae-13c9-4ea8-83a6-90f806cda1a8"
                ]
            },
            {
                "id": "b3dbd811-ca5e-4194-8a7c-a12d731964fd",
                "department": "system adminstratator",
                "created_at": "2022-08-30T07:18:17.023609Z",
                "updated_at": "2022-08-30T07:18:17.023640Z",
                "is_active": true,
                "team_name": "test team one mores",
                "access_status": "allow_to_all",
                "created_by": null,
                "updated_by": null,
                "user": "7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
                "members": [
                    "63dfc90d-513d-4dbc-a1e0-5cd2964e719b",
                    "e055dbae-13c9-4ea8-83a6-90f806cda1a8"
                ]
            }
        ],
        "success": true,
        "message": "Done"
        }
        """
        self.service_req_data = {
            "auth_instance": request.user,
        }
        resp = TeamService(**self.service_req_data).team_detail_list()
        return APIResponseParser.response(**resp)

    def post(self, request):
        """
        this post method used to add team in system
        """
        if not request.data:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not request.data.get("team_name"):
            self.errors.append(
                {"team_name": API_RESPONSE_MSG["PLEASE_PROVIDE_TEAM_NAME"]}
            )
        if not request.data.get("department"):
            self.errors.append(
                {"department": API_RESPONSE_MSG["PLEASE_PROVIDE_LAST_NAME"]}
            )

        # all m2m relation fields
        if not request.data.get("members"):
            self.errors.append({"members": API_RESPONSE_MSG["PROVIDE_MEMBERS"]})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "team_req_data": request.data.copy(),
        }
        resp = TeamService(**self.service_req_data).create_team_detail()
        return APIResponseParser.response(**resp)


class MemberActivateDeactivateApi(LoggingMixin, APIView):
    """MemberActivateDeactivateApi
    path: /api/v1/user/members/active/?is_active=1&member_id=e1c0f49f-590d-40c5-a550-be7e677280bf
    Authorization: YES
    method: GET
    Response:{
        "data": {
            "is_active": "1"
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

        if not request.query_params.get("is_active"):
            self.errors.append(
                {"is_active": API_RESPONSE_MSG["PLEASE_PROVIDE_ACTIVE_STATUS"]}
            )
        if not request.query_params.get("member_id"):
            self.errors.append(
                {"member_id": API_RESPONSE_MSG["PLEASE_PROVIDE_MEMBER_ID"]}
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
            "query_params": request.query_params,
        }
        resp = UserMemberService(**self.service_req_data).member_activate_deactivate()
        return APIResponseParser.response(**resp)


class TeamActivateDeactivateApi(LoggingMixin, APIView):
    """TeamActivateDeactivateApi
    path: /api/v1/team/active/?is_active=1&team_id=1a2d24b8-ed68-4258-b9eb-7ad5f6f65b96
    Authorization: YES
    method: GET
    Response:{
        "data": {
            "is_active": "1"
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

        if not request.query_params.get("is_active"):
            self.errors.append(
                {"is_active": API_RESPONSE_MSG["PLEASE_PROVIDE_ACTIVE_STATUS"]}
            )
        if not request.query_params.get("team_id"):
            self.errors.append({"team_id": API_RESPONSE_MSG["PLEASE_PROVIDE_TEAM_ID"]})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "query_params": request.query_params,
        }
        resp = TeamService(**self.service_req_data).team_activate_deactivate()
        return APIResponseParser.response(**resp)


class TeamMemberListApi(LoggingMixin, APIView):
    """TeamMemberListApi
    path: /api/v1/team/member/list/?team_id=1a2d24b8-ed68-4258-b9eb-7ad5f6f65b96
    Authorization: YES
    method: GET
    Response:{
        "data": [
            {
                "id": "63dfc90d-513d-4dbc-a1e0-5cd2964e719b",
                "color": "#0000FF",
                "role": "Member",
                "department": "Super system g",
                "created_at": "2022-08-25T12:39:53.182576Z",
                "updated_at": "2022-08-26T09:05:33.280777Z",
                "is_active": true,
                "first_name": "Manish",
                "last_name": "Singh",
                "email": "manish@gmail.com",
                "mobile": "8989209090",
                "access_status": "self_only",
                "registration_type": "web",
                "auth_user": 8
            },
            {
                "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                "color": "#00FF00",
                "role": "Member",
                "department": "Super system g",
                "created_at": "2022-08-25T12:34:50.336439Z",
                "updated_at": "2022-08-26T09:04:51.908585Z",
                "is_active": true,
                "first_name": "Sumeet",
                "last_name": "Singh",
                "email": "sumeet@gmail.com",
                "mobile": "8989209090",
                "access_status": "allow_to_all",
                "registration_type": "web",
                "auth_user": 7
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
        get the team details using token
        """

        if not request.query_params:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not request.query_params.get("team_id"):
            self.errors.append({"team_id": API_RESPONSE_MSG["PLEASE_PROVIDE_TEAM_ID"]})

        if self.errors:
            return APIResponseParser.response(
                success=False,
                message=API_RESPONSE_MSG["ERRORS"],
                errors=self.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self.service_req_data = {
            "auth_instance": request.user,
            "query_params": request.query_params,
        }
        resp = TeamService(**self.service_req_data).team_members()
        return APIResponseParser.response(**resp)


class MemberSearchApi(LoggingMixin, APIView):
    """MemberSearchApi
    usage: this endpoint used to get member details list.
    path: /api/v1/team/member/search/?q=goura
    Authorization: YES
    method: GET
    response:{
        "data": [
            {
                "id": "7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
                "color": "",
                "role": "Manager",
                "department": "IT",
                "team_association": [],
                "created_at": "2022-08-18T10:28:39.809157Z",
                "updated_at": "2022-08-26T09:05:24.891647Z",
                "is_active": true,
                "first_name": "Gourav",
                "last_name": "Sharma",
                "email": "govind@gmail.com",
                "mobile": "8750752954",
                "access_status": "self_only",
                "registration_type": "web",
                "color_hex_code": null,
                "auth_user": 2
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
            "auth_instance": request.user,
            "query_params": request.query_params,
        }

        resp = MemberFilterService(**self.service_req_data).search_member_list()
        return APIResponseParser.response(**resp)


class MemberFilterApi(LoggingMixin, APIView):
    """
    MemberFilterApi
    usage: this endpoint used to get member details using filter reqoest.
    path: /api/v1/team/member/filter/
    Authorization: YES
    method: POST
    request: {
        "department": "46c9d716-cdd0-40d8-8c2e-810a6f9fb8dd",
        "isd": "91"
    }
    response:{
        "data": [
            {
                "id": "e055dbae-13c9-4ea8-83a6-90f806cda1a8",
                "color": "",
                "role": "Member",
                "department": "Super system g",
                "team_association": [
                    {
                        "team_name": "test team one"
                    },
                    {
                        "team_name": "test team one mores"
                    },
                    {
                        "team_name": "test team one more"
                    }
                ],
                "created_at": "2022-08-25T12:34:50.336439Z",
                "updated_at": "2022-09-07T07:18:22.875772Z",
                "is_active": true,
                "first_name": "Sumeet",
                "last_name": "Singh",
                "email": "sumeet@gmail.com",
                "mobile": "8989209090",
                "access_status": "allow_to_all",
                "registration_type": "web",
                "color_hex_code": null,
                "auth_user": 7
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

    def post(self, request):
        """
        TopicListApi
        this get method used to get the all topic of as per system logic
        """

        self.service_req_data = {
            "auth_instance": request.user,
            "member_req_data": request.data.copy(),
        }
        resp = MemberFilterService(**self.service_req_data).filter_member_list()
        return APIResponseParser.response(**resp)


class MemberUpdateApi(LoggingMixin, APIView):
    """
    MemberUpdateApi
    usage: this endpoint used to update the member details using member id.
    path: /api/v1/team/member/update/
    Authorization: YES
    method: POST
    request:{
        "member_id": "f575a5d2-83c2-4370-9e20-6329f3e380dd",
        "first_name": "khalids",
        "last_name": "siddiqui",
        "mobile": "8989209090",
        "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
        "color_hex_code": "#00FF00"
    }
    response:{
        "data": {
            "id": "f575a5d2-83c2-4370-9e20-6329f3e380dd",
            "created_at": "2022-08-30T06:45:09.447903Z",
            "updated_at": "2022-09-07T12:31:45.296747Z",
            "is_active": true,
            "first_name": "khalids",
            "last_name": "siddiqui",
            "email": "khalid123@gmail.com",
            "mobile": "8989209090",
            "isd": null,
            "access_status": "allow_to_all",
            "registration_type": "web",
            "color_hex_code": "#00FF00",
            "department": "fb7b6de9-b1de-49fb-b87c-6254663b92d2",
            "color": null,
            "role": "d07d4948-e7e0-4d3c-989e-f1aaa89d6f8b",
            "auth_user": 38
        },
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.service_req_data = {}

    def put(self, request):
        """
        this put method used to get the all topic of as per system logic
        """

        self.service_req_data = {
            "auth_instance": request.user,
            "team_req_data": request.data.copy(),
        }
        resp = TeamService(**self.service_req_data).update_team_member()
        return APIResponseParser.response(**resp)


class UserStickyNotesApi(LoggingMixin, APIView):
    """
    UserStickyNotesApi
    usage: this endpoint used to add and get the sticky notes
    path: /api/v1/user/sticky/notes/
    Authorization: YES
    method: PUT/GET
        request:{
            "note": "fadshkglhasklfhgkljajsdhg"
        }
    response:{
        "data": {
            "id": "b75c0721-a58e-4e9e-8a09-f32872dbe906",
            "created_at": "2022-09-12T05:28:27.767487Z",
            "updated_at": "2022-09-12T05:28:27.767519Z",
            "is_active": true,
            "note": "fadshkglhasklfhgkljajsdhg",
            "created_by": null,
            "updated_by": null,
            "user": "075cd848-46b2-4626-99d7-99db5c6b4af6"
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
        this get method used to get the user sticky notes from databases
        """
        self.service_req_data = {
            "auth_instance": request.user,
            "query_params": request.query_params,
        }
        resp = TeamService(**self.service_req_data).get_sticky_note()
        return APIResponseParser.response(**resp)

    def put(self, request):
        """
        this put method used to get the all topic of as per system logic
        """

        self.service_req_data = {
            "auth_instance": request.user,
            "team_req_data": request.data.copy(),
        }
        resp = TeamService(**self.service_req_data).update_sticky_note()
        return APIResponseParser.response(**resp)


class MemberSampleSheetApi(APIView):
    """MemberSampleSheetApi
    usage: this endpoint used to download department sample sheet.
    path: /api/v1/user/sample/sheet/?user_id=40b0b1fa-5faa-43a6-9448-3ec5c796740e
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
            "auth_instance": request.user,
            "query_params": request.query_params
        }
        return ImportExportMemberService(**self.service_req_data).export_member_sample()


class MemberImportExcelSheetApi(APIView):
    """MemberImportExcelSheetApi
    usage: this endpoint used to import the excel sheet of member
    path: /api/v1/user/import/
    Authorization: YES
    method: POST
    1: all member uploaded successfuly
    2: 5 done and 5 already exist
    3: all user already exists
    request:
        import_file: media_file
    response:{
        "data": {
            "new_created_ids": [
                {
                    "id": "540942ed-0205-4ddb-be2c-bf59c145d6a1",
                    "email": "seemarani@gmail.com"
                },
                {
                    "id": "f34caade-d90a-415a-812a-60fb29e0080e",
                    "email": "ravishkumar@gmail.com"
                }
            ],
            "data_pool_list": [
                "38263dfb-a6ef-44ad-a5dc-f101dee2757f"
            ],
            "display_alery_key": "1/2/3"
        },
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.member_req_data = {}
        self.service_req_data = {}
        self.request_not_found = request_not_found()

    def post(self, request):
        """
        DepartmentImportSheetApi
        this get method used to get the all topic of as per system logic
        """
        if not request.data:
            return APIResponseParser.response(**self.request_not_found)

        self.member_req_data = request.data
        self.member_req_data._mutable = True

        if not self.member_req_data.get("import_file", None):
            return APIResponseParser.response(
                success=False, message=API_RESPONSE_MSG["IMPORT_FILE_NAME_NOT_FOUND"]
            )

        try:
            self.service_req_data = {
                "auth_instance": request.user,
                "member_req_data": self.member_req_data,
            }
            resp = ImportExportMemberService(
                **self.service_req_data
            ).import_member_list()
            return APIResponseParser.response(**resp)
        except Exception as e:
            print("ImportExportService.DoesNotExist: %s" % e)
            return APIResponseParser.response(
                success=False,
                # message='please resolved  %s' % str(e),
                message=MSG["CORRECT_SHEET_ERROR"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class CognitoUserLoginApi(APIView):
    """MemberImportExcelSheetApi
    usage: this endpoint used to import the excel sheet of member
    path: /api/v1/user/cognito/login/
    Authorization: YES
    method: POST
    1: all member uploaded successfuly
    2: 5 done and 5 already exist
    3: all user already exists
    request:{
        "username": "raja@gmail.com",
        "password": "Admin@123"
    }
    response:{
        "aws_cognito_data": {
            "ChallengeParameters": {},
            "AuthenticationResult": {
                "AccessToken": "eyJraWQiOiJjVU1XWnIrakVBY1lwRUhlMnNVelpESmdEZFhQd2NzQ0pwVjM4NzBydnh3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9HbjdENzd6bXciLCJjbGllbnRfaWQiOiIya2NocW1wb3RvNmswNmFrOXY5MzY4ajQ4aiIsIm9yaWdpbl9qdGkiOiJhZTJlY2QwZS1hZTFjLTRlMWUtOWZkOS02ZjE5NmRkYmM1NjUiLCJldmVudF9pZCI6IjA1NjAzOGQzLTZlOTYtNGI4YS1hM2Y2LTM1M2MyOWJmZWIwYiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2NzA0ODc5ODIsImV4cCI6MTY3MDQ5MTU4MiwiaWF0IjoxNjcwNDg3OTgyLCJqdGkiOiJjYzk0MTc2ZC0yMDFlLTRjOWUtOTlhMy1kYTQ3N2ViN2Y0ZGQiLCJ1c2VybmFtZSI6IjA0YjU1Mzg3LTMyMzEtNDIyOC04NjM1LWM2MGJmMmVkYTg2NyJ9.ZB98ch26IWSuEqfXlxbH0mBnr94O157A4Q9tVAr7iXtFBrCNlKvNUI5yaYu5rAONICfvwRPwWXtZjRNhiIWnMHWkcflasJxQv54e0XrTuq03xaQ8isUtUBwlc4D3jZTwXD6Vn6_1SX5KFNybE7ALOm5hv7zzNpP-aQvZA4Dv5eM4lzPR68EGTiXNWybev2ryREIEiR25-ByckftmW2BzGYwigHlCLGc6u6dlQPYyBsfwmpIGowtOQ3l5IeNJK-UHno4Zyajwd1AqvKlcqemjlKLs-c6filP1tB6WvfRh98RKRVqV-ErKRF2T77dXjF86rhgvkcZC1vaYJgpkPxqcqQ",
                "ExpiresIn": 3600,
                "TokenType": "Bearer",
                "RefreshToken": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.Gvvr_QXOqTjvPUHOENsL5yekD6sNUD96Nj3Vs24_kKkNN45m5KLFyq1uAmxoToJZoGRTcjclIe7UsjolhmsFWFVNKUC9LjVUPpZt_8DC9edriczEm6807ppg14uELQgLpEMQNWg66rOiqD2XVXfJ-6dqMtgy5665G_rrLBCNvrdILBB2bs2ddqjn-KueWYAsNlmCi1o2VhOoreHNXYD4WaoEwvG0TENxYa2XmQCZAJqUgU9xyXNNRGf-iQoaOOEEn1sz4DoRBRZ--DrjFoJq1iDRef0PhJFG0e50uJ6EeXWu_ppimQtd6RupU2a-ozpbdZ0eGxvS5i6URGdC4hOuHg.FpI9SHNDHarUvYSu.w9ZIdb1H69NOvHqmQh9h-Yv-BcCGEOPyEczWPj3UAEQJzL4BtUqq-HUWmBrcQqGbM7BBDKbKk1rkPC-IUJn2IDwqE7sFCU8kWzDOHRrsBPdTSID8mDm_l4JkIzkenm5VugxAdiSRgZRKKOgYxV9HA16hAMqfo02Q6RvIcUSi2XhQRVt5hshskcMvAFNU7k0h8lhssclsfR-4FOICtbRF_7npRMk4XUaZtJKdQj0iiFJlpvikIvIJJLGefCOcBPcV9OTJUjDV2VQr2t5PI0HShzd0sKPoscfweysyC6bijTWrVSA0ciYzo1fDegZr8F1JnRjqxZL7xH8ppKIB6Wq9hTkI5Ha8at-KTX3-GDOSnadXVUJMVFobJvDyTMGu_Uhn8fp_oW2tw7yJq8N7GAW4NbH-LkuJdAddX9mFdHUfczrBPDUoxBl34yVLfksOulR67M9NzAJEJIpOupmax4hKv828INtSqVhrSbJqqNkdTlVSFFSNFmaaE0g1ZGdKyDhcqiQtcL1GK-0cAJNrfngBsVBlzEV-xVxRQ4OERQ3keB_KbxPcu1q5dfCycfvnxEzIDUd1e1xKKTJGyyfk2trHl5SeQs-7sm9brnF2D0yW3xQrxChMbuipf9eBVvCkDKhb9FcrtEdrkrjryIhr64B3jOvWKpI6LWUqFoMl48aJ3F0FkA24bBNJrVNcSBPCDVVopbFOAL79grkkkpT4DLTeybSNh2Kgw32uCRpyhAdeLxMBXCQaRs0rjw20DWKbrnZg7BY-sAeHqmTTdn_qod8N8uZaRBOJoHEhzdyoAe1x3LgvkqZ6j23gK0BIufjsccR7nMl4TvEqHsRzRPXT6qYBfiD_gmmDHnPPK7m8E3EHJkavzbJPrut_uNHWA2Tdnu_f9ytmDkcAfrw5T02hFydeC85g1OT39LxHUOTX00THqpt81ia8lr6J8t0Q53I9o-LjTw_Jr3tNXCYPAj6iyiTJQQxpCZSIJkB6LBrp1svI3uq_tFvB81J6LgZTuRnzcOx_H4tZIYlJGJawgvkI_UubzVmQliAGLDRcXoP66adf6rwayopNXXkKrcdofvwZo-MST8fzYPSaaPLRpEaqUtmYloZmjVrOgnLnHmevNIV8VMEYPGcpWUDnaWdKqy7Q66e1JxMdQ7JKgBn30WXdmudAnMR13lukXY2D1uewjCgKqytAAe7IaOnPWwpvYJWzkq4tbFcA2kTvfU8MY2lDwH2mPXnZlVHzuGVRu9GeMYONA91e81FSY_f_OreRJCjRRzVMIjbCJPBp0E2B3VqwfgsD-IGpjPFEaNVtNXR9zajDFHmyEJR_jZETTFS07I4.x5FpRLokroKzOgpkVJ45qw",
                "IdToken": "eyJraWQiOiJQMDhLaENhRTlyOHU0MGVRc2RLOTNia0FLZ0xhZFhKREIyYThSdDBpbm1JPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS13ZXN0LTEuYW1hem9uYXdzLmNvbVwvZXUtd2VzdC0xX0duN0Q3N3ptdyIsInBob25lX251bWJlcl92ZXJpZmllZCI6ZmFsc2UsImNvZ25pdG86dXNlcm5hbWUiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJnaXZlbl9uYW1lIjoiQWRpbCBSYWphIiwib3JpZ2luX2p0aSI6ImFlMmVjZDBlLWFlMWMtNGUxZS05ZmQ5LTZmMTk2ZGRiYzU2NSIsImF1ZCI6IjJrY2hxbXBvdG82azA2YWs5djkzNjhqNDhqIiwiZXZlbnRfaWQiOiIwNTYwMzhkMy02ZTk2LTRiOGEtYTNmNi0zNTNjMjliZmViMGIiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY3MDQ4Nzk4MiwicGhvbmVfbnVtYmVyIjoiKzkxNjQ1NjQ1NjQ1NiIsImV4cCI6MTY3MDQ5MTU4MiwiaWF0IjoxNjcwNDg3OTgyLCJmYW1pbHlfbmFtZSI6IkR1bW15IGZhbWlseSBOYW1lIiwianRpIjoiZDY2YTVhNWEtMjUyOS00NDkxLWI1MDAtM2UzN2MwZGI0NjYxIiwiZW1haWwiOiJyYWphQGdtYWlsLmNvbSJ9.H7jc76O8TnPKg_KHPCXd13U8Jk5a8ujceGvsy3Riul0TbRUW2NE4ba0atPDgzG7mdBSWvXXciHpcQ55n9zUwKgh_jv8EvItYwFj1ntFnZd_gk1eMzo-oit-oXOCUInQrg9_QSudE8kzOpyuNuhiJOMCBIht6kLnoHR40VoCHTCI_u9SBeciahL3u2MxnRduR5GDrwqQAAnU4ZO-diheKTQQyidfOaDp2N4PplRsstKPlxM4Lot62p2gVS2evipMLzOeMWANPo-mu5T3giGZNyznWEzesiLg80M-c4aYRMAAzvnY5n_fi7QfzAuXDF98aMmt-AYkutLOn7l6ebfvJcA"
            },
            "ResponseMetadata": {
                "RequestId": "056038d3-6e96-4b8a-a3f6-353c29bfeb0b",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "date": "Thu, 08 Dec 2022 08:26:22 GMT",
                    "content-type": "application/x-amz-json-1.1",
                    "content-length": "4232",
                    "connection": "keep-alive",
                    "x-amzn-requestid": "056038d3-6e96-4b8a-a3f6-353c29bfeb0b"
                },
                "RetryAttempts": 0
            }
        },
        "success": true,
        "message": "Done"
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []
        self.member_req_data = {}
        self.service_req_data = {}
        self.request_not_found = request_not_found()

    def post(self, request):
        """
        DepartmentImportSheetApi
        this get method used to get the all topic of as per system logic
        """
        if not request.data:
            return APIResponseParser.response(**self.request_not_found)

        self.member_req_data = request.data
        # self.member_req_data._mutable = True
        try:
            aws_cognito_response = AWSCognito(
                username=request.data.get("username")
            ).authenticate_and_get_token(request.data.get("password"))
            api_response_dict = {
                "success": True,
                "keyname": "aws_cognito_data",
                "data": aws_cognito_response,
                "message": API_RESPONSE_MSG["DONE"],
                "status_code": status.HTTP_200_OK,
            }
            return APIResponseParser.response(**api_response_dict)
        except Exception as e:
            print("CognitoUserLoginApi.DoesNotExist: %s" % e)
            return APIResponseParser.response(
                success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST
            )
