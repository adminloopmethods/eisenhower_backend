from datetime import datetime
from django.contrib import admin

# Register your models here.
from task_management.models import Tasks
from task_management.models import TaskComments

from configuration.admin import make_activate_data, make_deactivate_data


class TasksAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['task_owner']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'task_owner',
        'task_name',
        # 'description',
        'due_date',
        'estimate',
        'notes',
        'comments',
        'reminder',
        'status',
        'department',
        'topic',
        # 'members',
        'matrix_type_config',
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]

    actions = [make_activate_data, make_deactivate_data]

    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:

            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()


class TasksCommentsAdmin(admin.ModelAdmin):
    actions = [make_activate_data, make_deactivate_data]

    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:

            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()


admin.site.register(Tasks, TasksAdmin)
admin.site.register(TaskComments, TasksCommentsAdmin)
