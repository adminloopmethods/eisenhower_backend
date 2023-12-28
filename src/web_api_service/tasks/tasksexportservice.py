# import csv module
import csv
from datetime import datetime

# import django modules
from django.http import HttpResponse

# import core modules
from core.api_response_parser import (bad_request_response, final_response,
                                      not_acceptable_response)
# task models
from task_management.models import Tasks
from web_api_service.helpers.all_config_func import \
    get_auth_instance_from_user_id


class ExportTasksService:
    """
    ExportTasksService

    ##
    https://djangotricks.blogspot.com/2019/02/how-to-export-data-to-xlsx-files.html
    ##
    https://blog.devgenius.io/building-your-own-export
    -and-import-data-into-excel-using-django-celery-pandas-%EF%B8%8F-with-784fd688e328
    """

    def __init__(self, **kwargs):
        self.auth_instance = kwargs.get("auth_instance", None)
        self.task_req_data = kwargs.get("task_req_data", None)
        self.task_list_params = kwargs.get("task_list_params", None)
        self.final_response = final_response()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self.language = None
        self._task_fields_list = [
            "task_name",  # 1
            "customer_name",  # 2
            "description",  # 3
            "start_date",  # 4
            "due_date",  # 5
            "estimate",  # 6
            # 'notes',  #7
            # 'comments', #8
            "reminder",  # 9
            "status_data",  # 10
            "department",  # 11
            "topic",  # 12
            "member",  # 13
            "task_owner",  # 14
            # 'matrix_type_config', #15
            "matrix_type",  # 16
            "importance",  # 17
            "urgency",  # 18
        ]
        self._task_sheet_title_list = [
            "Task Name",  # 1
            "Customer Name",  # 2
            "Description",  # 3
            "Start Date (mm/dd/yyyy)",  # 4
            "Due Date (mm/dd/yyyy)",  # 5
            "Estimate",  # 6
            # 'Notes', #7
            # 'Comments', #8
            "Reminder (mm/dd/yyyy)",  # 9
            "Status",  # 10
            "Department",  # 11
            "Topic",  # 12
            "Members",  # 13
            "Task Owner",  # 14
            # 'matrix_type_config', #15
            "Matrix Type",  # 16
            "importance",  # 17
            "urgency",  # 18
        ]
        self.file_name = "tasks_list"
        self.language = "ENG"
        # self.file_content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        # self.file_content_type = 'application/ms-excel'
        # self.file_content_type = 'application/vnd.ms-excel'
        self.file_content_type = 'text/csv'

    def task_value_manipulation(self, obj):
        """task_value_manipulation
        this task_value_manipulation method used to mainpulate the task values
        """
        try:
            if obj.customer_name == "" or obj.customer_name is None:
                obj.customer_name = "None"
        except Exception as e:
            print('objCustomerNameException')
            print(e)

        try:
            if obj.description == "" or obj.description is None:
                obj.description = "None"
        except Exception as e:
            print('objDescriptionException')
            print(e)

        try:
            if obj.estimate == "" or obj.estimate is None:
                obj.estimate = "None"
        except Exception as e:
            print('objEstimateException')
            print(e)

        try:
            if obj.topic == "" or obj.topic is None:
                obj.topic = "None"
        except Exception as e:
            print('objTopicException')
            print(e)

    def nested_getattr(self, obj, attribute, split_rule="__"):
        """
        This function is responsible for getting the nested record from the given obj parameter
        :param obj: whole item without splitting
        :param attribute: field after splitting
        :param split_rule:
        :return:
        """
        self.task_value_manipulation(obj)

        # all date time split
        try:
            obj.reminder = str(obj.reminder).split(" ")[0]
        except Exception as e:
            print('reminderFormatException')
            print(e)

        try:
            obj.due_date = str(obj.due_date).split(" ")[0]
        except Exception as e:
            print('dueDateFormatException')
            print(e)

        try:
            obj.start_date = str(obj.start_date).split(" ")[0]
        except Exception as e:
            print('startDateFormatException')
            print(e)

        # try:
        #     print('startdata--------------', obj.start_date.date(), type(obj.start_date))
        #     print('enddata--------------', obj.due_date.date(), type(obj.due_date))
        #     print('reminder--------------', obj.reminder.date(), type(obj.reminder))
        # except Exception as e:
        #     print(e)

        # try:
        #     obj.start_date = str(obj.start_date.date())
        # except Exception as e:
        #     obj.start_date = 'None'
        #     print(e)
        #
        # try:
        #     obj.reminder = str(obj.reminder.date())
        # except Exception as e:
        #     obj.reminder = 'None'
        #     print(e)
        #
        # try:
        #     obj.due_date = str(obj.due_date.date())
        # except Exception as e:
        #     obj.due_date = 'None'
        #     print(e)

        # obj.Start_date = str(obj.start_date.date())
        # obj.Due_date = str(obj.due_date.date())
        # obj.Reminder = str(obj.reminder.date())



        # if obj.start_date and obj.start_date != 'None':
        #     obj.Start_date = datetime.strptime(obj.start_date, "%Y-%m-%d").strftime('%d-%m-%Y')
        # else:
        #     obj.Start_date = "None"
        # if obj.due_date and obj.due_date != 'None':
        #     obj.Due_date = datetime.strptime(obj.due_date, "%Y-%m-%d").strftime('%d-%m-%Y')
        # else:
        #     obj.Due_date = "None"
        # if obj.reminder and obj.reminder != 'None':
        #     obj.Reminder = datetime.strptime(obj.reminder, "%Y-%m-%d").strftime('%d-%m-%Y')
        # else:
        #     obj.Reminder = "None"

        # datetime_format = "%d-%m-%Y, %I:%M %p"

        # try:
        #     start_date_time_string = obj.start_date.strftime(
        #         datetime_format
        #     )
        #     start_date_time_obj = datetime.strptime(
        #         str(start_date_time_string), datetime_format
        #     )
        #     print('444444', start_date_time_obj, type(start_date_time_obj))
        #     print(
        #         datetime.strptime(
        #             str(start_date_time_obj.date()), '%Y-%m-%d'
        #         ).strftime("%d-%m-%Y")
        #     )
        #     obj.Start_date = str(datetime.strptime(
        #                         str(start_date_time_obj.date()), '%Y-%m-%d'
        #                     ).strftime("%d-%m-%Y"))
        # except Exception as e:
        #     obj.Start_date = obj.start_date
        #     print('1startDate')
        #     print(e)

        # try:
        #     due_date_time_obj = obj.due_date.strftime(
        #         datetime_format
        #     )
        #     due_date_time_obj = datetime.strptime(
        #         str(due_date_time_obj), datetime_format
        #     )
        #     obj.Due_date = str(datetime.strptime(
        #                     str(due_date_time_obj.date()), '%Y-%m-%d'
        #                 ).strftime("%d-%m-%Y"))
        # except Exception as e:
        #     obj.Due_date = obj.due_date
        #     print('1DueDate')
        #     print(e)

        # try:
        #     reminder_time_obj = obj.reminder.strftime(
        #         datetime_format
        #     )
        #     reminder_time_obj = datetime.strptime(
        #         str(reminder_time_obj), datetime_format
        #     )
        #     obj.Reminder = str(datetime.strptime(
        #                     str(reminder_time_obj.date()), '%Y-%m-%d'
        #                 ).strftime("%d-%m-%Y"))
        # except Exception as e:
        #     obj.Reminder = obj.reminder
        #     print('1remindrDate')
        #     print(e)


        # print('startdate-enddate-reminder------')
        # print(obj.start_date, obj.due_date, obj.reminder)
        # print(type(obj.start_date), type(obj.due_date), type(obj.reminder))

        # obj.start_date, obj.due_date, obj.reminder = str(obj.start_date), str(obj.due_date), str(obj.reminder)


        # all many-to-many relationships members
        obj.member = ", ".join(
            [
                str(i.first_name) + " " + str(i.last_name)
                for i in obj.members.all().order_by("-created_at")
            ]
        )

        try:
            for _matrix_type_data in obj.matrix_type_config.task_type_config.all():
                try:
                    if str(self.language) == "ITL":
                        if _matrix_type_data.rule_name == "Importance":
                            obj.importance = _matrix_type_data.priority_status.priority_status_in_italian
                        if _matrix_type_data.rule_name == "Urgency":
                            obj.urgency = _matrix_type_data.priority_status.priority_status_in_italian
                    if str(self.language) == "ENG":
                        if _matrix_type_data.rule_name == "Importance":
                            obj.importance = _matrix_type_data.priority_status
                        if _matrix_type_data.rule_name == "Urgency":
                            obj.urgency = _matrix_type_data.priority_status
                except Exception as e:
                    print("ExceptionErrTemp")
                    print(e)
                    if _matrix_type_data.rule_name == "Importance":
                        obj.importance = _matrix_type_data.priority_status
                    if _matrix_type_data.rule_name == "Urgency":
                        obj.urgency = _matrix_type_data.priority_status
        except Exception as e:
            print("matrixConfigException")
            print(e)

        try:
            if str(self.language) == "ENG":
                obj.matrix_type = obj.matrix_type_config.matrix_type
            if str(self.language) == "ITL":
                obj.matrix_type = obj.matrix_type_config.matrix_type.matrix_rule_in_italian
        except Exception as e:
            print("ExpforErr")
            print(e)

        try:
            if str(self.language) == "ENG":
                obj.status_data = obj.status.status_name
            if str(self.language) == "ITL":
                obj.status_data = obj.status.status_name_in_italian
        except Exception as e:
            print("statusErrException")
            print(e)

        split_attr = attribute.split(split_rule)
        for attr in split_attr:
            if not obj:
                break
            obj = getattr(obj, attr)
        return obj

    def get_task_list_for_export(self):
        """this get_task_list_for_export method used to manage
        the task export service translation with data.
        """
        _ids_list = self.task_list_params.get("all_id").split(",")

        try:
            if len(_ids_list) == 1:
                self.auth_instance = get_auth_instance_from_user_id(
                    _ids_list[0])
        except Exception as e:
            self.auth_instance = None
            print("Exception")
            print(e)

        try:
            self.language = self.task_list_params.get("lang", "ENG")
        except Exception as e:
            print("Errors")
            print(e)

        try:
            self.language = self.auth_instance.user_auth.language
        except Exception as e:
            print("Errors")
            print(e)

        # try:
        #     task_queryset = (
        #         Tasks.objects.filter(
        #             Q(task_owner__id=self.auth_instance.user_auth.id)
        #             | Q(members__in=[self.auth_instance.user_auth.id]),
        #             is_deleted=False,
        #         )
        #         .order_by("created_at")
        #         .distinct()
        #     )
        # except Exception as e:
        #     print(e)
        #     task_queryset = None

        try:
            task_queryset = Tasks.objects.filter(
                members__in=[self.auth_instance.user_auth.id],
                is_deleted=False).order_by("created_at").distinct()
        except Exception as e:
            print(e)
            task_queryset = None

        if not task_queryset:
            task_queryset = Tasks.objects.filter(
                id__in=self.task_list_params.get("all_id").split(",")
            ).order_by("created_at")

        task_fields = self._task_fields_list
        fields = self._task_fields_list
        titles = self._task_sheet_title_list
        model = task_queryset.model

        response = HttpResponse(content_type=self.file_content_type)
        # force download
        response[
            "Content-Disposition"
        ] = "attachment; filename={}.csv".format(self.file_name)
        # the csv writer
        writer = csv.writer(response)
        if fields:
            headers = fields
            if titles:
                titles = titles
            else:
                titles = headers
        else:
            headers = []

            for field in model._meta.fields:
                headers.append(field.name)
            titles = headers

        # Writes the title for the file
        writer.writerow(titles)

        # write data rows
        for item in task_queryset:
            # a=str(item.start_date)
            writer.writerow(
                [self.nested_getattr(item, field) for field in headers]
            )

        return response
