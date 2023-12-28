from core.api_response_parser import bad_request_response
from core.api_response_parser import final_response_ok
from core.api_response_parser import not_acceptable_response
from core.custom_serializer_error import SerializerErrorParser
from core.messages import MSG
from task_management.models import TaskComments
from web_api_service.helpers.all_config_func import get_user_instance, get_task_instance
from web_api_service.tasks.serializers import (
    CreateTaskCommentsSerializer,
    TaskCommentsSerializer,
)


class TaskCommentService:
    """
    TaskCommentService
    """

    def __init__(self, **kwargs):
        self.auth_instance = kwargs.get("auth_instance", None)
        self.task_req_data = kwargs.get("task_req_data", None)
        self.task_list_params = kwargs.get("task_list_params", None)
        self.final_response = final_response_ok()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()

    def check_validate_data(self):
        """
        check validate data
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            return MSG.get("USER_NOT_FOUND")
        if self.task_req_data.get("task", None):
            task_instance = get_task_instance({"id": self.task_req_data.get("task")})
            if not task_instance:
                return MSG.get("TASK_NOT_EXISTS")

    def not_acceptable_with_serializer_error_parser(self, serializer_errors):
        """
        not_acceptable_with_serializer_error_parser
        """
        _serializer_error_instance = SerializerErrorParser(str(serializer_errors))
        key_name, error = _serializer_error_instance()
        self.not_acceptable_response["message"] = "".join([str(key_name), str(error)])
        return self.not_acceptable_response

    def update_task_comments(self):
        """this update_task_comments method used to update the task comments"""
        error_checker_msg = self.check_validate_data()
        if error_checker_msg:
            self.bad_request_response["message"] = error_checker_msg
            return self.bad_request_response

        self.task_req_data["members"] = self.auth_instance.user_auth.id
        task_comments_serializer = CreateTaskCommentsSerializer(data=self.task_req_data)
        if task_comments_serializer.is_valid(raise_exception=True):
            task_comments_serializer.save()
            self.final_response["data"] = task_comments_serializer.data
            return self.final_response
        else:
            return self.not_acceptable_with_serializer_error_parser(
                task_comments_serializer.errors
            )

    def get_task_comments(self):
        """this get_task_comments method used to get the task comments from particular task bot"""
        error_checker_msg = self.check_validate_data()
        if error_checker_msg:
            self.bad_request_response["message"] = error_checker_msg
            return self.bad_request_response

        task_comments_instance = TaskComments.objects.filter(
            task=self.task_req_data.get("task")
        )
        if not task_comments_instance:
            self.not_acceptable_response["message"] = MSG.get("No_ACTIVE_DATA")
            return self.not_acceptable_response

        task_comments_serializer = TaskCommentsSerializer(
            task_comments_instance,
            context={"login_user": self.auth_instance.user_auth},
            many=True,
        )
        if task_comments_serializer:
            self.final_response["data"] = task_comments_serializer.data
            return self.final_response
        else:
            return self.not_acceptable_with_serializer_error_parser(
                task_comments_serializer.errors
            )

    def delete_task_comment_db(self, comment_id):
        """this delete_task_comment_db method used to delete comments from task comments db"""
        try:
            is_deleted_instance = TaskComments.objects.filter(id=comment_id).delete()
            self.final_response["data"] = {"is_deleted": True} if is_deleted_instance else {"is_deleted": False}
            return self.final_response
        except Exception as e:
            print("deleteTaskComments.exception", e)
            self.bad_request_response["message"] = str(e)
            return self.bad_request_response

    def edit_and_delete_task_comments(self):
        """
        This edit_and_delete_task_comments method used to edit and delete task comments
        """
        error_checker_msg = self.check_validate_data()
        if error_checker_msg:
            self.bad_request_response["message"] = error_checker_msg
            return self.bad_request_response
        try:
            task_comments_instance = TaskComments.objects.get(
                id=self.task_req_data.get("comment_id"),
                members=self.auth_instance.user_auth,
            )
        except Exception as e:
            self.bad_request_response["message"] = MSG["PROVIDE_COMMENTS_ID_WITH_USER"]
            print(e)
            return self.bad_request_response

        is_deleted_comment = self.task_req_data.get("is_deleted", None)
        if is_deleted_comment:
            return self.delete_task_comment_db(self.task_req_data["comment_id"])

        task_comments_serializer = TaskCommentsSerializer(
            task_comments_instance,
            data=self.task_req_data,
            partial=True
        )
        if task_comments_serializer:
            task_comments_serializer.is_valid(raise_exception=True)
            task_comments_serializer.save()
            self.final_response["data"] = task_comments_serializer.data
            return self.final_response

        # not acceptable common serializers
        return self.not_acceptable_with_serializer_error_parser(
            task_comments_serializer.errors
        )
