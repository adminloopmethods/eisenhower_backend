"""
all configuration Services
"""

from random import randint

from django.http import HttpResponse
from core.messages import MSG
from core.constants import ACCESS_STATUS

from core.modules.import_export_excel import ImportExportExcel

from user.models import UserDepartmentMapping
from user.models import UserTopicMapping

from core.custom_serializer_error import SerializerErrorParser
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response
from core.api_response_parser import bad_request_response

from configuration.models import DepartmentBulkDataExcelFiles

from web_api_service.helpers.all_config_func import get_user_instance

from configuration.models import Departments


class ImportExportService:
    """
    this ImportExportService used to manage the import and export excel service
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
        self.department_xlsx_fields = [
            'department_name',
            'description',
            'access_status'
        ]

    def export_department_sample(self):
        """this export_department_sample used to 
        import the department sample file
        """
        try:
            # single random object
            random_object = Departments.objects.all()[
                randint(0, Departments.objects.count() - 1)
            ]
            department_query_set = Departments.objects.filter(id=random_object.id)
        except Exception as e:
            print('Departments.DoesNotExist: %s' % e)
            department_query_set = None

        export_xlsx_parameters = {
            'excel_field_list': self.department_xlsx_fields,
            'excel_title_list': self.department_xlsx_fields,
            'queryset': department_query_set,
            'http_response': HttpResponse,
            'import_sample_filename': 'department-sample',
            'file_content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        }
        # return None
        return ImportExportExcel(**export_xlsx_parameters).export_excel()

    def import_department_list(self):
        """this import_department_list import list by export media files
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
        create_import_file_instance = DepartmentBulkDataExcelFiles.objects.create(
            file_save_path=self.config_req_data['import_file']
        )
        if not create_import_file_instance:
            self.bad_request_response['message'] = MSG['FILE_DOES_NOT_EXIST']
            return self.bad_request_response

        import_excel_params = {
            'model_class': Departments,
            'mapping_model_class': UserDepartmentMapping,
            'excel_sheet_path': create_import_file_instance.file_save_path.path,
            'excel_sheet_name': 'Sheet1',
            'import_type': '__department__',
            'auth_instance': self.auth_instance,
            'auth_user_language': self.auth_instance.user_auth.language.language_code,
        }
        status, import_export_details, msg = ImportExportExcel(
            **import_excel_params
        ).import_excel()
        if status:
            self.final_response['message'] = msg
            self.final_response['data'] = import_export_details
            return self.final_response
        else:
            self.bad_request_response['message'] = msg
            return self.bad_request_response
