from datetime import datetime

from cards.models import BusinessExpenseManager
from web_api_service.bcr.business_card_reader.update_business_card_details import \
    UpdateBusinessCardDetails
from web_api_service.bem.modules.abby_bem_data_manipulation import \
    AbbyBusinessExpense
from web_api_service.bem.modules.serializers import (
    BusinessExpenseManagerSerializer,
)
from web_api_service.bem.modules.serializers import (
    BusinessExpenseManagerUpdateSerializer,
)


class BusinessExpenseDetail:
    """
    BusinessExpenseDetail
    """

    def __init__(self, **kwargs):
        self.auth_user_instance = kwargs.get('auth_user_instance', None)
        self.business_expense_id = kwargs.get('business_expense_id', None)
        self.business_expense_data = kwargs.get('business_expense_data', None)
        self.business_expense_instance = None
        self.submit_to = None
        self.expense_process_status = None
        self.description = None
        self.expense_image = None

    def expense_list(self):
        """this expense_list method used to get the
        all business card expense list from models
        """
        business_expense_qs = BusinessExpenseManager.objects.filter(
            user=self.auth_user_instance.user_auth,
            is_active=True).order_by('-created_at')
        if not business_expense_qs:
            return None

        # # for every time failed status
        try:
            business_expense_queryset = BusinessExpenseManager.objects.filter(
                user=self.auth_user_instance.user_auth,
                is_card_retrived=False,
                retrive_status="initiate",
                is_active=True
            )
            UpdateBusinessCardDetails(
                auth_user_instance=self.auth_user_instance
            ).business_expense_update_by_abby_response(
                business_expense_queryset
            )
        except Exception as e:
            print("BusinessExpenseManagerErr")
            print(e)

        try:
            return BusinessExpenseManagerSerializer(
                business_expense_qs, many=True
            ).data
        except Exception as e:
            print('ExpenseListSerializerErr')
            print(e)
            return None

    def get_business_expense_instance(self):
        """this get_business_expense_instance method used to
        get the business expense instance
        """
        try:
            self.business_expense_instance = BusinessExpenseManager.objects.get(
                user_id=self.auth_user_instance.user_auth.id,
                id=self.business_expense_id,
                is_active=True)
        except BusinessExpenseManager.DoesNotExist:
            print('BusinessExpenseManager.DoesNotExist')
            self.business_expense_instance = None

    def expense_detail(self):
        """this expense_detail method used to get the business card
        details by according a valid id
        """
        self.get_business_expense_instance()
        if not self.business_expense_instance:
            return None
        try:
            return BusinessExpenseManagerSerializer(
                self.business_expense_instance
            ).data
        except Exception as e:
            print('DictSerializerErr')
            print(e)
            return None

    def update_submitted_to(self, business_expense_data):
        """this update_submitted_to method used to update the submit to 
        values using frontend null and none values handled
        """
        if business_expense_data['submit_to']:
            self.submit_to = business_expense_data['submit_to']
            self.expense_process_status = 'submitted'
        if (business_expense_data['submit_to'] == 'null' 
                or business_expense_data['submit_to'] is None):
            self.submit_to = None
            self.expense_process_status = 'drafted'

    def update_expense_description(self, business_expense_data):
        """this update_expense_description update the description detail using 
        frontend null handle values
        """
        if business_expense_data['description']:
            self.description = business_expense_data['description']
        if (business_expense_data['description'] == 'null'
                or business_expense_data['description'] is None):
            self.description = None

    def create_business_expense_manager(self, business_expense_data):
        """this create_business_expense_manager method used to create new 
        record for bem
        """
        try:
            self.update_submitted_to(business_expense_data)
        except Exception as e:
            print('submitExpErr')
            print(e)

        try:
            self.update_expense_description(business_expense_data)
        except Exception as e:
            print('submitExpErr')
            print(e)

        business_expense_data['submit_to'] = self.submit_to
        business_expense_data['user'] = self.auth_user_instance.user_auth.id
        business_expense_data['retrive_status'] = 'retrive'
        business_expense_data['is_card_retrived'] = True
        business_expense_data[
            'expense_process_status'
        ] = self.expense_process_status
        business_expense_data['expense_capture_type'] = 'manual'
        business_expense_data['is_active'] = True
        business_expense_data['description'] = self.description

        expense_serializer = BusinessExpenseManagerUpdateSerializer(
            data=business_expense_data
        )
        if expense_serializer.is_valid(raise_exception=True):
            expense_serializer.save()
            return expense_serializer.data
        else:
            return None

    def update_expense_details(self):
        """this update_expense_details method used to update
        the business card detail
        """
        self.business_expense_id = self.business_expense_data.pop('id')[0]

        try:
            datetime_obj = datetime.strptime(
                self.business_expense_data.get('date', None),
                '%d-%m-%Y'
            )

            self.business_expense_data[
                'purchased_on'
            ] = datetime_obj.strftime("%Y-%m-%d")
            # self.business_expense_data[
            #     'purchased_on'
            # ] = self.business_expense_data.get('date', None)
        except Exception as e:
            print('purchasedOnExceptionErr')
            print(e)
        try:
            if self.business_expense_id == 'null':
                self.business_expense_id = None
        except Exception as e:
            print('Err')
            print(e)

        self.get_business_expense_instance()
        if not self.business_expense_instance:
            return self.create_business_expense_manager(
                self.business_expense_data
            )
        # self.business_card_id = self.business_card_data.pop('id')

        try:
            if (self.business_expense_data.get('expense_image') is None
                    or self.business_expense_data.get('expense_image') == 'null'
                    or self.business_expense_data.get('expense_image') == ''):
                self.expense_image = self.business_expense_data.pop(
                    'expense_image'
                )
        except Exception as e:
            print('popTheImageFileFromFormData')
            print(e)

        try:
            if (self.business_expense_data.get('description') is None
                    or self.business_expense_data.get('description') == 'null'):
                self.description = None
            else:
                self.description = self.business_expense_data.get('description')
        except Exception as e:
            print('popTheImageFileFromFormData')
            print(e)

        try:
            if self.business_expense_data['submit_to']:
                self.submit_to = self.business_expense_data['submit_to']
            if (self.business_expense_data['submit_to'] == 'null'
                    or self.business_expense_data['submit_to'] is None):
                self.submit_to = None
        except Exception as e:
            print('submitTomData')
            print(e)

        self.business_expense_data['description'] = self.description
        self.business_expense_data['submit_to'] = self.submit_to

        expense_serializer = BusinessExpenseManagerUpdateSerializer(
            self.business_expense_instance,
            data=self.business_expense_data,
            partial=True)
        if expense_serializer.is_valid(raise_exception=True):
            expense_serializer.save()
            return expense_serializer.data
        else:
            return None
