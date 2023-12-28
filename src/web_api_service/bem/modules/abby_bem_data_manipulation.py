from cards.models import BusinessCardAddress
from cards.models import BusinessCardDates
from cards.models import BusinessCardEmail
from cards.models import BusinessCardFax
from cards.models import BusinessCardJob
from cards.models import BusinessCardMobile
from cards.models import BusinessCardReaderManager
from cards.models import BusinessCardSocialNetwork
from cards.models import BusinessCardWeb

# import business card models
from cards.models import CategoryGroupMaster
from core.constants import MOBILE_TYPE
from web_api_service.bcr.abby_apis.abby_ocr_services import AbbyOcrReader

# import custom user
from web_api_service.bcr.business_card_reader.business_card_serializers import (
    BusinessCardReaderManagerSerializer,
)


class AbbyBusinessExpense:
    """
    BusinessCardReader
    """

    def __init__(self, **kwargs):
        self.business_card_instance = None
        self.auth_user_instance = kwargs.get("auth_user_instance", None)
        self.business_card_id = kwargs.get("business_card_id", None)
        self.business_card_data = kwargs.get("business_card_data", {})
        self.category_group_data = kwargs.get("category_group_data", {})
        self.card_data = kwargs.get("business_card_request_data", {})

        self._user_category_value_list = []

        # initiate the categoryGroupMaster Models
        self.category_group_entity = CategoryGroupMaster.objects.filter(
            is_active=True
        )

    def business_expense_update_by_abby_response(self, business_card_queryset):
        """this business_expense_update_by_abby_response method 
        used to update the abby response
        business_card_queryset: this query set help to manage the our BEM models 
        instance update, add, delete, and get the BCr card details
        new_abby_bem_response: {}
        """
        for business_card_read in business_card_queryset:
            abby_status_data, abby_response_msg = AbbyOcrReader(
                abby_response_id=business_card_read.abby_response_id,
                auth_user_instance=self.auth_user_instance,
            ).abby_retrieve_call()
            print('################################### @@abby_bem_status_data')
            print(abby_status_data)
            if abby_status_data:
                business_expense_data = {
                }
                self.update_business_expense_details_from_abby_response(
                    business_card_read.id,
                    business_card_data
                )



