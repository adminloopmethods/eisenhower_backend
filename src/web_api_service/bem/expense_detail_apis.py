"""
all expense details api
List
Details
Edit
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG
from web_api_service.bem.modules.expense_details import BusinessExpenseDetail
from web_api_service.bem.modules.expense_type_master import BusinessExpenseTypeMaster
from web_api_service.helpers.all_config_func import get_user_instance


class BusinessExpenseList(LoggingMixin, APIView):
    """
    BusinessCardList
    Authorization: YES
    path: /api/v1/business/expense/list/
    Method: GET
    response: {
        "business_card_list": [
            {
                "id": "cd57493f-8386-46eb-b6d3-3eafbb8314c3",
                "created_at": "2023-01-10T07:32:36.253536Z",
                "updated_at": "2023-01-10T07:32:36.253567Z",
                "is_active": true,
                "expense_process_status": "drafted",
                "expense_image": "/media/expense_images/806623172_156100.jpg",
                "merchant_name": "testt",
                "date": "2023-01-18",
                "description": "ttttttttttttttttttttttt",
                "amount": "223",
                "submit_to": null,
                "reimbursed_on": "2023-01-10T10:00:00Z",
                "reimbursed_by": "Gourav Sharma",
                "reimbursed_method": "Cash",
                "expense_capture_type": "automated",
                "is_card_retrived": true,
                "retrive_status": "failed",
                "reason_for_failed": null,
                "created_by": 1,
                "updated_by": 1,
                "expense_type": null,
                "user": "efb01b9e-a269-4331-abfe-4d0ef7394b4a"
            }
        ],
        "success": true,
        "message": "DONE"
    }
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """get the business card list
        """
        if not request.user:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                success=False)

        user_instance = get_user_instance(
            {
                'is_active': True,
                'auth_user': request.user
            }
        )
        if not user_instance:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                success=False)

        business_card_list = BusinessExpenseDetail(
            auth_user_instance=request.user
        ).expense_list()
        if not business_card_list:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA'],
                success=False
            )

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname='business_expense_list',
            data=business_card_list,
            success=True)


