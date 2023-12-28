from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG
from web_api_service.bcr.search_filters.serach_filter_service import (
    BusinessCardSearchFilter,
)

# import business card services
from web_api_service.helpers.all_config_func import get_user_instance


# import business card models


class BusinessCardSearch(LoggingMixin, APIView):
    """
    BusinessCardSearch
    Method: GET
    Authorization: YES
    path: /api/v1/business/card/search/?q=tes
    response: {
    "business_card_list": [
        {
            "id": "f01d162d-fe89-4d46-9cdc-d924c2557666",
            "business_image": "/media/business_card_images/806630449_140265.jpg",
            "title": "test for demo",
            "first_name": "test for demo",
            "second_name": "test for demo",
            "last_name": "test for demo",
            "suffix": "test for demo",
            "company_name": "test for demo",
            "telephone_office": "test for demo",
            "telephone_mobile": "test for demo",
            "fax": "test for demo",
            "telephone_home": "test for demo",
            "e_mail": "test for demo",
            "country": "test for demo",
            "city": "test for demo",
            "street": "test for demo",
            "postal_code": "test for demo",
            "web": "test for demo",
            "facebook": "test for demo",
            "category_group": null,
            "category_group_data": {},
            "color_hex_code": "#000000"
        }
    ],
    "success": true,
    "message": "DONE"
    }
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """get the business card list"""
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
                message=API_RESPONSE_MSG["USER_NOT_FOUND"],
                success=False,
            )

        business_card_list = BusinessCardSearchFilter(
            auth_user_instance=request.user,
            business_card_search_data=request.query_params.get("q"),
        ).business_card_search_list()
        if not business_card_list:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["No_ACTIVE_DATA"],
                success=False,
            )
        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card_list",
            data=business_card_list,
            success=True,
        )


class BusinessCardFilter(LoggingMixin, APIView):
    """
    BusinessCardFilter
    Authorization: YES
    method: GET
    path: /api/v1/business/card/filter/
    request_body: {
        "category_group_id": "Water mixer",
        "sort_by": "asc"
    }
    response: {
    "business_card_list": [
        {
            "id": "9a516fd8-ed88-4db3-80e8-f9ac76511313",
            "business_image": "/media/business_card_images/Sample_Results_JXLhff7.png",
            "title": "demo",
            "first_name": "test",
            "second_name": "test",
            "last_name": "sample",
            "suffix": null,
            "company_name": "loop it methods pvt ltd",
            "telephone_office": "08287694556",
            "telephone_mobile": null,
            "fax": null,
            "telephone_home": null,
            "e_mail": "Joy@gmail.com",
            "country": "India",
            "city": "New Delhi",
            "street": "Safdarjung enclave new Delhi Delhi",
            "postal_code": "110051",
            "web": null,
            "facebook": null,
            "category_group": "c5f7ac4d-a3f7-4856-8c69-193e8d46febe",
            "category_group_data": {
                "id": "c5f7ac4d-a3f7-4856-8c69-193e8d46febe",
                "category_name": "Water mixer",
                "color_hex_code": "#ff0000"
            },
            "color_hex_code": "#ff0000"
        }
        ],
        "success": true,
        "message": "DONE"
    }
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """post the filter request and get the response according to filter data"""
        if not request.data:
            return APIResponseParser.response(
                message=API_RESPONSE_MSG["REQUEST_NOT_FOUND"],
                status_code=status.HTTP_400_BAD_REQUEST,
                success=False,
            )

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
                message=API_RESPONSE_MSG["USER_NOT_FOUND"],
                success=False,
            )

        business_card_list = BusinessCardSearchFilter(
            auth_user_instance=request.user, business_card_filter_data=request.data
        ).business_card_filter_list()
        if not business_card_list:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["No_ACTIVE_DATA"],
                success=False,
            )
        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card_list",
            data=business_card_list,
            success=True,
        )
