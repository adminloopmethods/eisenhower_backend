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
from web_api_service.bcr.business_card_reader.send_business_card_by_email import (
    BusinessCardSender,
)
from web_api_service.bcr.business_card_reader.update_business_card_details import (
    UpdateBusinessCardDetails,
)
from web_api_service.helpers.all_config_func import get_user_instance


# import business card models


class BusinessCardList(LoggingMixin, APIView):
    """
    BusinessCardList
    Authorization: YES
    path: /api/v1/business/card/list/
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

        business_card_list = BusinessCardReader(
            auth_user_instance=request.user
        ).business_card_list()
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


class BusinessCardDetail(LoggingMixin, APIView):
    """
    BusinessCardDetails
    Authorization: YES
    method: GET
    path: /api/v1/business/card/detail/?id=9a516fd8-ed88-4db3-80e8-f9ac76511313
    response: {
        "business_card_detail": {
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
            "category_data": {
                "id": "c5f7ac4d-a3f7-4856-8c69-193e8d46febe",
                "category_name": "Water mixer",
                "color_hex_code": "#ff0000"
            },
            "color_hex_code": "#ff0000",
            "user": "a8c1c071-153c-459b-97a0-e6a5e702b3a7",
            "is_card_retrived": true,
            "retrive_status": "retrive",
            "reason_for_failed": null,
            "created_at": "2022-12-10T14:48:09.793510Z",
            "prefix": null,
            "department": null,
            "position": null,
            "email_work": null,
            "email_personal": null,
            "contact_number_personal": null,
            "contact_number_work": null,
            "website": null,
            "address_type": null,
            "region": null,
            "zip_code": null,
            "address": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:00:05.611651Z",
                    "updated_at": "2022-12-19T12:00:05.611672Z",
                    "is_active": true,
                    "type": "company",
                    "street": "Safdarjung enclave new Delhi Delhi",
                    "city": "New Delhi",
                    "region": "Delhi",
                    "country": "India",
                    "zip_code": "110051",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                },
                {
                    "id": 2,
                    "created_at": "2022-12-20T08:23:48.683742Z",
                    "updated_at": "2022-12-20T08:23:48.683763Z",
                    "is_active": true,
                    "type": "home",
                    "street": "Safdarjung enclave new Delhi Delhi",
                    "city": "New Delhi",
                    "region": "Delhi",
                    "country": "India",
                    "zip_code": "110051",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ],
            "social_network": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:06:32.847766Z",
                    "updated_at": "2022-12-19T12:06:32.847800Z",
                    "is_active": true,
                    "type": "facebook",
                    "social_network_value": "fb,comss",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                },
                {
                    "id": 2,
                    "created_at": "2022-12-19T12:06:50.051191Z",
                    "updated_at": "2022-12-19T12:06:50.051211Z",
                    "is_active": true,
                    "type": "linkedin",
                    "social_network_value": "linkedlinked",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ],
            "emails": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:04:31.933694Z",
                    "updated_at": "2022-12-19T12:04:31.933715Z",
                    "is_active": true,
                    "type": "work",
                    "email_value": "pycodertesting@gmail.com",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ],
            "mobile_numbers": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:05:36.341471Z",
                    "updated_at": "2022-12-19T12:05:36.341507Z",
                    "is_active": true,
                    "type": "work",
                    "mobile_value": "8750758938",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ],
            "faxs": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:05:03.780408Z",
                    "updated_at": "2022-12-19T12:05:03.780439Z",
                    "is_active": true,
                    "type": "work",
                    "fax_value": "loopfaxsampless",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ],
            "jobs": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:07:25.699238Z",
                    "updated_at": "2022-12-19T12:07:25.699257Z",
                    "is_active": true,
                    "type": "company",
                    "job_value": "loopmethods.com",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                },
                {
                    "id": 2,
                    "created_at": "2022-12-19T12:07:39.180615Z",
                    "updated_at": "2022-12-19T12:07:39.180638Z",
                    "is_active": true,
                    "type": "position",
                    "job_value": "developer",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                },
                {
                    "id": 3,
                    "created_at": "2022-12-19T12:07:53.652423Z",
                    "updated_at": "2022-12-19T12:07:53.652443Z",
                    "is_active": true,
                    "type": "department",
                    "job_value": "development",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ],
            "dates": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:02:49.754717Z",
                    "updated_at": "2022-12-19T12:02:49.754744Z",
                    "is_active": true,
                    "type": "dateofbirth",
                    "date": "2022-12-14T16:30:00Z",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ],
            "webs": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:07:08.606568Z",
                    "updated_at": "2022-12-19T12:07:08.606603Z",
                    "is_active": true,
                    "type": "work",
                    "website": "https://bitbucket.org",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ],
            "notes": [
                {
                    "id": 1,
                    "created_at": "2022-12-19T12:05:55.178741Z",
                    "updated_at": "2022-12-19T12:05:55.178774Z",
                    "is_active": true,
                    "type": "fair",
                    "notes": "test of tests",
                    "created_by": 1,
                    "updated_by": 1,
                    "business_card": "9a516fd8-ed88-4db3-80e8-f9ac76511313"
                }
            ]
        },
        "success": true,
        "message": "DONE"
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
                status_code=status.HTTP_400_BAD_REQUEST,
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
        ).business_card_detail()
        if not business_card_detail:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["PLEASE_PROVIDE_VALID_CARD_ID"],
                success=False,
            )

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card_detail",
            data=business_card_detail,
            success=True,
        )


