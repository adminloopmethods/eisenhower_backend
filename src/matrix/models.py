import uuid
# import django modules

from django.db import models

# Create your models here.

# import abstract modules
from core.models import ABSTRACTDateModel
from core.models import ABSTRACTStatusModel
from core.models import ABSTRACTCreateUpdateByModel

# import configuration tables
from configuration.models import ColorMaster
from configuration.models import TaskPriorityStatus

from configuration.models import Language


class MatrixConfiguration(ABSTRACTDateModel,
                          ABSTRACTStatusModel,
                          ABSTRACTCreateUpdateByModel):
    """
    MatrixConfiguration master table
    """
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    matrix_rule_name = models.CharField(max_length=30, unique=True)
    color = models.ForeignKey(ColorMaster, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,
                                 blank=True)
    matrix_rule_in_italian = models.CharField(max_length=30, null=True,
                                              blank=True)

    class Meta:
        verbose_name = '  Matrix Configuration'
        verbose_name_plural = '  Matrix Configuration'
        db_table = 'matrix_configuration'

    def __str__(self):
        return self.matrix_rule_name


class TaskTypeConfig(ABSTRACTDateModel,
                     ABSTRACTStatusModel,
                     ABSTRACTCreateUpdateByModel):
    """
    TaskTypeConfig master table
    """
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    rule_name = models.CharField(max_length=30)
    rule_name_in_italian = models.CharField(max_length=30, null=True,
                                            blank=True)
    priority_status = models.ForeignKey(
        TaskPriorityStatus,
        on_delete=models.CASCADE,
        related_name='priority_status_task_type_config')
    priority_status_in_italian = models.ForeignKey(
        TaskPriorityStatus,
        on_delete=models.CASCADE,
        related_name='priority_status_task_type_config_italian',
        null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True,
                                 blank=True)

    class Meta:
        verbose_name = ' Task Type Config'
        verbose_name_plural = ' Task Type Config'
        db_table = 'task_type_config'

    def __str__(self):
        return self.rule_name


class MatrixTaskMapping(ABSTRACTDateModel,
                        ABSTRACTStatusModel,
                        ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    matrix_type = models.OneToOneField(
        MatrixConfiguration,
        on_delete=models.CASCADE,
        related_name='_matrix_task_inst')
    task_type_config = models.ManyToManyField(TaskTypeConfig)

    class Meta:
        verbose_name = 'Matrix Task Mapping'
        verbose_name_plural = 'Matrix Task Mapping'
        db_table = 'matrix_task_mapping'

    def __str__(self):
        return self.matrix_type.matrix_rule_name

    def display_task_config_rules(self):
        return ', '.join([str(i.rule_name) + ': ' +
                          str(i.priority_status.priority_status_name)
                          for i in self.task_type_config.all()[:3]])

    display_task_config_rules.short_description = 'Task Type Config Rules'
