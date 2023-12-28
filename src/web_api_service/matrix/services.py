from rest_framework import status
from core.messages import MSG

from iteration_utilities import duplicates
from django.db.models import Count

from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.api_response_parser import bad_request_response

#  import matrix models
from matrix.models import MatrixConfiguration
from matrix.models import TaskTypeConfig
from matrix.models import MatrixTaskMapping

from core.serializer_getter import SerializerManipulationService

# from matrix
from web_api_service.matrix.serializers import (
    MatrixWithRuleConfigurationSerializer,
    MatrixWithRuleConfigurationItalianSerializer,
)

from web_api_service.helpers.all_config_func import get_user_instance

# import Task management
from task_management.models import Tasks


class MatrixDashboardService:
    """
    all MatrixDashboardService
    """

    def __init__(self, **kwargs):
        self.auth_instance = kwargs.get("auth_instance", None)
        self.final_response = final_response()
        self.not_acceptable = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self.matrix_rule_input = kwargs.get("matrix_rule_input", None)
        self.task_type_config_list = []

    def get_original_matrix(self):
        """
        this get_original_matrix method get the matrix info
        """
        try:
            matrix_serializer = MatrixWithRuleConfigurationSerializer(
                MatrixConfiguration.objects.filter(
                    is_active=True
                ).order_by("updated_at"),
                context={"login_user": self.auth_instance.user_auth},
                many=True,
            )
        except Exception as e:
            print("MatrixWithRuleConfigurationSerializer")
            print(e)
            matrix_serializer = None

        final_data = {
            "success": True,
            "message": MSG["DONE"],
            "keyname": "matrix_config_data",
            "data": matrix_serializer.data,
            "status_code": status.HTTP_200_OK,
        }
        return final_data if matrix_serializer else self.not_acceptable

    def get_italian_language_matrix(self):
        """
        this get_italian_language_matrix method get the list of matrix
        using italian language data
        """
        try:
            matrix_serializer = MatrixWithRuleConfigurationItalianSerializer(
                MatrixConfiguration.objects.filter(
                    is_active=True
                ).order_by("updated_at"),
                context={"login_user": self.auth_instance.user_auth},
                many=True,
            )
        except Exception as e:
            print("MatrixWithRuleConfigurationItalianSerializer")
            print(e)
            matrix_serializer = None

        final_data = {
            "success": True,
            "message": MSG["DONE"],
            "keyname": "matrix_config_data",
            "data": matrix_serializer.data,
            "status_code": status.HTTP_200_OK,
        }
        return final_data if matrix_serializer else self.not_acceptable

    def dashboard_details(self):
        """this get_dashboard_details method used to get dashboard related data
        params: auth_user_instance
        return: data
        """
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG.get("USER_NOT_FOUND")
            return self.bad_request_response

        if user_instance.language.language_code == "ITL":
            return self.get_italian_language_matrix()
        if user_instance.language.language_code == "ENG":
            return self.get_original_matrix()

    def assign_task_matrix(self):
        """
        this assign_task_matrix method used to manage the assign task
        with matrix config rules
        """
        for key, value in self.matrix_rule_input.items():
            task_type_config_instance = TaskTypeConfig.objects.filter(
                rule_name__icontains=str(key),
                priority_status__priority_status_name__icontains=str(value),
            ).last()
            if not task_type_config_instance:
                return None
            self.task_type_config_list.append(task_type_config_instance.id)
        matrix_task_mapping_instance = MatrixTaskMapping.objects.filter(
            task_type_config__id__in=self.task_type_config_list
        )
        if not matrix_task_mapping_instance:
            return None
        try:
            return [
                data.id
                for i, data in enumerate(matrix_task_mapping_instance)
                if data in matrix_task_mapping_instance[:i]
            ][0]
        except Exception as e:
            print("Duplicate.Exception.Error")
            print(e)
            return None
