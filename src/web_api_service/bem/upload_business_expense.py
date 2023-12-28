from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG
# import business card services
from web_api_service.bem.modules.upload_expense_file import UploadExpenseFile
from web_api_service.helpers.all_config_func import get_user_instance


# import business card models


class UploadBusinessExpenseImages(APIView):
    """
    UploadBusinessExpenseImages
    Usage: this endpoint used to update the profile details with media file.
    path: /api/v1/business/expense/upload/
    method: POST
    Authorization: YES
    Content-Type: MultiPartParser, FormParser
    request_data :
        expense_image: media_img.jpeg
    Response: {
        "business_expense": {
            "expense_image": "expense_images/806622677_155176_X6HBUO3.jpg"
        },
        "success": true,
        "message": "DONE"
    }
    """

    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.business_expense_request_data = {}

    def post(self, request):
        """this post method used to upload
        the business card image with upload the abby api call function

        Args:
            request (instance): in request instance we found the all
            type of request data
        """
        if not request.user:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                success=False)

        user_instance = get_user_instance({'is_active': True, 'auth_user': request.user})
        if not user_instance:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                success=False)

        self.business_expense_request_data = request.data
        self.business_expense_request_data._mutable = True

        business_expense_result = UploadExpenseFile(
            auth_user_instance=request.user,
            expense_data=self.business_expense_request_data
        ).upload_business_expense()

        if not business_expense_result:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['PLEASE_PROVIDE_VALID_CARD_ID'],
                success=False)

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname='business_expense',
            data=business_expense_result,
            success=True)
