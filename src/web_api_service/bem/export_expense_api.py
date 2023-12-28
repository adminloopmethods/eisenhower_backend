from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

# import business card services
from web_api_service.bem.modules.export_expense import ExportBusinessExpense


# import business card models


class ExportBusinessExpenseList(LoggingMixin, APIView):
    """
    PATH: /api/v1/business/card/export/?id=36746343764836436483648&business_card_ids=[]
    """

    def get(self, request):
        """
        Args:
            request (instance): this request instance used to manage
            the all type of api request
        Returns:
            media_file: this media file type is a
            Excel file format with xlsx format
        """
        print('data', self.request.query_params)
        return ExportBusinessExpense(
            expense_user_id=self.request.query_params.get('id'),
            expense_type=self.request.query_params.get('expense_type_id', None),
            start_date=self.request.query_params.get('start_date', None),
            end_date=self.request.query_params.get('end_date', None),
            created_at=self.request.query_params.get('created_at', None),
            business_expense_ids=self.request.query_params.get(
                'business_card_ids', None
            ),
        ).export_business_expense()
