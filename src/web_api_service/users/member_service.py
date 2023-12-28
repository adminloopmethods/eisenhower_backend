import phonenumbers
from rest_framework import status

from configuration.models import Departments
from core.api_response_parser import bad_request_response
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.constants import ACCESS_STATUS
from core.messages import MSG, ITALIAN_MSG
from core.serializer_getter import SerializerManipulationService
from user.models import CustomUsers
from user.models import UserMemberMapping
from web_api_service.cognito.aws_cognito_auth import AWSCognito
from web_api_service.helpers.all_config_func import (
    already_exist_check,
    get_user_instance,
    get_language_uuid,
)
from web_api_service.tasks.serializers import TaskDetailSerializer, \
    UpdateTaskDetailSerializerForMembers

# import member serializers
from web_api_service.users.serializers import (
    GetMemberDetailSerializer,
    MemberSerializer,
    MemberDetailSerializer,
    UserMemberMappingByDepartmentSerializer,
)
from web_api_service.users.serializers import UserMemberMappingSerializer
from web_api_service.users.services import UserService

from web_api_service.helpers.all_config_func import (
    get_task_instance,
    get_member_details_using_member_id,
)


class UserMemberService:
    """
    all ConfigService
    create_topic_detail
    """

    def __init__(self, **kwargs):
        self.department_master_data = []
        self.auth_instance = kwargs.get("auth_instance", None)
        self.member_req_data = kwargs.get("member_req_data", None)
        self.department_id_list = []
        self.user_id_list = []
        self.final_response = final_response()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self.topic_master_data = []
        self.member_user_data = []
        self.query_params = kwargs.get("query_params", None)
        self.member_auth_instance = None
        self._password = "Admin@123"
        self._email = None
        self._first_name = ""
        self._last_name = ""
        self._is_cognito_user = False
        self.cognito_response_data = None

    @staticmethod
    def split_given_name(given_name):
        """
        split_given_name
        split the name for using
        divide the first name and last name
        """
        if given_name is None:
            return None, None

        _given_name_list = given_name.split(" ")

        return (
            _given_name_list[0] if len(_given_name_list) > 0 else "",
            _given_name_list[1] if len(_given_name_list) > 1 else "",
        )

    def split_mobile_number(self, mobile_no):
        """
        split_mobile_number
        """
        if mobile_no is None:
            return None, None

        try:
            _my_number = phonenumbers.parse(str(mobile_no))
            if _my_number:
                return str(_my_number.country_code), str(_my_number.national_number)
        except Exception as e:
            print("Exception")
            print(e)
            return None, None

    def _confirm_enable_condition(self, _data):
        """
        this _confirm_enable_condition method used to check the filterize
        the cognito json data
        """
        return _data["UserStatus"] == "CONFIRMED" and _data["Enabled"] is True

    def create_cognito_to_local(self, cognito_pool_data):
        """
        this create_cognito_to_local method used to create cognito pool data
        """
        self.member_auth_instance = UserService().create_auth_user(
            {
                "first_name": cognito_pool_data["first_name"],
                "last_name": cognito_pool_data["last_name"],
                "email": cognito_pool_data["email"],
                "username": cognito_pool_data["email"],
                "password": self._password,
                "is_active": True,
            }
        )
        if self.member_auth_instance:
            member_serializer_data = self.create_member_with_access_status(
                {
                    "first_name": cognito_pool_data["first_name"],
                    "last_name": cognito_pool_data["last_name"],
                    "email": cognito_pool_data["email"],
                    "isd": cognito_pool_data["isd"],
                    "mobile": cognito_pool_data["mobile"],
                    "registration_type": "web",
                    "department": None,
                    "role": None,
                    "auth_user": self.member_auth_instance.id,
                    "color_hex_code": None,
                    "language": get_language_uuid("ENG"),
                    "is_cognito_user": True,
                    "access_status": ACCESS_STATUS[1][0],
                }
            )
            if not member_serializer_data:
                try:
                    UserService().delete_auth_user(self.member_auth_instance.id)
                except Exception as e:
                    print("UserService.Delete.Exception")
                    print(e)

    def active_member_detail_list(self):
        """
        active_member_detail_list
        this active_member_detail_list method used to to display only
        the active members
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        _custom_user_instance = CustomUsers.objects.filter(
            access_status=ACCESS_STATUS[0][0], is_active=True
        ).order_by("first_name")
        if not _custom_user_instance:
            self.member_user_data = []

        member_serializer = GetMemberDetailSerializer(_custom_user_instance, 
                                                      context={"user_instance": user_instance},
                                                      many=True)

        self.member_user_data = member_serializer.data if member_serializer else []

        try:
            user_member_serializer = SerializerManipulationService(
                type="__single__",
                model_class=UserMemberMapping,
                serializer_class=UserMemberMappingSerializer,
                query_params_var={
                    "is_active": True,
                    "user": self.auth_instance.user_auth,
                },
            )
        except Exception as e:
            print("user_member_serializer")
            print(e)

        try:
            self.member_user_data += user_member_serializer().get("members")
            self.member_user_data = [
                i
                for n, i in enumerate(self.member_user_data)
                if i not in self.member_user_data[n + 1 :]
            ]
            self.member_user_data = sorted(list(self.member_user_data),
                                           key=lambda x: x["first_name"],
                                           reverse=False)
        except Exception as e:
            print("user_member_serializer.exception")
            print(e)

        return {
            "success": True,
            "message": MSG["DONE"],
            "keyname": "members",
            "data": self.member_user_data,
            "status_code": status.HTTP_201_CREATED,
        } if self.member_user_data else self.not_acceptable_response

    def manipulate_local_user_with_cognito_user(self):
        """
        this manipulate_local_user_with_cognito_user method used to manage
        cognito user listing with local related user db
        """
        try:
            cognito_response_data = AWSCognito().get_cognito_user_list()
        except Exception as e:
            cognito_response_data = None
            print("AWSCognitoExceptionErr")
            print(e)

        if cognito_response_data:
            confirmed_and_enbled_users = [
                _data
                for _data in cognito_response_data
                if self._confirm_enable_condition(_data)
            ]
            for _enable_user in confirmed_and_enbled_users:
                for _attr in _enable_user["Attributes"]:
                    if _attr["Name"] == "email":
                        user_instance = get_user_instance({"email": _attr["Value"]})
                        if user_instance:
                            try:
                                CustomUsers.objects.filter(id=user_instance.id).update(is_cognito_user=True)
                            except Exception as e:
                                print("#G89")
                                print(e)
                        else:
                            if _attr["Name"] == "given_name":
                                first_name, last_name = self.split_given_name(_attr["Value"])
                            if _attr["Name"] == "phone_number":
                                isd, mobile_no = self.split_mobile_number(_attr["Value"])
                            try:
                                self.create_cognito_to_local(
                                    {"first_name": first_name,
                                     "last_name": last_name,
                                     "email": _attr["Value"] if _attr["Name"] == "email" else None,
                                     "isd": isd,
                                     "mobile": mobile_no,}
                                )
                            except Exception as e:
                                print(e)

    def member_detail_list(self):
        """this member_detail_list method used to get department related data
        in this method we get department details with in two db table
        single department master query
        with allow access all parameters and add on user
         department mapping query
        params: auth_user_instance
        return: department_master_data (json)
        ############
        ** in this method we cover a one logic afterwords for member
        list access only
        manager and admin user role and in task add time
        only display active members
        """
        # try:
        #     self.manipulate_local_user_with_cognito_user()
        # except Exception as e:
        #     print('manipulateLocalUserWithCognitoUser')
        #     print(e)

        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        _custom_user_instance = CustomUsers.objects.exclude(
            id=self.auth_instance.user_auth.id
        ).filter(access_status=ACCESS_STATUS[0][0]).order_by("first_name")
        if not _custom_user_instance:
            self.member_user_data = []
        member_serializer = GetMemberDetailSerializer(
            _custom_user_instance, context={"user_instance": user_instance}, many=True
        )

        self.member_user_data = member_serializer.data if member_serializer else []

        try:
            user_member_mapping_instance = UserMemberMapping.objects.filter(
                user_id=self.auth_instance.user_auth.id
            ).last()
            if user_member_mapping_instance:
                user_member_serializer = UserMemberMappingSerializer(
                    user_member_mapping_instance,
                    context={"user_instance": user_instance},
                )
                if user_member_serializer:
                    _serializer_data = user_member_serializer.data
        except Exception as e:
            print("userMappingSerializerExpErr")
            print(e)

        try:

            self.member_user_data += _serializer_data["members"]
            self.member_user_data = [
                i
                for n, i in enumerate(self.member_user_data)
                if i not in self.member_user_data[n + 1 :]
            ]
            self.member_user_data = sorted(list(self.member_user_data),
                                           key=lambda x: x["first_name"],
                                           reverse=False)
        except Exception as e:
            print("sortedUserMappingSerializerExpErr")
            print(e)

        return {
                "success": True,
                "message": MSG["DONE"],
                "keyname": "members",
                "data": self.member_user_data,
                "status_code": status.HTTP_201_CREATED,
            } if self.member_user_data else self.not_acceptable_response

    def member_detail_list_for_task_update(self):
        """this member_detail_list_for_task_updation method used to get the list of task updation values
        params: auth_user_instance
        return: department_master_data (json)
        """
        # try:
        #     self.manipulate_local_user_with_cognito_user()
        # except Exception as e:
        #     print('manipulateLocalUserWithCognitoUser')
        #     print(e)

        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        _custom_user_instance = CustomUsers.objects.exclude(
            id=self.auth_instance.user_auth.id
        ).filter(access_status=ACCESS_STATUS[0][0]).order_by("first_name")
        if not _custom_user_instance:
            self.member_user_data = []
        member_serializer = GetMemberDetailSerializer(
            _custom_user_instance,
            context={"user_instance": user_instance},
            many=True)
        self.member_user_data = (
            member_serializer.data
            if member_serializer else
            []
        )

        try:
            user_member_mapping_instance = UserMemberMapping.objects.filter(
                user_id=self.auth_instance.user_auth.id
            ).last()
            if user_member_mapping_instance:
                user_member_serializer = UserMemberMappingSerializer(
                    user_member_mapping_instance,
                    context={"user_instance": user_instance},
                )
                mapping_serializer_data = user_member_serializer.data['members']
            else:
                mapping_serializer_data = []
        except Exception as e:
            mapping_serializer_data = []
            print("userMappingSerializerExpErr")
            print(e)

        try:
            task_detail_serializer = UpdateTaskDetailSerializerForMembers(
                get_task_instance({"id": self.query_params.get("task_id")}),
                context={"user_instance": user_instance},
            )
            task_members_data = task_detail_serializer.data["members"]
        except Exception as e:
            task_members_data = []
            print("TaskMemberExceptionError")
            print(e)

        try:
            self.member_user_data += task_members_data
        except Exception as e:
            print("Err")
            print(e)

        try:
            self.member_user_data += mapping_serializer_data
        except Exception as e:
            print('memberUserDataErr')
            print(e)

        try:
            self.member_user_data = [
                i
                for n, i in enumerate(self.member_user_data)
                if i not in self.member_user_data[n + 1 :]
            ]
            self.member_user_data = sorted(list(self.member_user_data),
                                           key=lambda x: x["first_name"],
                                           reverse=False)
        except Exception as e:
            print("sortedUserMappingSerializerExpErr")
            print(e)

        return {
            "success": True,
            "message": MSG["DONE"],
            "keyname": "members",
            "data": self.member_user_data,
            "status_code": status.HTTP_201_CREATED
        } if self.member_user_data else self.not_acceptable_response

    def member_list_by_department(self):
        """this member_list_by_department get the all member list
        by using department id on add task time
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        try:
            _department_instance = Departments.objects.filter(
                department_name=self.query_params.get("department")
            ).last()
            _department_id = (
                _department_instance.id
                if _department_instance
                else self.query_params.get("department")
            )
        except Exception as e:
            _department_id = self.query_params.get("department")
            print("Departments.DoesNotExist")
            print(e)

        _custom_user_instance = CustomUsers.objects.filter(
            access_status=ACCESS_STATUS[0][0], department_id=_department_id
        ).order_by("first_name")

        if not _custom_user_instance:
            self.member_user_data = []

        try:
            member_serializer = MemberDetailSerializer(_custom_user_instance, many=True)
            self.member_user_data = member_serializer.data if member_serializer else []
        except Exception as e:
            print("MemberDetailSerializer.ExceptionError")
            print(e)

        try:
            user_member_serializer = UserMemberMappingByDepartmentSerializer(
                UserMemberMapping.objects.filter(
                    user=self.auth_instance.user_auth, is_active=True
                ).last(),
                context={"department": _department_id},
            )
            print("user_member_serializer()", user_member_serializer.data)
            self.member_user_data += user_member_serializer.data.get("members")
            self.member_user_data = [
                i
                for n, i in enumerate(self.member_user_data)
                if i not in self.member_user_data[n + 1 :]
            ]
            self.member_user_data = sorted(
                list(self.member_user_data),
                key=lambda x: x["first_name"],
                reverse=False,
            )
        except Exception as e:
            print("user_member_serializer.exception")
            print(e)
        return (
            {
                "success": True,
                "message": MSG["DONE"],
                "keyname": "members",
                "data": self.member_user_data,
                "status_code": status.HTTP_201_CREATED,
            }
            if self.member_user_data
            else self.not_acceptable_response
        )

    @staticmethod
    def create_member_with_access_status(member_request_data):
        """this create_department_with_access_status method create
        department master only using serailizer
        """
        serializer_instance = SerializerManipulationService(
            serializer_class=MemberSerializer,
            request_data=member_request_data,
            type="__create__",
        )
        return serializer_instance()

    def assign_user_mapping(self, member_serializer_data):
        """this assign_user_mapping method used to assign the with user only"""
        user_query_params = {"user": self.auth_instance.user_auth}
        self.user_id_list.append(member_serializer_data.get("id", None))
        mapping_instance = UserMemberMapping.objects.filter(**user_query_params).first()
        if not mapping_instance:
            mapping_instance = UserMemberMapping.objects.create(**user_query_params)
        if mapping_instance:
            mapping_instance.members.add(*self.user_id_list)
            self.final_response["data"] = member_serializer_data
            return self.final_response
        else:
            return self.not_acceptable_response

    def create_member_detail(self):
        """this create_member_detail method used to create member with
        the user assignment access status
        return: member_details (json)
        """
        if not self.member_req_data.get("access_status"):
            self.bad_request_response["message"] = MSG["ACCESS_STATUS_PROVIDE"]
            return self.bad_request_response

        if "Y" != self.member_req_data.get(
            "access_status"
        ) and "N" != self.member_req_data.get("access_status"):
            self.bad_request_response["message"] = MSG.get("VALID_CHOICE")
            return self.bad_request_response

        # check already exists.
        if already_exist_check(
            {"email": self.member_req_data["email"], "access_status": "allow_to_all"}
        ):
            try:
                if self.auth_instance.user_auth.language.language_code == "ENG":
                    member_already_exist_message = MSG["MEMBER_ALREADY_EXISTS"]
                else:
                    member_already_exist_message = ITALIAN_MSG["MEMBER_ALREADY_EXISTS"]
            except Exception as e:
                member_already_exist_message = MSG["MEMBER_ALREADY_EXISTS"]
                print("G219")
                print(e)
            self.bad_request_response["message"] = member_already_exist_message
            return self.bad_request_response

        if already_exist_check(
            {"email": self.member_req_data["email"], "access_status": "self_only"}
        ):
            try:
                if self.auth_instance.user_auth.language.language_code == "ENG":
                    member_already_exist_message = MSG["MEMBER_ALREADY_EXISTS_PRIVATE"]
                else:
                    member_already_exist_message = ITALIAN_MSG[
                        "MEMBER_ALREADY_EXISTS_PRIVATE"
                    ]
            except Exception as e:
                member_already_exist_message = MSG["MEMBER_ALREADY_EXISTS_PRIVATE"]
                print("G219")
                print(e)
            self.bad_request_response["message"] = member_already_exist_message
            return self.bad_request_response

        self._first_name = self.member_req_data["first_name"].capitalize()
        self._last_name = self.member_req_data["last_name"].capitalize()
        self._email = self.member_req_data["email"].lower()
        self._password = "Admin@123"

        _error_msg = None
        try:
            self.cognito_response_data = AWSCognito(
                data={
                    "first_name": self._first_name,
                    "last_name": self._last_name,
                    "email": self._email,
                    "isd": self.member_req_data.get("isd", None),
                    "mobile": self.member_req_data["mobile"],
                    "department": self.member_req_data["department"],
                    "role": self.member_req_data["level"],
                    "password": self._password,
                }
            ).confirm_sign_up()
        except Exception as e:
            self.cognito_response_data = None
            self._is_cognito_user = False
            _error_msg = str(e)
            print("AWSCognitoExceptionErr")
            print(e)

        # if not scognito_response_data:
        #     self.bad_request_response['message'] = _error_msg
        #     return self.bad_request_response

        if self.cognito_response_data:
            self._is_cognito_user = True

        self.member_auth_instance = UserService().create_auth_user(
            {
                "first_name": self._first_name,
                "last_name": self._last_name,
                "email": self._email,
                # "username": self._email,
                "password": self._password,
                "is_active": True,
            }
        )

        if not self.member_auth_instance:
            try:
                if self.auth_instance.user_auth.language.language_code == "ENG":
                    auth_exception_message = MSG.get("AUTH_EXCEPTION")
                else:
                    auth_exception_message = ITALIAN_MSG.get("AUTH_EXCEPTION")
            except Exception as e:
                auth_exception_message = MSG.get("AUTH_EXCEPTION")
                print("G219")
                print(e)
            self.not_acceptable_response["message"] = auth_exception_message
            return self.not_acceptable_response

        member_serializer_data = self.create_member_with_access_status(
            {
                "first_name": self._first_name,
                "last_name": self._last_name,
                "email": self._email,
                "isd": self.member_req_data.get("isd", None),
                "mobile": self.member_req_data["mobile"],
                "registration_type": self.member_req_data["registration_type"],
                "department": self.member_req_data["department"],
                "role": self.member_req_data["level"],
                "auth_user": self.member_auth_instance.id,
                "color_hex_code": self.member_req_data.get("color", None),
                "language": get_language_uuid("ENG"),
                # 'is_cognito_user': self._is_cognito_user,
                "is_cognito_user": True,
                "access_status": (
                    ACCESS_STATUS[0][0]
                    if self.member_req_data["access_status"] == "Y"
                    else ACCESS_STATUS[1][0]
                ),
            }
        )
        if not member_serializer_data:
            try:
                UserService().delete_auth_user(self.member_auth_instance.id)
            except Exception as e:
                print("UserService.Delete.Exception")
                print(e)
            self.not_acceptable_response["message"] = MSG.get("SERIALIZER_NOT_FOUND")
            return self.not_acceptable_response

        if self.member_req_data["access_status"] == "N":
            return self.assign_user_mapping(member_serializer_data)
        self.final_response["data"] = member_serializer_data
        return self.final_response

    def member_activate_deactivate(self):
        """this member_activate_deactivate method used to change the status
        of member using active and in active status
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        try:
            CustomUsers.objects.get(id=self.query_params.get("member_id"))
        except Exception as e:
            print("CustomUser.DoesNotExist")
            print(e)
            self.bad_request_response["errors"] = [
                {"member_id": MSG.get("MEMBER_NOT_EXISTS")}
            ]
            self.bad_request_response["message"] = MSG.get("MEMBER_NOT_EXISTS")
            return self.bad_request_response

        if CustomUsers.objects.filter(id=self.query_params.get("member_id")).update(
            is_active=self.query_params.get("is_active")
        ):
            self.final_response["data"] = {
                "is_active": self.query_params.get("is_active")
            }
            return self.final_response
        else:
            self.not_acceptable_response["message"] = MSG["No_ACTIVE_DATA"]
            return self.not_acceptable_response
