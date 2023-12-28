# import business card models
import datetime
import operator
from datetime import datetime
from datetime import timedelta
# reduce and complex queryset module
from functools import reduce

from django.db.models import Q

from cards.models import BusinessExpenseManager
#  import serializers
from web_api_service.bem.modules.serializers import \
    BusinessExpenseManagerSerializer


class BusinessExpenseSearchFilter:
    """
    BusinessCardReader
    """

    def __init__(self, **kwargs):
        self.business_card_instance = None
        self.auth_user_instance = kwargs.get('auth_user_instance', None)
        self.business_expense_search_data = kwargs.get(
            'business_expense_search_data', None
        )
        self.filter_data = kwargs.get('business_expense_filter_data', {})
        self.expense_qs = None
        self.expense_filter_list = list()
        self.start_date = None
        self.end_date = None

    @staticmethod
    def business_expense_data(business_card_expense_queryset):
        """this  business_expense_data method used to collect serializers data
        """
        return BusinessExpenseManagerSerializer(
            business_card_expense_queryset, many=True
        ).data

    def business_expense_search_list(self):
        """this business_card_list method used to get the
        all business card list from models
        """
        if (self.business_expense_search_data == ""
                or self.business_expense_search_data is None):
            self.expense_qs = BusinessExpenseManager.objects.filter(
                user=self.auth_user_instance.user_auth,
                is_active=True).order_by('-created_at')

        if self.business_expense_search_data:
            self.expense_qs = BusinessExpenseManager.objects.filter(
                user=self.auth_user_instance.user_auth,
                merchant_name__istartswith=self.business_expense_search_data,
                is_active=True).order_by('-created_at')

        if not self.expense_qs:
            return None

        try:
            return self.business_expense_data(self.expense_qs)
        except Exception as e:
            print('BusinessExpenseErr')
            print(e)
            return None

    def business_expense_filter_list_old(self):
        """this business_expense_filter_list method used to get
        the all business card filter data according to the request
        """
        # business_card_expense_queryset = BusinessExpenseManager.objects.filter(
        #     user=self.auth_user_instance.user_auth,
        #     is_active=True).select_related()

        expense_qs = BusinessExpenseManager.objects.filter(
            user=self.auth_user_instance.user_auth,
            is_active=True).order_by('-created_at')

        if not expense_qs:
            return None

        if self.business_expense_filter_data.get('sort_by', None):
            try:
                if (
                        self.business_expense_filter_data['sort_by'] == 'asc'
                        or self.filter_data['sort_by'] == 'ascending'
                ):
                    expense_qs = expense_qs.order_by('merchant_name')
                if (
                        self.business_expense_filter_data['sort_by'] == 'dsc'
                        or self.filter_data['sort_by'] == 'decending'
                ):
                    expense_qs = expense_qs.order_by('-merchant_name')
            except Exception as e:
                print('SortByException')
                print(e)

        if self.business_expense_filter_data.get('date', None):
            try:
                datetime_obj = datetime.strptime(
                    self.business_expense_filter_data['date'],
                    "%Y-%m-%dT%H:%M:%S.%f%z"
                )
                expense_qs = expense_qs.filter(
                    purchased_on=datetime_obj.date()
                )
            except Exception as e:
                print('DateFilterException')
                print(e)

        if self.business_expense_filter_data.get('type', None):
            try:
                expense_qs = expense_qs.filter(
                    expense_type_id=self.filter_data['type']
                )
            except Exception as e:
                print('ExpenseTypeFilterException')
                print(e)

        try:
            return self.business_expense_data(expense_qs)
        except Exception as e:
            print('BusinessExpenseErr')
            print(e)
            return None

    def create_filter_list(self):
        """this create_filter_list method used to create filter 
        list using frontend request
        """
        if self.filter_data.get('type'):
            self.expense_filter_list.append(
                Q(expense_type_id=self.filter_data.get('type', None))
            )
        if self.filter_data.get('range'):
            if self.filter_data.get('range') == '1':
                self.expense_filter_list.append(
                    Q(created_at__date=datetime.now() - timedelta(days=1))
                )
            if self.filter_data.get('range') == '7':
                self.expense_filter_list.append(
                    Q(created_at__date__gte=datetime.now() - timedelta(days=7))
                )
            if self.filter_data.get('range') == '30':
                self.expense_filter_list.append(
                    Q(created_at__date__gte=datetime.now() - timedelta(days=30))
                )
            if self.filter_data.get('range') == 'custom_date':
                try:
                    datetime_obj = datetime.strptime(
                        self.filter_data.get('start_date'),
                        '%d-%m-%Y'
                    )
                    self.start_date = datetime_obj.strftime("%Y-%m-%d")
                except Exception as e:
                    print('startDateErr')
                    print(e)
                try:
                    datetime_obj = datetime.strptime(
                        self.filter_data.get('end_date'),
                        '%d-%m-%Y'
                    )
                    self.end_date = datetime_obj.strftime("%Y-%m-%d")
                except Exception as e:
                    print('endDateErr')
                    print(e)
                if self.start_date or self.end_date:
                    self.expense_filter_list.append(
                        Q(created_at__date=self.start_date)
                    )
                if self.end_date or self.start_date is None:
                    self.expense_filter_list.append(
                        Q(created_at__date=self.end_date)
                    )
                if self.start_date and self.end_date:
                    self.expense_filter_list.append(
                        Q(created_at__date__range=[self.start_date,
                                                   self.end_date])
                    )

    def business_expense_filter_list(self):
        """this business_expense_filter_list method used to get
        the all business card filter data according to the request
        """
        expense_qs = BusinessExpenseManager.objects.filter(
            user=self.auth_user_instance.user_auth,
            is_active=True).order_by('-created_at')

        if not expense_qs:
            return None

        self.create_filter_list()
        if len(self.expense_filter_list) > 0:
            _expense_filter_data = reduce(
                operator.and_,
                self.expense_filter_list
            )
            try:
                expense_qs = expense_qs.filter(_expense_filter_data)
            except Exception as e:
                print('expenseFilterErr')
                print(e)
        else:
            expense_qs = expense_qs

        try:
            return self.business_expense_data(expense_qs)
        except Exception as e:
            print('BusinessExpenseErr')
            print(e)
            return None
