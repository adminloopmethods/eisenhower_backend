from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG
# import business card services
from web_api_service.bcr.business_card_reader.business_card_services import (
    BusinessCardReader,
)
from web_api_service.helpers.all_config_func import get_user_instance


# import business card models


class UploadBusinessCardImages(APIView):
    """
    UserDetailsUpdateApi
    Usage: this endpoint used to update the profile details with media file.
    path: /api/v1/user/detail/update/
    method: PUT
    Authorization: YES
    Content-Type: MultiPartParser, FormParser
    request_data :
        first_name:Gourav
        last_name:Sharma
        mobile:8750752954
    Response: {
        "user_details": {
            "id": "7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
            "first_name": "Gourav",
            "last_name": "Sharma",
            "email": "govindsharma@gmail.com",
            "mobile": "8750752954",
            "mobile_with_isd": "918287694556",
            "isd": 91,
            "profile_picture": null,
            "department": "c5208922-52b0-4e8c-9498-367e9eed09a7"
        },
        "success": true,
        "message": "Done"
    }
    """

    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.business_card_request_data = {}

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
                message=API_RESPONSE_MSG["USER_NOT_FOUND"],
                success=False,
            )

        user_instance = get_user_instance(
            {"is_active": True, "auth_user": request.user}
        )
        if not user_instance:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                success=False,
                message=API_RESPONSE_MSG["USER_NOT_FOUND"],
            )

        self.business_card_request_data = request.data
        self.business_card_request_data._mutable = True

        business_card_result = BusinessCardReader(
            auth_user_instance=request.user,
            business_card_request_data=self.business_card_request_data,
        ).upload_business_card()

        if isinstance(business_card_result, str):
            return APIResponseParser.response(
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=business_card_result
            )

        if not business_card_result:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["PLEASE_PROVIDE_VALID_CARD_ID"],
                success=False
            )

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card",
            data=business_card_result,
            success=True
        )


class TestImagesUpload(APIView):
    """
    UserDetailsUpdateApi
    Usage: this endpoint used to update the profile details with media file.
    path: /api/v1/business/card/test/upload/
    method: POST
    Authorization: YES
    Content-Type: MultiPartParser, FormParser
    request_data :
        test_file:media_file
    Response: {
        "user_details": {
            "id": "7302fe63-e6bb-4e36-b9be-fcf6c26f7a4b",
            "first_name": "Gourav",
            "last_name": "Sharma",
            "email": "govindsharma@gmail.com",
            "mobile": "8750752954",
            "mobile_with_isd": "918287694556",
            "isd": 91,
            "profile_picture": null,
            "department": "c5208922-52b0-4e8c-9498-367e9eed09a7"
        },
        "success": true,
        "message": "Done"
    }
    """

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    # permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.business_card_request_data = {}

    def post(self, request):
        """this post method used to upload
        the business card image with upload the abby api call function

        Args:
            request (instance): in request instance we found the all
            type of request data
        """
        self.business_card_request_data = request.data
        self.business_card_request_data._mutable = True

        business_card_result = BusinessCardReader(
            business_card_request_data=self.business_card_request_data
        ).test_file_upload()

        if not business_card_result:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="test file failed",
                success=False,
            )

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card",
            data={"id": business_card_result},
            success=True,
        )
