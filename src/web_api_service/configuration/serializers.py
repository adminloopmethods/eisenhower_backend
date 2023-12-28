# import rest apps
from dataclasses import field
from rest_framework import serializers

from core.constants import ACCESS_STATUS

# import models
from configuration.models import Language
from configuration.models import TaskStatusMaster
from configuration.models import CurrencyMaster
from configuration.models import ColorMaster
from configuration.models import UserRoleMaster
from configuration.models import Departments
from configuration.models import Topics

from location.models import CountryMaster

# import user mapping models
from user.models import UserDepartmentMapping
from user.models import UserTopicMapping


class DepartmentsSerializer(serializers.ModelSerializer):

    my_department_status = serializers.SerializerMethodField(
        'get_my_department_status'
    )

    def get_my_department_status(self, instance):
        try:
            custom_user = self.context['user_instance']
            if str(custom_user.department.id) == str(instance.id):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    class Meta:
        model = Departments
        exclude = ('created_by', 'updated_by')


class UserDepartmentMappingSerializer(serializers.ModelSerializer):
    # departments = DepartmentsSerializer(many=True, read_only=True)
    departments = serializers.SerializerMethodField('get_department_list')

    class Meta:
        model = UserDepartmentMapping
        fields = ('id', 'user', 'departments')

    @staticmethod
    def get_department_list(instance):
        try:

            return DepartmentsSerializer(
                instance.departments.order_by('-created_at'),
                many=True).data
        except Exception as e:
            print(e)
            return []


class UserDepartmentMappingSearchSerializer(serializers.ModelSerializer):
    # departments = DepartmentsSerializer(many=True, read_only=True)
    departments = serializers.SerializerMethodField('get_department_list')

    class Meta:
        model = UserDepartmentMapping
        fields = ('id', 'user', 'departments')

    # @staticmethod
    def get_department_list(self, instance):
        try:
            return DepartmentsSerializer(
                instance.departments.filter(
                    department_name__istartswith=self.context['search_parameter']
                ).order_by('department_name'),
                many=True).data
        except Exception as e:
            print(e)
            return []

            


class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'


class UserTopicMappingSerializer(serializers.ModelSerializer):
    # topics = TopicsSerializer(many=True, read_only=True)
    topics = serializers.SerializerMethodField('get_topics_list')

    class Meta:
        model = UserTopicMapping
        fields = ('id', 'user', 'topics')

    @staticmethod
    def get_topics_list(instance):
        try:
            return TopicsSerializer(instance.topics.order_by('-created_at'),
                                    many=True).data
        except Exception as e:
            print(e)
            return []


class UserTopicSearchMappingSerializer(serializers.ModelSerializer):
    # topics = TopicsSerializer(many=True, read_only=True)
    topics = serializers.SerializerMethodField('get_topics_list')

    class Meta:
        model = UserTopicMapping
        fields = ('id', 'user', 'topics')

    # @staticmethod
    def get_topics_list(self, instance):
        try:
            return TopicsSerializer(
                instance.topics.filter(topic_name__istartswith=self.context['search_parameter']
                                       ).order_by('topic_name'),
                many=True).data
        except Exception as e:
            print(e)
            return []


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class TaskStatusMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusMaster
        fields = '__all__'


class TaskStatusMasterItalianSerializer(serializers.ModelSerializer):
    status_name = serializers.SerializerMethodField('get_status_name')

    class Meta:
        model = TaskStatusMaster
        fields = '__all__'

    @staticmethod
    def get_status_name(obj):
        """
        get_status_name
        """
        try:
            if not obj:
                return None
            return obj.status_name_in_italian if obj.status_name_in_italian \
                else obj.status_name
        except Exception as e:
            print(e)
            return None


class CurrencyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyMaster
        fields = '__all__'


class ColorMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorMaster
        fields = '__all__'


class UserRoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleMaster
        fields = '__all__'


class UserRoleMasterItalianSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField('get_role_name')

    class Meta:
        model = UserRoleMaster
        fields = '__all__'

    @staticmethod
    def get_role_name(obj):
        """
        get_role_name
        """
        try:
            if not obj:
                return None
            return obj.role_in_italian if obj.role_in_italian \
                else obj.role_name
        except Exception as e:
            print(e)
            return None


class CountryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMaster
        fields = '__all__'