class UpdateBusinessCardDetail(LoggingMixin, APIView):
    """
    UpdateBusinessCardDetail
    Authorization: YES
    Method: PUT
    path: /api/v1/business/card/update/
    request: {
        "id": "f01d162d-fe89-4d46-9cdc-d924c2557666",
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
        "address":[
            {
                "type" :"company",
                "street": "Safdarjung enclave new Delhi seelampur delhi",
                "city": "Neww Delhi",
                "region": "North",
                "country": "India",
                "zip_code": "110051"
            },
            {
                "type": "home",
                "street": "Safdarjung enclave new Delhi seelasssmpur delhi",
                "city": "Neww Delhi",
                "region": "North",
                "country": "India",
                "zip_code": "110051"
            },
            {
                "type": "home",
                "street": "super address",
                "city": "Neww Delhi",
                "region": "North",
                "country": "India",
                "zip_code": "110051"
            }
        ],
        "social_network": [
            {
                "type": "facebook",
                "social_network_value": "fb  comss"
            }
        ],
        "emails": [
            {
                "type": "home",
                "email_value": "gousha@gmail.com"
            }
        ],
        "mobile_numbers": [
            {
                "type": "home",
                "mobile_value": "3343344637435"
            }
        ],
        "faxs": [
            {
                "type": "home",
                "fax_value": "gousha@"
            }
        ],
        "jobs": [
            {
                "type": "company",
                "job_value": "loop"
            }
        ],
        "dates": [
            {
                "type": "anniversary",
                "date": "loop"
            }
        ],
        "webs": [
            {
                "type": "anniversary",
                "website": "loop.com"
            }
        ],
        "notes": [
            {
                "type": "fair",
                "notes": "tes"
            }
        ]
    }
    response: {
        "business_card_detail": {
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
            "category_data": {},
            "color_hex_code": "",
            "user": "a8c1c071-153c-459b-97a0-e6a5e702b3a7",
            "is_card_retrived": true,
            "retrive_status": "retrive",
            "reason_for_failed": null,
            "created_at": "2022-12-10T14:52:14.996889Z",
            "prefix": null,
            "department": null,
            "position": null,
            "email_work": null,
            "email_personal": null,
            "contact_number_personal": null,
            "contact_number_work": null,
            "website": null,
            "address_type": null,
            "region": null,
            "zip_code": null,
            "address": [
                {
                    "id": 5,
                    "created_at": "2022-12-20T10:36:46.120834Z",
                    "updated_at": "2022-12-21T18:18:04.713696Z",
                    "is_active": true,
                    "type": "company",
                    "street": "Safdarjung enclave new Delhi seelampur delhi",
                    "city": "Neww Delhi",
                    "region": "North",
                    "country": "India",
                    "zip_code": "110051",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                },
                {
                    "id": 6,
                    "created_at": "2022-12-20T10:36:46.128305Z",
                    "updated_at": "2022-12-21T18:18:04.722460Z",
                    "is_active": true,
                    "type": "home",
                    "street": "Safdarjung enclave new Delhi seelasssmpur delhi",
                    "city": "Neww Delhi",
                    "region": "North",
                    "country": "India",
                    "zip_code": "110051",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                },
                {
                    "id": 7,
                    "created_at": "2022-12-20T10:37:35.987306Z",
                    "updated_at": "2022-12-21T18:18:04.729624Z",
                    "is_active": true,
                    "type": "home",
                    "street": "super address",
                    "city": "Neww Delhi",
                    "region": "North",
                    "country": "India",
                    "zip_code": "110051",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                }
            ],
            "social_network": [
                {
                    "id": 3,
                    "created_at": "2022-12-20T10:57:42.143647Z",
                    "updated_at": "2022-12-20T10:57:42.143688Z",
                    "is_active": true,
                    "type": "facebook",
                    "social_network_value": "fb,comss",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                },
                {
                    "id": 4,
                    "created_at": "2022-12-20T10:57:58.761489Z",
                    "updated_at": "2022-12-21T18:18:04.738810Z",
                    "is_active": true,
                    "type": "facebook",
                    "social_network_value": "fb  comss",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                }
            ],
            "emails": [
                {
                    "id": 2,
                    "created_at": "2022-12-21T17:09:40.689063Z",
                    "updated_at": "2022-12-21T18:18:04.745951Z",
                    "is_active": true,
                    "type": "home",
                    "email_value": "gousha@gmail.com",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                }
            ],
            "mobile_numbers": [
                {
                    "id": 2,
                    "created_at": "2022-12-21T18:18:04.757519Z",
                    "updated_at": "2022-12-21T18:18:04.757589Z",
                    "is_active": true,
                    "type": "home",
                    "mobile_value": "3343344637435",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                }
            ],
            "faxs": [
                {
                    "id": 2,
                    "created_at": "2022-12-21T18:18:04.772339Z",
                    "updated_at": "2022-12-21T18:18:04.772387Z",
                    "is_active": true,
                    "type": "home",
                    "fax_value": "gousha@",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                }
            ],
            "jobs": [
                {
                    "id": 4,
                    "created_at": "2022-12-21T18:18:04.781899Z",
                    "updated_at": "2022-12-21T18:18:04.781939Z",
                    "is_active": true,
                    "type": "company",
                    "job_value": "loop",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                }
            ],
            "dates": [],
            "webs": [
                {
                    "id": 2,
                    "created_at": "2022-12-21T18:18:04.795421Z",
                    "updated_at": "2022-12-21T18:18:04.795456Z",
                    "is_active": true,
                    "type": "anniversary",
                    "website": "loop.com",
                    "created_by": null,
                    "updated_by": null,
                    "business_card": "f01d162d-fe89-4d46-9cdc-d924c2557666"
                }
            ],
            "notes": []
            },
        "success": true,
        "message": "DONE"
        }
    """

    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """this put method used to update a business card details"""
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

        business_card_detail = UpdateBusinessCardDetails(
            auth_user_instance=request.user, business_card_data=request.data
        ).update_business_card_detail()
        if not business_card_detail:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["PLEASE_PROVIDE_VALID_CARD_ID"],
                success=False,
            )

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card_detail",
            data=business_card_detail,
            success=True,
        )


