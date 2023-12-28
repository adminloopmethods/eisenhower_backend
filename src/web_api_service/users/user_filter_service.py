"""
all configuration Services
"""

import operator
from functools import reduce

from django.db.models import Q

from core.api_response_parser import bad_request_response
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.custom_serializer_error import SerializerErrorParser
from core.messages import MSG, ITALIAN_MSG
from user.models import CustomUsers, UserMemberMapping
from web_api_service.helpers.all_config_func import get_user_instance

from core.constants import ACCESS_STATUS

#  all serializer models
from web_api_service.users.serializers import (
    MemberDetailSerializer,
    GetMemberDetailSerializer,
)
from web_api_service.users.serializers import UserMemberSearchMappingSerializer


class MemberFilterService:
    """
    all ConfigFilterService
    create_topic_detail
    create and deleted case with duplicated system is pending
    """

    def __init__(self, **kwargs):
        self.first_name = ""
        self.last_name = ""
        self.department_master_data = []
        self.auth_instance = kwargs.get("auth_instance", None)
        self.member_req_data = kwargs.get("member_req_data", None)
        self.department_id_list = []
        self.member_filter_list = []
        self.final_response = final_response()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self.topic_master_data = []
        self.query_params = kwargs.get("query_params", None)
        self.member_user_data = None

    def not_acceptable_with_serializer_error_parser(self, serializer_errors):
        """
        not_acceptable_with_serializer_error_parser
        """
        _serializer_error_instance = SerializerErrorParser(str(serializer_errors))
        key_name, error = _serializer_error_instance()
        self.not_acceptable_response["message"] = "".join([str(key_name), str(error)])
        return self.not_acceptable_response

    def search_member_list(self):
        """this search_member_list method used to get the
        department list by using search keywords.
        """
        # if (self.query_params.get('q') == ''
        #     or self.query_params.get('q') is None):
        #     self.bad_request_response['message'] = MSG['No_ACTIVE_DATA']
        #     return self.bad_request_response

        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        try:
            self.first_name = self.query_params.get("q").split(" ")[0]
            self.last_name = self.query_params.get("q").split(" ")[1]
            # filter for combined full name
            custom_user_query_set = (
                CustomUsers.objects.exclude(
                    id=self.auth_instance.user_auth.id, is_active=True
                )
                .filter(access_status=ACCESS_STATUS[0][0])
                .filter(
                    # Q(first_name__istartswith=self.first_name) |
                    # Q(last_name__istartswith=self.first_name) |
                    # Q(first_name__istartswith=self.last_name) |
                    # Q(last_name__istartswith=self.last_name)
                    # Q(first_name__istartswith=self.first_name) |
                    # Q(last_name__istartswith=self.first_name) |
                    Q(first_name__istartswith=self.first_name)
                    & Q(last_name__istartswith=self.last_name)
                )
                .order_by("first_name")
            )
        except Exception as e:
            print("firstSearchExpErr")
            print(e)
            # custom_user_query_set = None
            try:
                custom_user_query_set = (
                    CustomUsers.objects.exclude(
                        id=self.auth_instance.user_auth.id, is_active=True
                    )
                    .filter(first_name__istartswith=self.query_params.get("q"))
                    .filter(access_status=ACCESS_STATUS[0][0])
                    .order_by("first_name")
                )
            except Exception as e:
                print(e)
                print("onlyFirstName.CustomUsers.Exception")

        member_search_serializer = GetMemberDetailSerializer(
            custom_user_query_set, context={"user_instance": user_instance}, many=True
        )
        if member_search_serializer:
            self.member_user_data = member_search_serializer.data

        try:
            try:
                user_mapping_instance = UserMemberMapping.objects.filter(
                    is_active=True, user=self.auth_instance.user_auth
                ).last()
            except Exception as e:
                print("UserMemberMapping.Search.DoesNotExist: %s" % e)
                try:
                    user_mapping_instance = UserMemberMapping.objects.filter(
                        is_active=True,
                        user=self.auth_instance.user_auth
                        # first_name__istartswith=self.query_params.get('q')
                    ).last()
                except Exception as e:
                    print("UserMemberMapping.CustomUsers.Exception")
                    print(e)
            member_search_serializer = UserMemberSearchMappingSerializer(
                user_mapping_instance,
                context={
                    "user_instance": user_instance,
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                },
            ).data
            self.member_user_data += member_search_serializer.get("members")
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

        if self.member_user_data:
            self.final_response["data"] = self.member_user_data
            return self.final_response
        return self.not_acceptable_with_serializer_error_parser(
            member_search_serializer.errors
        )

    def create_filter_list(self):
        """
        this create_filter_list method create the filter list for filter out request
        """
        if self.member_req_data.get("department"):
            self.member_filter_list.append(
                Q(department_id=self.member_req_data.get("department"))
            )

        if self.member_req_data.get("isd"):
            self.member_filter_list.append(Q(isd=self.member_req_data.get("isd")))

    def filter_member_list(self):
        """this filter_member_list method get the member list using request of filter."""
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG.get("USER_NOT_FOUND")
            return self.bad_request_response

        custom_user_query_set = CustomUsers.objects.filter(
            is_active=True
        ).select_related()
        if not custom_user_query_set:

            try:
                if user_instance.language.language_code == "ENG":
                    self.msg = MSG["No_ACTIVE_DATA"]
                else:
                    self.msg = ITALIAN_MSG["No_ACTIVE_DATA"]
            except Exception as e:
                print("##G199")
                print(e)
                self.msg = MSG["No_ACTIVE_DATA"]

            self.not_acceptable_response["message"] = self.msg
            return self.not_acceptable_response

        self.create_filter_list()
        if len(self.member_filter_list) > 0:
            _member_filter_data = reduce(operator.and_, self.member_filter_list)
            _custom_user_instance = custom_user_query_set.filter(_member_filter_data).exclude(auth_user=self.auth_instance)
        else:
            _custom_user_instance = custom_user_query_set.exclude(auth_user=self.auth_instance)

        member_serializer = MemberDetailSerializer(
            _custom_user_instance.order_by("first_name"), many=True
        )
        if member_serializer:
            self.final_response["data"] = member_serializer.data
            return self.final_response
        return self.not_acceptable_with_serializer_error_parser(
            member_serializer.errors
        )
