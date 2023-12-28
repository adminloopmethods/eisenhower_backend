from django.contrib import admin

# datetime
from datetime import datetime
from import_export.admin import ImportExportModelAdmin

from location.models import CountryMaster
from configuration.admin import make_deactivate_data, make_activate_data

# Register your models here.


class CountryMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    CountryMasterAdmin
    all required listing data for
    admin panel
    """
    search_fields = [
        'country',
        # 'isd',
        # 'mobile_no_digits',
        # 'currency__currency',
        # 'code',
        # 'timezone'
    ]
    list_filter = [
        'is_active',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
        # 'country',
        # 'isd',
        # 'mobile_no_digits',
        # 'currency',
        # 'code',
        # 'timezone'
    ]
    list_display = [
        'country',
        'mobile_no_digits',
        'isd',
        'currency',
        'is_active',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by'
        # 'code',
        # 'timezone'
    ]

    exclude = [
        'is_active',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by'
    ]
    list_per_page = 8

    actions = [make_deactivate_data, make_activate_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return False

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in adin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()


admin.site.register(CountryMaster, CountryMasterAdmin)
