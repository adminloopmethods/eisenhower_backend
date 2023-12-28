import uuid
from django.db import models

# Create your models here.
# import abstract modules
from core.models import ABSTRACTDateModel
from core.models import ABSTRACTStatusModel
from core.models import ABSTRACTCreateUpdateByModel

# import relation tables
from configuration.models import TaskStatusMaster
from configuration.models import Departments
import uuid

from configuration.models import Topics

# matrix mapping models
from matrix.models import MatrixTaskMapping

# user as a member models
from user.models import CustomUsers


class Tasks(ABSTRACTDateModel,
            ABSTRACTStatusModel,
            ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # Tasks manager models
    task_name = models.CharField(max_length=100)
    customer_name = models.CharField(
        max_length=100,
        null=True, blank=True,
        default=None)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    due_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    estimate = models.CharField(max_length=50, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    reminder = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    # all relation models fields
    status = models.ForeignKey(TaskStatusMaster, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    topic = models.ForeignKey(
        Topics,
        # on_delete=models.CASCADE,
        on_delete=models.SET_NULL,
        null=True, blank=True)
    members = models.ManyToManyField(CustomUsers, null=True, blank=True)
    task_owner = models.ForeignKey(CustomUsers,
                                   on_delete=models.CASCADE,
                                   related_name='task_owner_user')

    matrix_type_config = models.ForeignKey(
        MatrixTaskMapping,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Tasks'
        verbose_name_plural = 'Tasks'
        db_table = 'tasks'

    def __str__(self):
        return self.task_name


class TaskComments(ABSTRACTDateModel,
                   ABSTRACTStatusModel,
                   ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # Tasks comments
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)
    members = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Task Comments'
        verbose_name_plural = 'Task Comments'
        db_table = 'task_comments'

    def __str__(self):
        return self.comments
