from statistics import mode
import uuid
from django.db import models

# import abstract modules
from core.models import ABSTRACTDateModel
from core.models import ABSTRACTStatusModel
from core.models import ABSTRACTCreateUpdateByModel

# import constant
from core.constants import ACCESS_STATUS


class Language(ABSTRACTDateModel,
               ABSTRACTStatusModel,
               ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    language_code = models.CharField(max_length=70, unique=True)
    language_name = models.CharField(max_length=70, unique=True)

    class Meta:
        verbose_name = "Language Configuration"
        verbose_name_plural = "Language Configuration"
        db_table = 'language_configuration'

    def __str__(self):
        return self.language_code


class TaskStatusMaster(ABSTRACTDateModel,
                       ABSTRACTStatusModel,
                       ABSTRACTCreateUpdateByModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    status_name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    access_status = models.CharField(
        max_length=100,
        choices=ACCESS_STATUS)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,
                                 blank=True)
    status_name_in_italian = models.CharField(max_length=30, null=True,
                                              blank=True)

    class Meta:
        verbose_name = 'Task Status Master'
        verbose_name_plural = 'Task Status Master'
        db_table = 'task_status_master'

    def __str__(self):
        return self.status_name


class CurrencyMaster(ABSTRACTDateModel,
                     ABSTRACTStatusModel,
                     ABSTRACTCreateUpdateByModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    currency = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    symbol = models.CharField(max_length=30)
    code_iso = models.CharField(
        max_length=30,
        null=True, blank=True,
    )
    hex_symbol = models.CharField(
        max_length=30,
        null=True, blank=True, verbose_name='Hex Code')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,
                                 blank=True)

    class Meta:
        verbose_name = 'Currency Master'
        verbose_name_plural = 'Currency Master'
        db_table = 'currency_master'

    def __str__(self):
        return self.currency


class ExpenseTypeMaster(ABSTRACTDateModel,
                        ABSTRACTStatusModel,
                        ABSTRACTCreateUpdateByModel):
    """
    ExpenseTypeMaster
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    expense_type = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Expense Type Master'
        verbose_name_plural = 'Expense Type Master'
        db_table = 'expense_type_master'

    def __str__(self):
        return self.expense_type


class ColorMaster(ABSTRACTDateModel,
                  ABSTRACTStatusModel,
                  ABSTRACTCreateUpdateByModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    color_name = models.CharField(max_length=30, unique=True)
    color_code = models.CharField(max_length=30)
    hex_symbol = models.CharField(
        max_length=30,
        null=True, blank=True, verbose_name='Hex Code')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Color Config Master'
        verbose_name_plural = 'Color Config Master'
        db_table = 'color_master'

    def __str__(self):
        return self.color_name


class UserRoleMaster(ABSTRACTDateModel,
                     ABSTRACTStatusModel,
                     ABSTRACTCreateUpdateByModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    role_name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=30)
    role_in_italian = models.CharField(max_length=30, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,
                                 blank=True)

    class Meta:
        verbose_name = 'User Role Master'
        verbose_name_plural = 'User Role Master'
        db_table = 'user_role_master'

    def __str__(self):
        return self.role_name


class Departments(ABSTRACTDateModel,
                  ABSTRACTStatusModel,
                  ABSTRACTCreateUpdateByModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    department_name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    access_status = models.CharField(max_length=100, choices=ACCESS_STATUS)
    is_deleted = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,
                                 blank=True)

    class Meta:
        verbose_name = 'Departments'
        verbose_name_plural = 'Departments'
        db_table = 'departments'

    def __str__(self):
        return self.department_name


class Topics(ABSTRACTDateModel,
             ABSTRACTStatusModel,
             ABSTRACTCreateUpdateByModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    topic_name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    access_status = models.CharField(max_length=100, choices=ACCESS_STATUS)
    is_deleted = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,
                                 blank=True)

    class Meta:
        verbose_name = 'Topics'
        verbose_name_plural = 'Topics'
        db_table = 'topics'

    def __str__(self):
        return self.topic_name


class TaskPriorityStatus(ABSTRACTDateModel,
                         ABSTRACTStatusModel,
                         ABSTRACTCreateUpdateByModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    priority_status_name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,
                                 blank=True)
    priority_status_in_italian = models.CharField(max_length=30, null=True,
                                                  blank=True)

    class Meta:
        verbose_name = 'Task Priority Status'
        verbose_name_plural = 'Task Priority Status'
        db_table = 'task_priority_status'

    def __str__(self):
        return self.priority_status_name


class DepartmentBulkDataExcelFiles(models.Model):
    """DepartmentBulkDataExcelFiles
    """
    file_save_path = models.FileField(
        upload_to='department_bulk_import_excel_files')


class MemberBulkDataExcelFiles(models.Model):
    """MemberBulkDataExcelFiles
    """
    file_save_path = models.FileField(
        upload_to='member_bulk_import_excel_files')


class TaskBulkDataExcelFiles(models.Model):
    """TaskBulkDataExcelFiles
    """
    file_save_path = models.FileField(
        upload_to='task_bulk_import_excel_files')


class TestFilesUploadForRequest(models.Model):
    """TestFilesUploadForRequest
    """
    test_file = models.FileField(upload_to='test_file')
