from django.contrib.auth.models import User


from rest_framework import status

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin


from user.models import CustomUsers

from core.messages import API_RESPONSE_MSG

# import business card models
from cards.models import (
    CategoryGroupMaster,
    BusinessCardReaderManager,
    BusinessCardSocialLink,
)

from web_api_service.bcr.search_filters.serach_filter_service import (
    BusinessCardSearchFilter,
)

from core.api_response_parser import APIResponseParser

# import business card services
from web_api_service.bcr.business_card_reader.business_card_services import (
    BusinessCardReader,
)
from web_api_service.helpers.all_config_func import get_user_instance

from web_api_service.bcr.export.business_card_export_excel import ExportBusinessCards


class ExportBusinessCardList(APIView):
    """
    PATH: /api/v1/business/card/export/
    """

    def get(self, request):
        """
        Args:
            request (instance): this request instance used to manage
            the all type of api request
        Returns:
            media_file: this media file type is a excel file format with xlsx format
        """
        try:
            return ExportBusinessCards(
                business_card_id=self.request.query_params.get("id")
            ).export_business_cards()
        except Exception as e:
            print('ExportBusinessCardsExp')
            print(e)
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Data Not Found",
                success=False,
            )
