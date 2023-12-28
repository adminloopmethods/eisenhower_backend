import csv
import operator
from datetime import datetime
from functools import reduce

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse

# import business card models
from cards.models import BusinessExpenseManager
from core.api_response_parser import bad_request_response
from core.api_response_parser import final_response
from core.api_response_parser import not_acceptable_response


class ExportBusinessExpense:
    """
    ExportTasksService

    ##
    https://djangotricks.blogspot.com/2019/02/how-to-export-data-to-xlsx-files.html
    ##
    https://blog.devgenius.io/building-your-own-export
    -and-import-data-into-excel-using-django-celery-pandas-%EF%B8%8F-with-784fd688e328
    # if self.business_card_id:
    #     business_card_queryset = self.business_card_manager_instance.filter(
    #                 id=self.business_card_id,
    #                 is_active=True)
    # else:
    #     business_card_queryset = self.business_card_manager_instance.filter(
                                is_active=True)
    """

    def __init__(self, **kwargs):
        self.project_base_url = settings.PROJECT_BASE_URL
        self.auth_user_instance = kwargs.get('auth_instance', None)
        self.expense_user_id = kwargs.get('expense_user_id', None)
        self.expense_type = kwargs.get('expense_type', None)
        self.start_date = kwargs.get('start_date', None)
        self.end_date = kwargs.get('end_date', None)
        self.created_at = kwargs.get('created_at', None)
        self.business_expense_ids = kwargs.get('business_expense_ids', None)
        self.business_expense_instance = BusinessExpenseManager.objects.filter()
        self.final_response = final_response()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self._business_expense_fields_list = [
            # 'expense_process_status',
            'expense_images',
            # 'expense_image',
            'merchant_name',
            'Purchased_on',
            'description',
            'amount',
            # 'submit_to',
            'expense_type',
            # 'reimbursed_on',
            'Submitted_on',
            # 'reimbursed_by',
            # 'reimbursed_method',
            'expense_capture_type',
            # 'is_card_retrived',
            # 'retrive_status',
            # 'reason_for_failed',
            'user'
        ]
        self._business_expense_sheet_title_list = [
            # 'expense_process_status',
            'expense_images',
            # 'expense_image',
            'merchant_name',
            'Purchased_on',
            'description',
            'amount',
            # 'submit_to',
            'expense_type',
            # 'reimbursed_on',
            'Submitted_on',
            # 'reimbursed_by',
            # 'reimbursed_method',
            'expense_capture_type',
            # 'is_card_retrived',
            # 'retrive_status',
            # 'reason_for_failed',
            'user'
        ]
        self.file_name = 'business_expense_list'
        # self.file_content_type = 'application/vnd.openxmlformats-officedocument'\
        # '.spreadsheetml.sheet'
        # self.file_content_type = 'application/ms-excel'
        self.file_content_type = 'application/vnd.ms-excel'
        self.file_content_type = 'text/csv'
        self.expense_filter_list = list()

    def nested_getattr(self, obj, attribute, split_rule='__'):
        """
        This function is responsible for getting the nested record from the
        given obj parameter.
        :param obj: whole item without splitting
        :param attribute: field after splitting
        :param split_rule:
        :return:
        """
        try:
            obj.expense_images = ''.join(
                [
                    self.project_base_url,
                    '/media/', str(obj.expense_image)
                ]
            )
        except Exception as e:
            print('businessImageException')
            print(e)

        try:
            if obj.purchased_on:
                datetime_obj = datetime.strptime(
                    str(obj.purchased_on),
                    '%Y-%m-%d'
                ).strftime("%d-%m-%Y")
                obj.Purchased_on = datetime_obj
            else:
                obj.Purchased_on = obj.purchased_on
        except Exception as e:
            print('ExpErr')
            print(e)

        try:
            if obj.submitted_on:
                datetime_obj = datetime.strptime(
                    str(obj.submitted_on),
                    '%Y-%m-%d'
                ).strftime("%d-%m-%Y")
                obj.Submitted_on = datetime_obj
            else:
                obj.Submitted_on = obj.submitted_on
        except Exception as e:
            print('ExpErr')
            print(e)

        split_attr = attribute.split(split_rule)
        for attr in split_attr:
            if not obj:
                break
            obj = getattr(obj, attr)

        return obj

    def create_filter_list(self):
        """this create_filter_list method used to create filter list
        :return:
        """
        if self.expense_type:
            self.expense_filter_list.append(Q(expense_type=self.expense_type))

        if self.start_date and self.end_date:
            self.expense_filter_list.append(
                Q(created_at__range=[self.start_date,
                                     self.end_date]))

    def business_expense_filter_qs(self):
        """this business expense filter method used to set the filter query 
        for export by filter
        """
        if len(self.expense_filter_list) > 0:
            _expense_filter_data = reduce(
                operator.and_,
                self.expense_filter_list
            )
            try:
                business_expense_queryset = (
                    self.business_expense_instance.filter(
                        id=self.business_expense_id,
                        is_active=True
                    ).filter(
                        self.expense_filter_list
                    ) if self.business_expense_id else
                    self.business_expense_instance.filter(
                        is_active=True
                    ).filter(
                        self.expense_filter_list
                    )
                )
            except Exception as e:
                business_expense_queryset = None
                print(e)

    def business_expense_qs(self):
        """this business_expense_qs method used to get the
        query set of business expense from using business expense id or simple 
        query set
        """
        try:
            return (
                self.business_expense_instance.filter(
                    user_id=self.expense_user_id,
                    is_active=True
                ) if self.expense_user_id else
                self.business_expense_instance.filter(is_active=True)
            )
        except Exception as e:
            print(e)
            business_expense_queryset = None

    def business_expense_using_ids(self):
        """this business_expense_using_ids method used to get the
        query set of business expense from using business expense id or simple 
        query set
        """
        try:
            return (
                self.business_expense_instance.filter(
                    id__in=self.business_expense_ids.split(','),
                    is_active=True) if self.business_expense_ids else
                self.business_expense_instance.filter(is_active=True)
            )
        except Exception as e:
            print(e)
            return None

    def export_business_expense(self):
        """export_business_expense method used to export
        the all business card detail in Excel format
        Returns: media_excel: Excel sheet file
        """
        # self.create_filter_list()
        business_expense_queryset = (
            self.business_expense_using_ids()
            if self.business_expense_ids else
            self.business_expense_qs()
        )

        if not business_expense_queryset:
            business_expense_queryset = self.business_expense_instance

        task_fields = self._business_expense_fields_list
        fields = self._business_expense_fields_list
        titles = self._business_expense_sheet_title_list
        business_expense_queryset = business_expense_queryset.order_by(
            '-created_at'
        )
        model = business_expense_queryset.model

        response = HttpResponse(content_type=self.file_content_type)
        # force download
        response[
            'Content-Disposition'
        ] = 'attachment; filename={}.csv'.format(self.file_name)
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
        for item in business_expense_queryset:
            # a=str(item.start_date)
            writer.writerow(
                [self.nested_getattr(item, field) for field in headers])

        return response
