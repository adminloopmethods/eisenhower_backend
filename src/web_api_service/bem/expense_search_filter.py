from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG
from web_api_service.bem.modules.expense_search_filter import \
    BusinessExpenseSearchFilter
from web_api_service.helpers.all_config_func import get_user_instance


# import business card models


class BusinessExpenseSearch(LoggingMixin, APIView):
    """
    BusinessExpenseSearch
    Method: GET
    Authorization: YES
    path: /api/v1/business/expense/search/?q=pycodertest
    response: {
        "business_expense_list": [
            {
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
            {'is_active': True, 'auth_user': request.user}
        )
        if not user_instance:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                success=False)

        business_expense_list = BusinessExpenseSearchFilter(
            auth_user_instance=request.user,
            business_expense_search_data=request.query_params.get('q')
        ).business_expense_search_list()
        if not business_expense_list:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA'],
                success=False)
        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname='business_expense_list',
            data=business_expense_list,
            success=True)


class BusinessExpenseFilter(LoggingMixin, APIView):
    """
    BusinessExpenseFilter
    Authorization: YES
    method: POST
    path: /api/v1/business/expense/filter/
    request_body: {
        "sort_by": "asc",
        "date": "",
        "type": "62f6ffe6-a407-4d78-acbf-90f6746dc65e"
    }
    response: {
        "business_expense_list": [
            {
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
            }
        ],
        "success": true,
        "message": "DONE"
    }
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """post the filter request and get the response according to filter data
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
            {'is_active': True, 'auth_user': request.user}
        )
        if not user_instance:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['USER_NOT_FOUND'],
                success=False)

        business_expense_list = BusinessExpenseSearchFilter(
            auth_user_instance=request.user,
            business_expense_filter_data=request.data
        ).business_expense_filter_list()
        if not business_expense_list:
            return APIResponseParser.response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=API_RESPONSE_MSG['No_ACTIVE_DATA'],
                success=False)
        return APIResponseParser.response(
            status_code=status.HTTP_200_OK,
            keyname='business_expense_list',
            data=business_expense_list,
            success=True)