class CategoryGroupList(LoggingMixin, APIView):
    """
    BusinessCardDetails
    Authorization: YES
    Method: GET
    path: /api/v1/business/card/category/
    response: {
        "category_group_list": [
            {
                "id": "c5f7ac4d-a3f7-4856-8c69-193e8d46febe",
                "created_at": "2022-12-10T14:50:53.638926Z",
                "updated_at": "2022-12-10T14:50:53.638956Z",
                "is_active": true,
                "category_name": "Water mixer",
                "description": "tes",
                "color_hex_code": "#ff0000",
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "d579c859-20bc-4578-a7e9-8784563d5d1c",
                "created_at": "2022-12-10T14:51:08.190816Z",
                "updated_at": "2022-12-10T14:51:08.190845Z",
                "is_active": true,
                "category_name": "Frok",
                "description": "fadshgkjla",
                "color_hex_code": "#ff0000",
                "created_by": 1,
                "updated_by": 1
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

        business_card_detail = BusinessCardReader(
            auth_user_instance=request.user, business_card_data=request.data
        ).category_group_list()
        if not business_card_detail:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["PLEASE_PROVIDE_VALID_CARD_ID"],
                success=False,
            )

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="category_group_list",
            data=business_card_detail,
            success=True,
        )

    def post(self, request):
        """post the category group list
        method: POST
        path: api/v1/business/card/category/
        request_body: {
            "category_name": "new category",
            "color_hex_code": "#ff0000"
        }
        response: {
            "category_group_list": {
                "id": "7bfd8ea2-b9c7-4b37-818d-20a2cf16a456",
                "created_at": "2022-12-12T07:03:39.957120Z",
                "updated_at": "2022-12-12T07:03:39.957163Z",
                "is_active": true,
                "category_name": "new category",
                "description": null,
                "color_hex_code": "#ff0000",
                "created_by": null,
                "updated_by": null
            },
            "success": true,
            "message": "DONE"
        }
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
                message=API_RESPONSE_MSG["USER_NOT_FOUND"],
                success=False,
            )

        category_group_result = BusinessCardReader(
            auth_user_instance=request.user, category_group_data=request.data
        ).create_category_group()

        if not category_group_result:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["CATEGORY_ALREADY_EXIST"],
                success=False,
            )
        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="category_group_list",
            data=category_group_result,
            success=True,
        )


