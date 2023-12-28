from datetime import datetime
from django.contrib import admin

# Register your models here.

from configuration.models import (Language,
                                  TaskStatusMaster,
                                  CurrencyMaster,
                                  ColorMaster,
                                  UserRoleMaster,
                                  Departments,
                                  Topics,
                                  TaskPriorityStatus,
                                  TestFilesUploadForRequest,
                                  ExpenseTypeMaster)

# all admin panel drop-down delete option remove
# admin.site.disable_action('delete_selected')
# User.objects.exclude(username__in=["loop", "alessandra.biella@gruppodr.it"]).filter(is_active=True).delete()
#


# function of active the data for all project records
def make_activate_data(modeladmin, request, queryset):
    """
    make_active_data:
    activate the data from admin side.
    """
    queryset.update(is_active='1', updated_at=datetime.now())


make_activate_data.short_description = "Move Items to Active"


# function of deactivate the data for all project records
def make_deactivate_data(modeladmin, request, queryset):
    """
    make_deactivate_data:
    deactivate the data from admin side.
    """
    queryset.update(is_active='0', updated_at=datetime.now())


make_deactivate_data.short_description = "Move Items to Deactive"


class LanguageAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['language_name', 'language_code']
    # list_filter = [
    #     'is_active',
    #     ('created_at', DateRangeFilter),
    #     ('updated_at', DateRangeFilter),
    #     'created_by',
    #     'updated_by'
    # ]
    list_display = [
        'language_code',
        'language_name',
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


class TaskStatusMasterAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['status_name']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'status_name',
        # 'description',
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


class CurrencyMasterAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['currency', 'symbol', ]
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'currency',
        # 'description',
        'symbol',
        'code_iso',
        'hex_symbol',
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


class ColorMasterAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['color_name', 'color_code', ]
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'color_name',
        # 'description',
        'color_code',
        'hex_symbol',
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


class UserRoleMasterAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['role_name', 'role', ]
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'role_name',
        # 'description',
        'role',
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


class DepartmentsAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['department_name']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'department_name',
        # 'description',
        'access_status',
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


class TopicsAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['topic_name']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'topic_name',
        # 'description',
        'access_status',
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


class TaskPriorityStatusAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['priority_status_name']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'priority_status_name',
        # 'description',
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


# all register admin values
admin.site.register(Language, LanguageAdmin)
admin.site.register(TaskStatusMaster, TaskStatusMasterAdmin)
admin.site.register(CurrencyMaster, CurrencyMasterAdmin)
admin.site.register(ColorMaster, ColorMasterAdmin)
admin.site.register(UserRoleMaster, UserRoleMasterAdmin)
admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(Topics, TopicsAdmin)
admin.site.register(TaskPriorityStatus, TaskPriorityStatusAdmin)
admin.site.register(TestFilesUploadForRequest)
admin.site.register(ExpenseTypeMaster)
