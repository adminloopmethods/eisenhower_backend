from rest_framework import serializers

from cards.models import BusinessExpenseManager

from configuration.models import ExpenseTypeMaster


class BusinessExpenseManagerSerializer(serializers.ModelSerializer):
    expense_type_id = serializers.SerializerMethodField('get_expense_type_id')
    expense_type = serializers.SerializerMethodField('get_expense_type')
    expense_process_status_flag = serializers.SerializerMethodField('get_expense_process_status_flag')

    """
    TestFilesUploadForRequestSerializer
    """

    class Meta:
        model = BusinessExpenseManager
        fields = '__all__'

    @staticmethod
    def get_expense_type(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers
        """
        try:
            return instance.expense_type.expense_type if instance.expense_type else ""
        except Exception as e:
            print('getExpenseTypeErr')
            print(e)
            return ""

    @staticmethod
    def get_expense_type_id(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers
        """
        try:
            return instance.expense_type.id if instance.expense_type else ""
        except Exception as e:
            print('getExpenseTypeIdErr')
            print(e)
            return ""

    @staticmethod
    def get_expense_process_status_flag(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers
        """
        try:
            if instance.submit_to and instance.reimbursed_by:
                return True if BusinessExpenseManager.objects.filter(id=instance.id).update(
                    expense_process_status='reimbursed') else False
            if instance.submit_to:
                return True if BusinessExpenseManager.objects.filter(id=instance.id).update(
                    expense_process_status='submitted') else False
            else:
                return True if BusinessExpenseManager.objects.filter(id=instance.id).update(
                    expense_process_status='drafted') else False
        except Exception as e:
            print('getExpenseTypeErr')
            print(e)
            return None


class BusinessExpenseManagerUpdateSerializer(serializers.ModelSerializer):
    """
    TestFilesUploadForRequestSerializer
    """

    class Meta:
        model = BusinessExpenseManager
        fields = '__all__'


class ExpenseTypeMasterSerializer(serializers.ModelSerializer):
    """
    TestFilesUploadForRequestSerializer
    """

    class Meta:
        model = ExpenseTypeMaster
        fields = '__all__'
