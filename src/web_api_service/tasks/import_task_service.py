"""
ImportExportTaskService
"""

from datetime import datetime
from itertools import chain

# excel sheet related package
import xlwt
from django.http import HttpResponse

# all models
from configuration.models import Departments
from configuration.models import TaskStatusMaster
from configuration.models import Topics
from core.constants import ACCESS_STATUS
# import api response with messages
from core.custom_serializer_error import SerializerErrorParser
from core.messages import MSG
# import import export base class
from core.modules.import_export_excel import ImportExportExcel
from user.models import CustomUsers
from user.models import UserDepartmentMapping
from user.models import UserMemberMapping
from user.models import UserTopicMapping
# department and notification call
from web_api_service.helpers.all_config_func import get_department_id_from_name
# all api services
from web_api_service.helpers.all_config_func import get_user_instance
from web_api_service.helpers.task_sample_excel_details import TASK_DUMMY_DATA
from web_api_service.helpers.task_sample_excel_details import TASK_SAMPLE_COLUMN
from web_api_service.helpers.validations import APIValidation
from web_api_service.matrix.services import MatrixDashboardService
from web_api_service.notification.push_notification import PushNotifications
from web_api_service.tasks.serializers import TasksSerializer

FILENAME = "Sheet1"
CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


class ImportExportTaskService(ImportExportExcel):
    """
    endpoint: /api/v1/task/bulk/import/
    this ImportExportTaskService module used to manage the import
    the task using excel format this module manage sample sheet
    get method to show sample sheet sample sheet will be dynamic
    like all config parameter given by sheet
    {
            'department': '751b9b63-6fcb-4a3b-8152-a1fb8ed648b2',
             'topic': 'bd098a81-10c5-4695-abfe-015f57499001',
             'members': ['51ea49c2-326e-41fc-a1f8-40a6ae2f7475',
                         '872ec914-7933-495d-ac28-220c603c5ee9'],
             'customer_name': 'adhaan',
             'task_name': 'rest',
             'description': 'test',
             'start_date': 1669075200000,
             'end_date': 1669766400000,
             'estimate': 33,
             'status': 'a29bcdb0-82f0-4950-a843-24213c3e7a6b',
             'importance': 'high',
             'urgency': 'low',
             'reminder': 1669248000000,
             'task_owner': UUID('a8c1c071-153c-459b-97a0-e6a5e702b3a7'),
             'matrix_type_config': UUID('38ad9ee2-10fd-4f83-acbc-1ec58f711ac9')
    }
    """

    def __init__(self, **kwargs):

        # inherit base class attribute
        super().__init__(**kwargs)

        self.file = None
        # auth user instance

        self.auth_instance = kwargs.get("auth_instance")
        self.custom_user_id = kwargs.get("custom_user_id")

        # excel related attribute
        self.sheet_titles = [
            "task_name",
            "customer_name",
            "description",
            "start_date",
            "due_date",
            "estimate_hour",
            "reminder",
            "status_id",
            "department",
            "topic_id",
            "members_id",
            "importance",
            "urgency",
        ]

        self.task_fields, self.task_titles = self.sheet_titles, self.sheet_titles
        self.import_sample_sheet_name = "tasks"
        self.import_sample_file_name = "attachment; filename={}.csv".format(
            self.import_sample_sheet_name
        )

        self.excel_sheet_path = kwargs.get("excel_sheet_path", None)
        self.excel_sheet_name = kwargs.get("excel_sheet_name", FILENAME)
        self.final_response_dict = {}
        self.exception_data_list = []
        self.member_list = []
        self.task_update_list = []

        self.task_dummy_data = TASK_DUMMY_DATA
        self.task_sample_column = TASK_SAMPLE_COLUMN

        self.date_format = "%d/%m/%Y"
        # self.date_format = "%m/%d/%Y"

    @staticmethod
    def task_details_data(ws):
        """this method task_details_data used to collect
        task details data from models.
        """
        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        str_style = xlwt.easyxf(num_format_str='@')

        columns = TASK_SAMPLE_COLUMN
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], str_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        str_style = xlwt.easyxf(num_format_str='@')
        # for dummy task details

        rows = TASK_DUMMY_DATA

        # Tasks

        # for row in rows:
        #     row_num += 1
        #     for col_num in range(len(row)):
        #         if row[col_num] == 'dd/mm/yyyy':
        #             ws.write(row_num, col_num, row[col_num], date_style)
        #         else:
        #             ws.write(row_num, col_num, row[col_num], font_style)

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], str_style)

    @staticmethod
    def departments_excel_list(ws, _custom_user_id):
        """this method departments_excel_data used to collect department
        related data to store data
        """
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [
            'id',
            'department'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = Departments.objects.filter(
            is_active=True,
            access_status=ACCESS_STATUS[0][0]
        ).values_list('id', 'department_name')
        try:
            user_department_mapping = UserDepartmentMapping.objects.get(
                is_active=True, user_id=_custom_user_id
            )
        except UserDepartmentMapping.DoesNotExist:
            print('UserDepartmentMapping.DoesNotExist')
            _user_department_mapping = None
        try:
            departments_values = user_department_mapping.departments.filter(
                is_active=True
            ).values_list('id', 'department_name')
        except Exception as e:
            departments_values = None
            print('userDepartmentMappingExpErr')
            print(e)
        try:
            rows = list(set(list(chain(rows, departments_values))))
        except Exception as e:
            print('concatenateQuerySetExpErr')
            print(e)

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

    @staticmethod
    def topics_excel_list(ws, _custom_user_id):
        """this method departments_excel_data used to collect department
        related data to store data
        """
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [
            'id',
            'topic'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = Topics.objects.filter(
            is_active=True,
            access_status=ACCESS_STATUS[0][0]
        ).values_list('id', 'topic_name')
        try:
            user_topic_mapping = UserTopicMapping.objects.get(
                is_active=True, user_id=_custom_user_id
            )
        except UserTopicMapping.DoesNotExist:
            print('UserDepartmentMapping.DoesNotExist')
            user_topic_mapping = None
        try:
            topics_values = user_topic_mapping.topics.filter(
                is_active=True
            ).values_list('id', 'topics')
        except Exception as e:
            topics_values = None
            print('userDepartmentMappingExpErr')
            print(e)
        try:
            rows = list(set(list(chain(rows, topics_values))))
        except Exception as e:
            print('concatenateQuerySetExpErr')
            print(e)

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num,
                         col_num,
                         str(row[col_num]),
                         font_style)

    @staticmethod
    def members_excel_list(ws, _custom_user_id):
        """this method member_excel_data used to collect member
        related data to store data
        """
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [
            'id',
            'first_name',
            'last_name',
            'email',
            'role'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        _query_rows = CustomUsers.objects.filter(
            # is_active=True,
            access_status=ACCESS_STATUS[0][0]
        ).values_list(
            'id',
            'first_name',
            'last_name',
            'email',
            'role__role_name'
        )
        try:
            user_member_mapping = UserMemberMapping.objects.get(
                is_active=True, user_id=_custom_user_id
            )
        except UserMemberMapping.DoesNotExist:
            print('UserMemberMapping.DoesNotExist')
            _user_department_mapping = None
        try:
            members_values_list = user_member_mapping.members.filter(
                # is_active=True
            ).values_list(
                'id',
                'first_name',
                'last_name',
                'email',
                'role__role_name'
            )
        except Exception as e:
            members_values_list = None
            print('userMemberMappingExpErr')
            print(e)
        try:
            _query_rows = list(
                set(list(chain(_query_rows, members_values_list)))
            )
        except Exception as e:
            print('concatenateQuerySetExpErr')
            print(e)

        for row in _query_rows:
            row_num += 1
            for col_num in range(len(row)):
                print("col_num", str(row[col_num]))
                ws.write(row_num, col_num, str(row[col_num]), font_style)

    @staticmethod
    def status_excel_list(ws):
        """this  status_excel_list used to collect status
        related data to store data
        """
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [
            'id',
            'status_name'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = TaskStatusMaster.objects.filter(
            is_active=True
        ).values_list('id', 'status_name')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num,
                         col_num,
                         str(row[col_num]),
                         font_style)

    def export_task_sample(self):
        """this export_task_sample method used to export
        the task sample sheet for use import the task sheet data.
        """
        _excel_fields, _excel_titles = self.task_fields, self.task_titles
        # response = HttpResponse(content_type=self.file_content_type)
        # response["Content-Disposition"] = self.import_sample_file_name
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="tasks.xls"'

        # all worksheet instance.
        wb = xlwt.Workbook(encoding="utf-8")
        task_detail_ws = wb.add_sheet("Sheet1")
        departments_ws = wb.add_sheet("departments")
        topics_ws = wb.add_sheet("topics")
        members_ws = wb.add_sheet("members")
        status_ws = wb.add_sheet("status")

        # all method call for collect the Excel data.
        self.task_details_data(task_detail_ws)
        # all dynamic department
        self.departments_excel_list(departments_ws, self.custom_user_id)
        # all dynamic topics list
        self.topics_excel_list(topics_ws, self.custom_user_id)
        # all dynamic member list
        self.members_excel_list(members_ws, self.custom_user_id)
        # all task status master data list
        self.status_excel_list(status_ws)

        wb.save(response)
        return response

    def _manage_last_msg(self):
        """this _manage_last_msg method used to manage
        the last task update messages
        """
        if len(self.task_update_list) >= 1:
            # self.msg = MSG['TASK_UPLOAD_SUCCESSFULLY'].replace("[FAILED]", 
            # str(len(self.exception_data_list)))
            self.msg = "Task has been added successfully"

    def matrix_rule_config(self, _data):
        """this matrix_rule_config method used to get
        the matrix rule as per request parameters
        """
        _matrix_rule_input = {
            "importance": _data.get("importance").capitalize(),
            "urgency": _data.get("urgency").capitalize(),
        }
        return MatrixDashboardService(
            auth_instance=self.auth_instance,
            matrix_rule_input=_matrix_rule_input
        ).assign_task_matrix()

    @staticmethod
    def convert_timestamp(_data):
        """
        this convert_timestamp_datetime method used to convert the all
        date timestamp to datetime format.
        """
        try:
            start_date = datetime.fromtimestamp(int(_data["start_date"] / 1000))
        except ValueError:
            start_date = None
        try:
            end_date = datetime.fromtimestamp(int(_data["end_date"] / 1000))
        except ValueError:
            end_date = None
        try:
            reminder = datetime.fromtimestamp(int(_data["reminder"] / 1000))
        except ValueError:
            reminder = None

        # return convert datetime
        return start_date, end_date, reminder

    # @staticmethod
    def convert_datetime(self, _data):
        """this convert_datetime method used to
        string format to datetime format
        """
        try:
            start_date = datetime.strptime(
                str(_data["start_date"]), self.date_format
            )
        except ValueError:
            start_date = None
        try:
            end_date = datetime.strptime(
                str(_data["end_date"]), self.date_format
            )
        except ValueError:
            end_date = None
        try:
            reminder = datetime.strptime(
                str(_data["reminder"]), self.date_format
            )
        except ValueError:
            reminder = None
        # convert string datetime
        return start_date, end_date, reminder

    def import_task_sheet_data(self):
        """
        this import_task_sheet_data methods used to import the task
        list into database with the assign members
        """
        for _data in self._json_input_data:
            # task owner from auth user
            _data["task_owner"] = self.auth_instance.user_auth.id

            # matrix rule from using importance and urgency medium
            matrix_type_config = self.matrix_rule_config(_data)
            if not matrix_type_config:
                self.exception_data_list.append(
                    {"matrix_type_config": MSG["MATRIX_ERROR_EXCEPTION"]}
                )
            _data["matrix_type_config"] = matrix_type_config

            # update all id from heading sheet
            try:
                _department_id = get_department_id_from_name(
                    _data["department"]
                )
                _data["department"] = _department_id
            except Exception as e:
                _data["department"] = _data.get("department", None)
                print("DepartmentExceptionErr")
                print(e)
            try:
                _data["status"] = (
                    _data["status_id"]
                    if _data["status_id"] else
                    None
                )
            except Exception as e:
                print("STATUSExceptionErr")
                print(e)
            try:
                _data["topic"] = (
                    _data["topic_id"]
                    if _data["topic_id"] else
                    None
                )
            except Exception as e:
                print("TopicExceptionErr")
                print(e)
            try:
                _data["estimate"] = _data.get("estimate_hour", None)
            except Exception as e:
                print("error")
                print(e)
            try:
                self.member_list = str(_data.get("members_id")).split(",")
            except Exception as e:
                self.success = False
                print("Exception")
                print(e)

            # update time from time stamp number
            try:
                start_date, end_date, reminder = self.convert_timestamp(_data)
                _data["start_date"] = (
                    start_date
                    if start_date else
                    _data.get("start_date", None)
                )
                _data["due_date"] = (
                    end_date
                    if end_date else
                    _data.get("end_date", None)
                )
                _data["reminder"] = (
                    reminder
                    if reminder else
                    _data.get("reminder", None)
                )
            except Exception as e:
                print("timeStampFormatErr")
                print(e)

            # this datetime convert the date time 
            try:
                start_date, end_date, reminder = self.convert_datetime(_data)
                _data["start_date"] = (
                    start_date
                    if start_date else
                    _data.get("start_date", None)
                )
                _data["due_date"] = (
                    end_date
                    if end_date else
                    _data.get("end_date", None)
                )
                _data["reminder"] = (
                    reminder
                    if reminder else
                    _data.get("reminder", None)
                )
            except Exception as e:
                print("timeStampFormatErr")
                print(e)

            # update members ids list and save data using serializers
            _data["members"] = self.member_list
            print("#######lastDateData", _data)
            task_serializer = TasksSerializer(data=_data)
            if task_serializer.is_valid(raise_exception=True):
                task_serializer.save()
                self.task_update_list.append(task_serializer.data["id"])
            else:
                self.success = False
                serializer_err_obj = SerializerErrorParser(str(task_serializer))
                key, err = serializer_err_obj()
                self.exception_data_list.append(
                    {"serializer_err": "".join([str(key), str(err)])}
                )

    def import_task_list(self):
        """this method use to import the task list from Excel sheet
        """
        # get custom user instance
        user_instance = get_user_instance(
            {"is_active": True, "auth_user": self.auth_instance}
        )
        if not user_instance:
            return self.success, self.final_response_dict, MSG["USER_NOT_FOUND"]

        # file extension check validation
        _file_extension = self.get_file_extension()
        if not _file_extension:
            return False, self.final_response_dict, MSG["UPLOAD_VALID_EXCEL"]

        # check file Extension is existed or not
        if str(_file_extension) in self.excel_file_extension:
            self.get_json_from_excel()

            if not self._json_input_data:
                return self.success, {}, "Please upload correct sheet"

            # all Excel sheet cell validation one by one
            for row, _data in enumerate(self._json_input_data):
                self.msg, self.success = APIValidation(

                ).check_invalid_data_for_task(row + 1, _data)
                if self.msg is not None:
                    return self.success, self.final_response_dict, self.msg

            # import task method
            self.import_task_sheet_data()

            # import push notification alert
            try:
                push_notification_instance = PushNotifications(
                    api_service_name="__IMPORTTASK__",
                    TO="admin",
                    user=user_instance.id,
                    user_notification_data={
                        "username": "".join(
                            [str(user_instance.first_name),
                             " ", str(user_instance.last_name)]
                        )
                    },
                )
                push_notification_instance()
            except Exception as e:
                print("NotificationErr")
                print(e)

            if self.success is False:
                return self.success, self.final_response_dict, self.msg

            # final response data with exception
            self.final_response_dict["exceptions"] = self.exception_data_list
            self.final_response_dict["task_list"] = self.task_update_list

            # last response msg manipulation for final response
            self._manage_last_msg()
            return self.success, self.final_response_dict, self.msg
