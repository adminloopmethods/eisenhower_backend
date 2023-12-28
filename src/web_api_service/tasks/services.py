"""
This Task Service used to manage the all task related methods
"""
import operator
from functools import reduce

from django.db.models import Q

from core.api_response_parser import bad_request_response
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.custom_serializer_error import SerializerErrorParser
from core.messages import MSG
# import serializer manipulation
from core.serializer_getter import SerializerManipulationService
from task_management.models import Tasks
from web_api_service.helpers.all_config_func import (
    get_task_instance,
    get_member_details_using_member_id,
)
# import all related modules instance
from web_api_service.helpers.all_config_func import get_user_instance
from web_api_service.matrix.services import MatrixDashboardService
from web_api_service.notification.push_notification import PushNotifications
from web_api_service.tasks.serializers import TaskDetailSerializer
# import serializer
from web_api_service.tasks.serializers import TasksSerializer


class TaskService:
    """
    all UserMemberService
    create_topic_detail
    """

    def __init__(self, **kwargs):
        self.department_master_data = []
        self.auth_instance = kwargs.get("auth_instance", None)
        self.task_req_data = kwargs.get("task_req_data", None)
        self.task_list_params = kwargs.get("task_list_params", None)
        self.department_id_list = []
        self.user_id_list = []
        self.final_response = final_response()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self.topic_master_data = []
        self.matrix_rule_input = {}
        self.task_instance = Tasks.objects.filter()
        self.matrix_priority_status = "High"
        self.task_filter_list = []
        self.members = []
        self.imp_urg_dict = {"0": "High", "50": "Medium", "100": "Low"}

    def not_acceptable_with_serializer_error_parser(self, serializer_errors):
        """
        not_acceptable_with_serializer_error_parser
        """
        _serializer_error_instance = SerializerErrorParser(str(serializer_errors))
        key_name, error = _serializer_error_instance()
        self.not_acceptable_response["message"] = "".join([str(key_name), str(error)])
        return self.not_acceptable_response

    def create_task(self):
        """
        this create_task method used to create task for a manager as user or member
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG.get("USER_NOT_FOUND")
            return self.bad_request_response

        _matrix_config_detail = self.task_req_data.get("matrix_config_detail", None)
        if not _matrix_config_detail:
            self.bad_request_response["message"] = MSG.get("MATRIX_ERROR_EXCEPTION_V1")
            return self.bad_request_response

        try:
            self.matrix_rule_input = {
                "importance": self.imp_urg_dict[
                    str(
                        _matrix_config_detail.get(
                            "importance", self.matrix_priority_status
                        )
                    )
                ],
                "urgency": self.imp_urg_dict[
                    str(
                        _matrix_config_detail.get(
                            "urgency", self.matrix_priority_status
                        )
                    )
                ],
            }
        except Exception as e:
            print("matrix_rule_input_exception")
            print(e)

        matrix_rule_config = MatrixDashboardService(
            auth_instance=self.auth_instance, matrix_rule_input=self.matrix_rule_input
        ).assign_task_matrix()

        if not matrix_rule_config:
            self.not_acceptable_response["message"] = MSG.get("MATRIX_ERROR_EXCEPTION")
            return self.not_acceptable_response

        self.task_req_data["task_owner"] = self.auth_instance.user_auth.id
        self.task_req_data["matrix_type_config"] = matrix_rule_config

        task_serializer_data = TasksSerializer(data=self.task_req_data)
        if task_serializer_data.is_valid(raise_exception=True):
            task_serializer_data.save()
            try:
                members = task_serializer_data.data["members"]
                for member in members:
                    print("i")
                    print(member)
                    member_details_data = get_member_details_using_member_id(member)
                    push_notification_instance = PushNotifications(
                        api_service_name="__TASKASSIGNE__",
                        TO="admin",
                        user=member,
                        user_notification_data={
                            "username": member_details_data["full_name"],
                            "task_name": str(self.task_req_data.get("task_name", None)),
                        },
                    )
                    push_notification_instance()
            except Exception as e:
                print("TaskAssigneeNotificationErr")
                print(e)

            try:
                push_notification_instance = PushNotifications(
                    api_service_name="__TASKASSIGN__",
                    TO="admin",
                    user=user_instance.id,
                    user_notification_data={
                        "username": "".join(
                            [
                                str(user_instance.first_name),
                                " ",
                                str(user_instance.last_name),
                            ]
                        ),
                        "task_name": str(self.task_req_data.get("task_name", None)),
                    },
                )
                push_notification_instance()
            except Exception as e:
                print("NotificationErr")
                print(e)

            self.final_response["data"] = task_serializer_data.data
            return self.final_response
        return self.not_acceptable_with_serializer_error_parser(
            task_serializer_data.errors
        )

    def task_list(self):
        """this task_list method used to get the all task list from task db table
        we covered the all types of delete and notification trigger cases.
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG.get("USER_NOT_FOUND")
            return self.bad_request_response

        if self.task_list_params["status"] == "all":

            # self.task_instance = self.task_instance.filter(
            #     Q(task_owner__id=self.auth_instance.user_auth.id)
            #     | Q(members__in=[self.auth_instance.user_auth.id]),
            #     matrix_type_config__matrix_type__id=self.task_list_params.get(
            #         "matrix_id"
            #     ),
            #     is_deleted=False,
            # )

            self.task_instance = self.task_instance.filter(
                members__in=[self.auth_instance.user_auth.id],
                matrix_type_config__matrix_type__id=self.task_list_params.get(
                    "matrix_id"
                ),
                is_deleted=False,
            )

            try:
                self.task_instance.filter(Q(members=None)).delete()
            except Exception as e:
                print("#Err")
                print(e)

            task_serializer = TaskDetailSerializer(
                self.task_instance.order_by("created_at"),
                context={"user_instance": user_instance},
                many=True,
            )
            if task_serializer:
                task_serializer_data = [
                    i
                    for n, i in enumerate(task_serializer.data)
                    if i not in task_serializer.data[n + 1:]
                ]
                task_serializer_data = sorted(
                    list(task_serializer_data),
                    key=lambda x: x["created_at"],
                    reverse=True,
                )

                self.final_response["data"] = task_serializer_data
                return self.final_response

        if self.task_list_params:
            # self.task_instance = self.task_instance.filter(
            #     Q(task_owner__id=self.auth_instance.user_auth.id)
            #     | Q(members__in=[self.auth_instance.user_auth.id])
            # ).filter(
            #     status__status_name__icontains=self.task_list_params.get("status"),
            #     matrix_type_config__matrix_type__id=self.task_list_params.get(
            #         "matrix_id"
            #     ),
            #     is_deleted=False,
            # )

            self.task_instance = self.task_instance.filter(
                members__in=[self.auth_instance.user_auth.id]
            ).filter(
                status__status_name__icontains=self.task_list_params.get("status"),
                matrix_type_config__matrix_type__id=self.task_list_params.get(
                    "matrix_id"
                ),
                is_deleted=False,
            )

        try:
            self.task_instance.filter(Q(members=None)).delete()
        except Exception as e:
            print("InstanceExpErr")
            print(e)

        task_serializer = TaskDetailSerializer(
            self.task_instance.order_by("created_at"),
            context={"user_instance": user_instance},
            many=True,
        )
        if task_serializer:
            task_serializer_data = [
                i
                for n, i in enumerate(task_serializer.data)
                if i not in task_serializer.data[n + 1:]
            ]
            task_serializer_data = sorted(
                list(task_serializer_data), key=lambda x: x["created_at"], reverse=True
            )

            self.final_response["data"] = task_serializer_data
            return self.final_response
        return self.not_acceptable_with_serializer_error_parser(task_serializer.errors)

    def task_status_update(self):
        """this task_status_update method used to update status"""
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        task_instance = get_task_instance({"id": self.task_list_params.get("task")})
        if not task_instance:
            self.bad_request_response["errors"] = [
                {"task": MSG.get("TASK_NOT_EXISTS")}
            ]
            self.bad_request_response["message"] = MSG.get("TASK_NOT_EXISTS")
            return self.bad_request_response

        try:
            members_task_instance = Tasks.objects.filter(
                id=self.task_list_params.get("task"),
                task_owner=user_instance,
                members_id__in=[user_instance.id]
            )
        except Exception as e:
            members_task_instance = None
            print('taskInstanceErr')
            print(e)

        if Tasks.objects.filter(id=self.task_list_params.get("task")).update(
                status=self.task_list_params.get("status")
        ):

            if members_task_instance:
                try:
                    task_status_name = task_instance.status.status_name
                    if str(self.task_list_params.get("status")) == "44716a50-58e2-4895-be14-460a069ff4e9":
                        # if task_status_name == "To-do" or task_status_name == "done":
                        push_notification_instance = PushNotifications(
                            api_service_name="__TASKSTATUSDONE__",
                            TO="admin",
                            user=task_instance.task_owner.id,
                            user_notification_data={
                                "username": "".join(
                                    [
                                        str(task_instance.task_owner.first_name),
                                        " ", str(task_instance.task_owner.last_name)
                                    ]
                                ),
                                "task_name": str(task_instance.task_name),
                                "done_by_username": "".join(
                                    [
                                        str(user_instance.first_name),
                                        " ", str(user_instance.last_name),
                                    ]
                                ),
                            },
                        )
                        push_notification_instance()
                except Exception as e:
                    print("TaskDoneNotificationExpErr")
                    print(e)
            else:
                try:
                    task_status_name = task_instance.status.status_name
                    if str(self.task_list_params.get("status")) == "44716a50-58e2-4895-be14-460a069ff4e9":
                        # if task_status_name == "To-do" or task_status_name == "done":
                        push_notification_instance = PushNotifications(
                            api_service_name="__TASKSTATUSDONE__",
                            TO="admin",
                            user=task_instance.task_owner.id,
                            user_notification_data={
                                "username": "".join(
                                    [
                                        str(task_instance.task_owner.first_name),
                                        " ", str(task_instance.task_owner.last_name)
                                    ]
                                ),
                                "task_name": str(task_instance.task_name),
                                "done_by_username": "".join(
                                    [
                                        str(user_instance.first_name),
                                        " ", str(user_instance.last_name),
                                    ]
                                ),
                            },
                        )
                        push_notification_instance()
                except Exception as e:
                    print("TaskDoneNotificationExpErr")
                    print(e)

                try:
                    task_status_name = task_instance.status.status_name
                    if str(self.task_list_params.get("status")) == "44716a50-58e2-4895-be14-460a069ff4e9":
                        # if task_status_name == "To-do" or task_status_name == "done":
                        members = task_instance.members.filter()
                        for member in members:
                            push_notification_instance = PushNotifications(
                                api_service_name="__TASKSTATUSDONE__",
                                TO="admin",
                                user=member.id,
                                user_notification_data={
                                    "username": "".join(
                                        [str(member.first_name), " ", str(member.last_name)]
                                    ),
                                    "task_name": str(task_instance.task_name),
                                    "done_by_username": "".join(
                                        [
                                            str(user_instance.first_name),
                                            " ",
                                            str(user_instance.last_name),
                                        ]
                                    ),
                                },
                            )
                            push_notification_instance()
                except Exception as e:
                    print("TaskDoneNotificationExpErr")
                    print(e)

            self.final_response["data"] = {
                "is_status_changed": True
            }
            return self.final_response
        else:
            self.not_acceptable_response["message"] = MSG["No_ACTIVE_DATA"]
            return self.not_acceptable_response

    def create_filter_list(self):
        """
        this create_filter_list method create the filter list for filter out request
        """
        if self.task_req_data.get("department"):
            self.task_filter_list.append(
                Q(department_id=self.task_req_data.get("department"))
            )

        if self.task_req_data.get("topic"):
            self.task_filter_list.append(Q(topic_id=self.task_req_data.get("topic")))

        if self.task_req_data.get("members"):
            self.task_filter_list.append(
                Q(members__in=self.task_req_data.get("members"))
            )

        # @@for date filter range ---->
        # if self.task_req_data.get('start_datetime') and self.task_req_data.get('due_datetime'):
        #     self.task_filter_list.append(
        #         Q(start_date__date__range=[
        #             self.task_req_data.get('start_datetime'),
        #             self.task_req_data.get('due_datetime')
        #         ]
        #         )
        #     )

        if self.task_req_data.get("start_datetime") and self.task_req_data.get(
                "due_datetime"
        ):
            self.task_filter_list.extend(
                [
                    Q(start_date__date=self.task_req_data.get("start_datetime"))
                    | Q(due_date__date=self.task_req_data.get("due_datetime"))
                ]
            )

        if self.task_req_data.get("start_datetime"):
            self.task_filter_list.append(
                Q(start_date__date=self.task_req_data.get("start_datetime"))
            )
        if self.task_req_data.get("due_datetime"):
            self.task_filter_list.append(
                Q(due_date__date=self.task_req_data.get("due_datetime"))
            )

    def filter_task_list(self):
        """
        this filter_task_list method used to get the all filter request data
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG.get("USER_NOT_FOUND")
            return self.bad_request_response

        # task_query_set = self.task_instance.filter(
        #     task_owner__id=self.auth_instance.user_auth.id,
        #     matrix_type_config__matrix_type__id=self.task_req_data.get('matrix_id')).select_related()

        # task_query_set = (
        #     self.task_instance.filter(
        #         Q(task_owner__id=self.auth_instance.user_auth.id)
        #         | Q(members__in=[self.auth_instance.user_auth.id])
        #     )
        #     .filter(
        #         matrix_type_config__matrix_type__id=self.task_req_data.get("matrix_id")
        #     )
        #     .select_related()
        # )

        task_query_set = (
            self.task_instance.filter(members__in=[self.auth_instance.user_auth.id])
            .filter(
                matrix_type_config__matrix_type__id=self.task_req_data.get("matrix_id"),
                is_deleted=False,
            )
            .select_related()
        )

        if not task_query_set:
            self.not_acceptable_response["message"] = MSG["No_ACTIVE_DATA"]
            return self.not_acceptable_response

        self.create_filter_list()
        if len(self.task_filter_list) > 0:
            _task_filter_data = reduce(operator.and_, self.task_filter_list)
            if self.task_req_data["status"] == "all":
                _task_instance = task_query_set.filter(_task_filter_data)
            else:
                _task_instance = task_query_set.filter(
                    status__status_name__icontains=self.task_req_data.get("status")
                ).filter(_task_filter_data)
        else:
            if self.task_req_data["status"] == "all":
                _task_instance = task_query_set
            else:
                _task_instance = task_query_set.filter(
                    status__status_name__icontains=self.task_req_data.get("status")
                )

        task_serializer = TaskDetailSerializer(
            _task_instance.order_by("created_at"),
            context={"user_instance": user_instance},
            many=True,
        )
        if task_serializer:
            self.final_response["data"] = sorted(
                list(
                    [
                        i
                        for n, i in enumerate(task_serializer.data)
                        if i not in task_serializer.data[n + 1:]
                    ]
                ),
                key=lambda x: x["created_at"],
                reverse=True,
            )
            return self.final_response
        return self.not_acceptable_with_serializer_error_parser(task_serializer.errors)

    def task_details(self):
        """
        this task_details method used to get task detail using task id
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG.get("USER_NOT_FOUND")
            return self.bad_request_response

        task_instance = get_task_instance({"id": self.task_list_params.get("task_id")})
        if not task_instance:
            self.bad_request_response["errors"] = [{"task": MSG.get("TASK_NOT_EXISTS")}]
            self.bad_request_response["message"] = MSG.get("TASK_NOT_EXISTS")
            return self.bad_request_response

        task_detail_serializer = TaskDetailSerializer(
            task_instance, context={"user_instance": user_instance}
        )
        if task_detail_serializer:
            self.final_response["data"] = task_detail_serializer.data
            return self.final_response

        return self.not_acceptable_with_serializer_error_parser(
            task_detail_serializer.errors
        )

    @staticmethod
    def mutual_serializer_manipulation(serializer_params):
        """
        This mutual_serializer_manipulation used to manage all serializer callable data
        """
        serializer_instance = SerializerManipulationService(**serializer_params)
        return serializer_instance()

    def delete_task_db(self, serializer_params):
        """
        this delete_topic_db method used to delete the department from db
        """
        _mutul_serializer_data = self.mutual_serializer_manipulation(serializer_params)
        self.final_response["data"] = (
            {"is_deleted": True} if _mutul_serializer_data else {"is_deleted": False}
        )
        return self.final_response

    def _manipulate_matrix_request(self):
        """this manipulate_matrix_request method used to manage matrix request data
        """
        _matrix_config_detail = self.task_req_data.get("matrix_config_detail", None)
        if _matrix_config_detail:
            self.imp_urg_dict[
                str(
                    _matrix_config_detail.get(
                        "importance", self.matrix_priority_status
                    )
                )
            ]
            self.matrix_rule_input = {
                "importance": self.imp_urg_dict[
                    str(
                        _matrix_config_detail.get(
                            "importance", self.matrix_priority_status
                        )
                    )
                ],
                "urgency": self.imp_urg_dict[
                    str(
                        _matrix_config_detail.get(
                            "urgency", self.matrix_priority_status
                        )
                    )
                ],
            }
            matrix_rule_config = MatrixDashboardService(
                auth_instance=self.auth_instance,
                matrix_rule_input=self.matrix_rule_input,
            ).assign_task_matrix()

            if not matrix_rule_config:
                self.task_req_data["matrix_type_config"] = None
            else:
                self.task_req_data["matrix_type_config"] = matrix_rule_config

    def _manage_related_fields_from_name(self):
        """this manage_related_fields_from_name method used to manage all related fields from name"""
        pass
        # for status alias id
        # _status = self.task_req_data.get('status', None)
        # if _status:
        #     _status_instance = get_status_instance({'status_name__icontains': _status})
        #     if _status_instance:
        #         self.task_req_data['status'] = _status_instance.id

        # for department alias id
        # _department = self.task_req_data.get('department', None)
        # if _department:
        #     _department_instance = get_department_instance({'department_name': _department})
        #     if _department_instance:
        #         self.task_req_data['department'] = _department_instance.id

        # # for topic alias id
        # _topic = self.task_req_data.get('topic', None)
        # if _topic:
        #     _topic_instance = get_topic_instance({'topic_name__icontains': _topic})
        #     if _topic_instance:
        #         self.task_req_data['topic'] = _topic_instance.id

    def update_task_details(self):
        """this update_task_details method is used to update the task details"""
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        task_instance = get_task_instance({"id": self.task_req_data.get("task_id")})
        if not task_instance:
            self.bad_request_response["errors"] = [
                {"task_id": MSG.get("TASK_NOT_EXISTS")}
            ]
            self.bad_request_response["message"] = MSG.get("TASK_NOT_EXISTS")
            return self.bad_request_response

        self._manipulate_matrix_request()
        # self._manage_related_fields_from_name()

        serializer_params = {
            "serializer_class": TasksSerializer,
            "request_data": self.task_req_data,
            "model_instance": task_instance,
            "type": "__update__",
        }

        is_deleted_task = self.task_req_data.get("is_deleted", None)
        if is_deleted_task:
            return self.delete_task_db(serializer_params)

        task_serializer_data = self.mutual_serializer_manipulation(serializer_params)
        if not task_serializer_data:
            self.not_acceptable_response["message"] = MSG.get(
                "TASK_SERIALIZER_NOT_UPDATE"
            )
            return self.not_acceptable_response

        self.final_response["data"] = task_serializer_data
        return self.final_response
