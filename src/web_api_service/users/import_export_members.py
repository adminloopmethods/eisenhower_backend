from random import randint

# from django.contrib.auth.models import User
from user.models import User

from django.http import HttpResponse
from core.messages import MSG, ITALIAN_MSG
from core.constants import ACCESS_STATUS

from core.modules.import_export_excel import ImportExportExcel

from user.models import CustomUsers

from user.models import UserMemberMapping


from core.custom_serializer_error import SerializerErrorParser
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.api_response_parser import bad_request_response

from configuration.models import MemberBulkDataExcelFiles

from web_api_service.helpers.all_config_func import get_user_instance

from configuration.models import Departments


class ImportExportMemberService:
    """
    ImportExportMemberService
    path: /api/v1/user/sample/sheet/
    """

    def __init__(self, **kwargs):
        self.department_master_data = []
        self.auth_instance = kwargs.get("auth_instance", None)
        self.member_req_data = kwargs.get("member_req_data", None)
        self.department_id_list = []
        self.topic_id_list = []
        self.final_response = final_response()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self.topic_master_data = []
        self.query_params = kwargs.get("query_params", None)
        self.user_xlsx_fields = [
            "first_name",
            "last_name",
            "isd",
            "mobile",
            "email",
            "access_status",
            "registration_type",
            "department",
            "color_hex_code",
            "role",
        ]
        self.msg = "Errors"

    def export_member_sample(self):
        """
        this export_department_sample used to import the department sample file
        """
        try:
            # single random object
            _random_instance_object = CustomUsers.objects.all()[
                randint(0, CustomUsers.objects.count() - 1)
            ]
            custom_user_query_set = CustomUsers.objects.filter(
                id=_random_instance_object.id
            )
        except Exception as e:
            print("Departments.DoesNotExist: %s" % e)
            custom_user_query_set = None
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )

        export_xlsx_parameters = {
            "excel_field_list": self.user_xlsx_fields,
            "excel_title_list": self.user_xlsx_fields,
            "queryset": custom_user_query_set,
            "http_response": HttpResponse,
            "import_sample_filename": "member-sample",
            # 'file_content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            "file_content_type": "text/csv",
            "custom_user_id": self.query_params.get('user_id', None),
            "customer_id":user_instance
        }
        # return None
        return ImportExportExcel(**export_xlsx_parameters).export_excel()

    def import_member_list(self):
        """this import_department_list import list by export media files."""
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            self.bad_request_response["message"] = MSG["USER_NOT_FOUND"]
            return self.bad_request_response

        create_import_file_instance = MemberBulkDataExcelFiles.objects.create(
            file_save_path=self.member_req_data["import_file"]
        )

        if not create_import_file_instance:
            try:
                self.msg = (
                    MSG["FILE_DOES_NOT_EXIST"]
                    if self.auth_instance.user_auth.language.language_code == "ENG" else
                    ITALIAN_MSG["FILE_DOES_NOT_EXIST"]
                )
            except ValueError:
                self.msg = MSG["FILE_DOES_NOT_EXIST"]
            self.bad_request_response["message"] = self.msg
            return self.bad_request_response

        import_excel_params = {
            "model_class": User,
            "mapping_model_class": UserMemberMapping,
            "excel_sheet_path": create_import_file_instance.file_save_path.path,
            "excel_sheet_name": "Sheet1",
            "import_type": "__member__",
            "auth_instance": self.auth_instance,
            "auth_user_language": self.auth_instance.user_auth.language.language_code,
        }
        status, import_export_details, msg = ImportExportExcel(
            **import_excel_params
        ).import_excel()

        if status:
            self.final_response["message"] = msg
            self.final_response["data"] = import_export_details
            return self.final_response
        else:
            self.bad_request_response["message"] = msg
            return self.bad_request_response
