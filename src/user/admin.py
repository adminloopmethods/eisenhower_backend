from datetime import datetime
from django.contrib import admin

# Register your models here.
from user.models import CustomUsers, Team
from user.models import UserDepartmentMapping
from user.models import UserTopicMapping
from user.models import UserMemberMapping
from user.models import UserStickyNotes

from configuration.admin import make_activate_data, make_deactivate_data


class CustomUsersAdmin(admin.ModelAdmin):
    exclude = ['is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['language_name', 'language_code']
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
    ]
    list_display = [
        'first_name',
        'last_name',
        'email',
        'mobile_with_isd',
        'registration_type',
        'profile_picture',
        'department',
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


class UserMemberMappingAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'get_members_list',
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


class UserDepartmentMappingAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'get_departments_list',
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


class UserTopicMappingAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'get_topics_list',
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


class UserStickyNotesAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'note',
    ]

    # actions = [make_activate_data, make_deactivate_data]

    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return False

    # def save_model(self, request, obj, form, change):
    #     if not change:

    #         obj.created_by = request.user
    #     else:
    #         obj.updated_by = request.user
    #         obj.updated_at = datetime.now()
    #     obj.save()


admin.site.register(CustomUsers, CustomUsersAdmin)

admin.site.register(UserMemberMapping, UserMemberMappingAdmin)
admin.site.register(UserDepartmentMapping, UserDepartmentMappingAdmin)
admin.site.register(UserTopicMapping, UserTopicMappingAdmin)
admin.site.register(UserStickyNotes, UserStickyNotesAdmin)

admin.site.register(Team)