class BusinessCardDelete(LoggingMixin, APIView):
    """
    BusinessCardDelete
    Authorization: YES
    Method: GET
    path: /api/v1/business/card/delete/
    method: POST
    request_body: {
        "business_card_id": "f459539d-ffeb-4e6f-93c7-f4ef85ff38fb"
    }
    response: {
        "business_card_delete": {
            "is_deleted": true
        },
        "success": true,
        "message": "DONE"
    }
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """post the business card delete id"""
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

        business_card_delete = BusinessCardReader(
            auth_user_instance=request.user, business_card_data=request.data
        ).business_card_delete()
        if not business_card_delete:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["PLEASE_PROVIDE_VALID_CARD_ID"],
                success=False,
            )
        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card_delete",
            data=business_card_delete,
            success=True,
        )


class SendBusinessCardEmail(LoggingMixin, APIView):
    """
    BusinessCardList
    Authorization: YES
    path: /api/v1/business/card/email/send/
    response: {
        "business_card_id": "f459539d-ffeb-4e6f-93c7-f4ef85ff38fb"
    }
    response: {
        "business_card_sent": {
            "sent": true
        },
        "success": true,
        "message": "DONE"
    }
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
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

        business_card_sender_status = BusinessCardSender(
            auth_user_instance=request.user, business_card_data=request.data.copy()
        ).card_send_by_email()
        if not business_card_sender_status:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG["No_ACTIVE_DATA"],
                success=False,
            )
        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname="business_card_sent",
            data={"sent": business_card_sender_status},
            success=True,
        )