class BusinessExpenseDetails(LoggingMixin, APIView):
    """
    BusinessCardDetails
    Authorization: YES
    method: GET
    path: /api/v1/business/expense/detail/?id=cd57493f-8386-46eb-b6d3-3eafbb8314c3
        response: {
        "business_card_detail": {
            "id": "cd57493f-8386-46eb-b6d3-3eafbb8314c3",
            "created_at": "2023-01-10T07:32:36.253536Z",
            "updated_at": "2023-01-10T07:32:36.253567Z",
            "is_active": true,
            "expense_process_status": "drafted",
            "expense_image": "/media/expense_images/806623172_156100.jpg",
            "merchant_name": "testt",
            "date": "2023-01-18",
            "description": "ttttttttttttttttttttttt",
            "amount": "223",
            "submit_to": null,
            "reimbursed_on": "2023-01-10T10:00:00Z",
            "reimbursed_by": "Gourav Sharma",
            "reimbursed_method": "Cash",
            "expense_capture_type": "automated",
            "is_card_retrived": true,
            "retrive_status": "failed",
            "reason_for_failed": null,
            "created_by": 1,
            "updated_by": 1,
            "expense_type": null,
            "user": "efb01b9e-a269-4331-abfe-4d0ef7394b4a"
        },
        "success": true,
        "message": "DONE"
    }
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """get the business card list
        """
        if not request.query_params:
            return APIResponseParser.response(
                message=API_RESPONSE_MSG['REQUEST_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST,
                success=False)

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

        if not request.query_params.get('id'):
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['PLEASE_PROVIDE_BUSINESS_CARD_ID'],
                success=False)

        business_card_detail = BusinessExpenseDetail(
            auth_user_instance=request.user,
            business_expense_id=request.query_params.get('id')).expense_detail()
        if not business_card_detail:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['PLEASE_PROVIDE_VALID_CARD_ID'],
                success=False)

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname='business_expense_detail',
            data=business_card_detail,
            success=True)


class UpdateBusinessExpenseDetail(APIView):
    """
    UpdateBusinessExpenseDetail
    Authorization: YES
    Method: PUT
    path: /api/v1/business/expense/update/
    request: {
        "id": "cd57493f-8386-46eb-b6d3-3eafbb8314c3",
        "merchant_name": "pycodertest",
        "date": "2023-01-18",
        "description": "testfor test",
        "amount": "223",
        "submit_to": "pycodertest@gmail.com",
        "expense_type": "62f6ffe6-a407-4d78-acbf-90f6746dc65e"
    }

    id:cd57493f-8386-46eb-b6d3-3eafbb8314c3
    merchant_name:pycodertest
    date:2023-01-18
    description:testfor test
    amount:223
    submit_to:pycodertest@gmail.com
    expense_type:62f6ffe6-a407-4d78-acbf-90f6746dc65e
    expense_image: media_image
    response: {
        "business_card_detail": {
            "id": "cd57493f-8386-46eb-b6d3-3eafbb8314c3",
            "created_at": "2023-01-10T07:32:36.253536Z",
            "updated_at": "2023-01-10T08:17:22.679355Z",
            "is_active": true,
            "expense_process_status": "drafted",
            "expense_image": "/media/expense_images/806623172_156100.jpg",
            "merchant_name": "pycodertest",
            "date": "2023-01-18",
            "description": "testfor test",
            "amount": "223",
            "submit_to": "pycodertest@gmail.com",
            "reimbursed_on": "2023-01-10T10:00:00Z",
            "reimbursed_by": "Gourav Sharma",
            "reimbursed_method": "Cash",
            "expense_capture_type": "automated",
            "is_card_retrived": true,
            "retrive_status": "failed",
            "reason_for_failed": null,
            "created_by": 1,
            "updated_by": 1,
            "expense_type": "62f6ffe6-a407-4d78-acbf-90f6746dc65e",
            "user": "efb01b9e-a269-4331-abfe-4d0ef7394b4a"
        },
        "success": true,
        "message": "DONE"
    }
    """
    permission_classes = (IsAuthenticated,)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.business_expense_data = None

    def put(self, request):
        """this put method used to update a business card details
        """
        if not request.data:
            return APIResponseParser.response(
                message=API_RESPONSE_MSG['REQUEST_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST,
                success=False)

        if not request.user:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                success=False)

        user_instance = get_user_instance(
            {
                'is_active': True,
                'auth_user': request.user
            }
        )
        if not user_instance:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                success=False)

        business_expense_data = request.data
        business_expense_data._mutable = True

        business_card_detail = BusinessExpenseDetail(
            auth_user_instance=request.user,
            business_expense_data=business_expense_data
        ).update_expense_details()
        if not business_card_detail:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['PLEASE_PROVIDE_VALID_CARD_ID'],
                success=False)

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname='business_expense_detail',
            data=business_card_detail,
            success=True)


class ExpenseMasterList(LoggingMixin, APIView):
    """
    BusinessCardDetails
    Authorization: YES
    Method: GET
    path: /api/v1/business/expense/type/
    response: {
        "expense_types_data": [
            {
                "id": "62f6ffe6-a407-4d78-acbf-90f6746dc65e",
                "created_at": "2023-01-10T08:09:46.891604Z",
                "updated_at": "2023-01-10T08:09:46.891642Z",
                "is_active": true,
                "expense_type": "Fees",
                "description": "test",
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "83d34009-44fb-49c1-a300-475847f8910e",
                "created_at": "2023-01-10T08:10:11.746723Z",
                "updated_at": "2023-01-10T08:10:11.746744Z",
                "is_active": true,
                "expense_type": "car",
                "description": "",
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "1c6b424b-bc77-4957-b81c-949a8e6f1c8c",
                "created_at": "2023-01-10T08:10:22.616999Z",
                "updated_at": "2023-01-10T08:10:22.617020Z",
                "is_active": true,
                "expense_type": "Home",
                "description": "rr",
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "ead8b8b9-7a1a-45bd-beb9-86b9b9d67fc7",
                "created_at": "2023-01-10T08:10:32.725086Z",
                "updated_at": "2023-01-10T08:10:32.725118Z",
                "is_active": true,
                "expense_type": "office",
                "description": "rrr",
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
        """get the business card list
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

        expense_types_data = BusinessExpenseTypeMaster(auth_user_instance=request.user).expense_type_list()
        if not expense_types_data:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['PLEASE_PROVIDE_VALID_CARD_ID'],
                success=False)

        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname='expense_types_data',
            data=expense_types_data,
            success=True)
