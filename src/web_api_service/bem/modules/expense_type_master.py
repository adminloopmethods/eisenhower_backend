from configuration.models import ExpenseTypeMaster

from web_api_service.bem.modules.serializers import ExpenseTypeMasterSerializer


class BusinessExpenseTypeMaster:
    """
    BusinessExpenseDetail
    """

    def __init__(self, **kwargs):
        self.auth_user_instance = kwargs.get('auth_user_instance', None)

    @staticmethod
    def expense_type_list():
        """this expense_list method used to get the
        all business card expense list from models
        """
        try:
            return ExpenseTypeMasterSerializer(ExpenseTypeMaster.objects.filter(is_active=True),
                                               many=True).data
        except Exception as e:
            print('ExpenseTypeSerializerErr')
            print(e)
            return None

