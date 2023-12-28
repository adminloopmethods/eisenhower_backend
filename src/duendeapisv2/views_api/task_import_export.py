"""TaskImportExportApi
Task Import Export api for update task using Excel sheet data
created at 12/feb/2023
by Loop developer
"""

from rest_framework import status
from rest_framework.views import APIView

from configuration.models import TaskBulkDataExcelFiles
from core.api_response_parser import APIResponseParser, request_not_found
from core.messages import API_RESPONSE_MSG, MSG
from duendeapisv2.services.export_sample_import_sample_task import \
    ExportSampleExportExcelTask
from web_api_service.tasks.import_task_service import ImportExportTaskService


# import service


class TaskExportSampleImportExcelSheetApi(APIView):
    """
    TaskExportSampleImportExcelSheetApi
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
        return ExportSampleExportExcelTask(
            auth_instance=request.user,
            custom_user_id=request.query_params.get('user_id', None)
        ).export_task_sample_sheet_xlsx()

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
                success=False,
                message=API_RESPONSE_MSG["IMPORT_FILE_NAME_NOT_FOUND"]
            )

        create_import_file_obj = TaskBulkDataExcelFiles.objects.create(
            file_save_path=self.task_req_data.get("import_file", None)
        )
        print('views--------------------')
        try:
            success, data, msg = ImportExportTaskService(
                excel_sheet_path=create_import_file_obj.file_save_path.path,
                auth_instance=request.user,
                task_req_data=self.task_req_data,
            ).import_task_list()

            if success is False:
                return APIResponseParser.response(
                    success=False,
                    message=msg,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if success:
                return APIResponseParser.response(
                    success=True,
                    keyname="data",
                    data=data,
                    message=msg,
                    status_code=status.HTTP_200_OK,
                )

        except Exception as e:
            print("ImportExportService.DoesNotExist: %s" % e)
            return APIResponseParser.response(
                success=False,
                message=MSG["CORRECT_SHEET_ERROR"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )
