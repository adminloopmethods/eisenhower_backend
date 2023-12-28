import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG

# import business card services
from web_api_service.bcr.business_card_reader.business_card_services import (
    BusinessCardReader,
)
from web_api_service.helpers.all_config_func import get_user_instance


# import business card models


class BusinessCardQrCardDetail(LoggingMixin, APIView):
    """
    BusinessCardQrCardDetail
    Authorization: YES
    path: /api/v1/business/card/qr/code/
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
            },
            {
                "id": "9a516fd8-ed88-4db3-80e8-f9ac76511313",
                "business_image": "/media/business_card_images/Sample_Results_JXLhff7.png",
                "title": null,
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
        "message": "DONE"json.dumps(business_card_detail)
    }
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """get the business card list"""
        if not request.query_params:
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
                sdfstatus_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["USER_NOT_FOUND"],
                success=False,
            )

        if not request.query_params.get("id"):
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["PLEASE_PROVIDE_BUSINESS_CARD_ID"],
                success=False,
            )

        business_card_detail = BusinessCardReader(
            auth_user_instance=request.user,
            business_card_id=request.query_params.get("id"),
        ).qr_code_business_card_detail()

        print("!" * 100, business_card_detail)
        print("#" * 100, type(business_card_detail))
        print("1" * 100, str(json.dumps(business_card_detail)))

        # Create an empty string
        # empty_str = ""
        # Convert the dictionary to a string
        # using for loop and items() function

        qr_data_dict = dict()
        dictionary = json.loads(json.dumps(business_card_detail))

        # print('----------------------> dictionary', dictionary)
        # for qr_key, qr_value in dictionary.items():
        # print('pointerloop', data)
        # qr_data_dict['first_name'] = data['first_name']
        # qr_data_dict['second_name'] = data['second_name']
        # qr_data_dict['last_name'] = data['last_name']
        # qr_data_dict['suffix'] = data['suffix']
        # qr_data_dict['company_name'] = data['company_name']
        # qr_data_dict['telephone_office'] = data['telephone_office']
        # qr_data_dict['telephone_mobile'] = data['telephone_mobile']
        # qr_data_dict['fax'] = data['fax']
        # qr_data_dict['telephone_home'] = data['telephone_home']
        # qr_data_dict['e_mail'] = data['e_mail']
        # qr_data_dict['country'] = data['country']
        # qr_data_dict['city'] = data['city']
        # qr_data_dict['street'] = data['street']
        # qr_data_dict['postal_code'] = data['postal_code']
        # qr_data_dict['web'] = data['web']
        # qr_data_dict['facebook'] = data['facebook']
        # qr_data_dict['category_group'] = data['category_group']
        # qr_data_dict['color_hex_code'] = data['color_hex_code']
        # qr_data_dict['department'] = data['department']
        # qr_data_dict['prefix'] = data['prefix']
        # qr_data_dict['position'] = data['position']
        # qr_data_dict['email_work'] = data['email_work']
        # qr_data_dict['email_personal'] = data['email_personal']
        # qr_data_dict['contact_number_personal'] = data['contact_number_personal']
        # qr_data_dict['contact_number_work'] = data['contact_number_work']
        # qr_data_dict['website'] = data['website']
        # qr_data_dict['region'] = data['region']
        # qr_data_dict['zip_code'] = data['zip_code']
        # qr_data_dict[qr_key] = qr_value

        print("QRRRRRRRRRRRRCode", qr_data_dict)

        empty_str = ""
        for key, value in dictionary.items():
            empty_str += str(key) + ": " + str(value) + ", "
        print(type(empty_str))
        print(empty_str)

        empty_str = empty_str.replace("[", "")
        empty_str = empty_str.replace("]", "")
        empty_str = empty_str.replace("{", "")
        empty_str = empty_str.replace("}", "")

        if not business_card_detail:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["PLEASE_PROVIDE_VALID_CARD_ID"],
                success=False,
            )

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card_detail",
            data=empty_str,
            success=True,
        )
