from _thread import start_new_thread

from cards.models import BusinessExpenseManager
from web_api_service.bcr.abby_apis.abby_ocr_services import AbbyOcrReader


class UploadExpenseFile:
    def __init__(self, **kwargs):
        self.auth_user_instance = kwargs.get('auth_user_instance', None)
        self.expense_data = kwargs.get('expense_data', None)
        # for abby service attrs-
        self.data_set_type = ""
        self.service_function = "recognition"
        self.application_type = "BEM"

    def upload_business_expense(self):
        """this upload_business_card method used to upload
        the business card image in bcr db
        """
        business_expense_create = BusinessExpenseManager.objects.create(
            retrive_status='initiate',
            user_id=self.auth_user_instance.user_auth.id,
            expense_image=self.expense_data.get('expense_image', None),
            expense_capture_type='automated'
        )

        if not business_expense_create:
            return None

        try:
            _abby_ocr_obj = AbbyOcrReader(
                business_image=business_expense_create.expense_image.path,
                business_image_name=business_expense_create.expense_image.name,
                application_type=self.application_type,
                service_function=self.service_function,
                data_set_type=self.data_set_type,
                auth_user_instance=self.auth_user_instance,
                business_expense_id=business_expense_create.id
            )
            _abby_ocr_obj.upload_business_expense()
            # start_new_thread(_abby_ocr_obj.upload_business_expense, ())
        except Exception as e:
            print("AbbyOcrForBemErr")
            print(e)
            return str(e)

        return {
            'expense_image': str(business_expense_create.expense_image)
        }
