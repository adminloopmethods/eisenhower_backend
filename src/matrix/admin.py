from datetime import datetime
from django.contrib import admin

# Register your models here.
from matrix.models import MatrixConfiguration, MatrixTaskMapping, \
    TaskTypeConfig
from configuration.admin import make_deactivate_data, make_activate_data


class MatrixConfigurationAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by',
               'updated_by']
    search_fields = ['matrix_rule_name', 'color']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'matrix_rule_name',
        'color',
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


class TaskTypeConfigAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by',
               'updated_by']
    search_fields = ['rule_name', 'priority_status__priority_status_name']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'rule_name',
        'priority_status',
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


class MatrixTaskMappingAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by',
               'updated_by']
    search_fields = ['matrix_type']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'matrix_type',
        'display_task_config_rules',
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]

    fields = [
        'matrix_type',
        'task_type_config'
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


admin.site.register(MatrixConfiguration, MatrixConfigurationAdmin)
admin.site.register(TaskTypeConfig, TaskTypeConfigAdmin)
admin.site.register(MatrixTaskMapping, MatrixTaskMappingAdmin)
