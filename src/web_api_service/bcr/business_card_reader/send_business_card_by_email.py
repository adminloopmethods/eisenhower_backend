from itertools import chain

from cards.models import BusinessCardAddress
from cards.models import BusinessCardDates
from cards.models import BusinessCardEmail
from cards.models import BusinessCardFax
from cards.models import BusinessCardJob
from cards.models import BusinessCardMobile
from cards.models import BusinessCardNotes
from cards.models import BusinessCardReaderManager
from cards.models import BusinessCardSocialNetwork
from cards.models import BusinessCardWeb

# import business card models
from cards.models import CategoryGroupMaster
from cards.models import UserCategoryGroupMaster
from configuration.models import TestFilesUploadForRequest
from core.constants import ACCESS_STATUS

# import customuser
from user.models import CustomUsers
from web_api_service.bcr.abby_apis.abby_ocr_services import AbbyOcrReader

#  import serializers
from web_api_service.bcr.business_card_reader.business_card_serializers import (
    BusinessCardReaderManagerSerializer,
)
from web_api_service.bcr.business_card_reader.business_card_serializers import (
    CategoryGroupMastersSerializer,
)

# mailer notification module
from web_api_service.notification.mailer.sender import Mailer


class BusinessCardSender:
    """
    BusinessCardReader
    """

    def __init__(self, **kwargs):
        self.mailer_parser_data = None
        self.business_card_obj = None
        self.business_card_instance = None

        self.auth_user_instance = kwargs.get("auth_user_instance", None)
        self.business_card_id = kwargs.get("business_card_id", None)
        self.business_card_data = kwargs.get("business_card_data", {})
        self.category_group_data = kwargs.get("category_group_data", {})
        self.card_data = kwargs.get("business_card_request_data", {})

        # for abby service attrs
        self.data_set_type = ""
        self.service_function = "recognition"
        self.application_type = "BCM"
        self._user_category_value_list = []
        self.email_html_template = "emailer/businsess_card.html"

        # init
        self.category_group_entity = CategoryGroupMaster.objects.filter(is_active=True)

    def collect_business_card_data(self):
        """this collect_business_card_data method used to send
        business card using email

        args: None and self

        return: response: {}
        """
        return BusinessCardReaderManagerSerializer(self.business_card_obj).data

    def card_send_by_email(self):
        """this card_send_by_email method used to send business card using email

        args: self body {'business_card_id': 43}

        return: response: {}
        """
        try:
            self.business_card_obj = BusinessCardReaderManager.objects.get(
                id=self.business_card_data["business_card_id"],
                user=self.auth_user_instance.user_auth,
                is_active=True,
            )
        except BusinessCardReaderManager.DoesNotExist:
            print("BusinessCardReaderManager.DoesNotExist")
            self.business_card_obj = None

        if not self.business_card_obj:
            return None

        self.mailer_parser_data = {
            "business_card_data": self.collect_business_card_data(),
            "email_html_template": self.email_html_template,
            "notification_data": {
                "username": self.auth_user_instance.user_auth.email,
            },
            "template_data": self.collect_business_card_data(),
            "sender_emails": self.auth_user_instance.user_auth.email,
            "api_service_name": "SEND_CARD_TEXT",
            "notification_to": "bcr_user",
            "user": self.auth_user_instance.user_auth.id,
        }

        _mailer = Mailer(**self.mailer_parser_data)
        _mailer()

        return True
