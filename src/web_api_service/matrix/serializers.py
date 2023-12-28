from rest_framework import serializers

from django.db.models import Q
from matrix.models import MatrixConfiguration
from matrix.models import TaskTypeConfig
from matrix.models import MatrixTaskMapping
from task_management.models import Tasks


class MatrixConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixConfiguration
        fields = "__all__"


class TaskTypeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTypeConfig
        fields = ("id", "rule_name", "priority_status", "description")

    # priority status serializer
    priority_status = serializers.SerializerMethodField("get_priority_status")

    @staticmethod
    def get_priority_status(obj):
        """this get_priority_status method get the priority status as per priority config"""
        if not obj:
            return {}
        return obj.priority_status.priority_status_name if obj.priority_status else None


class TaskTypeConfigItalianSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTypeConfig
        fields = ("id", "rule_name", "priority_status", "description")

    # priority status serializer
    priority_status = serializers.SerializerMethodField("get_priority_status")
    rule_name = serializers.SerializerMethodField("get_rule_name")

    @staticmethod
    def get_rule_name(obj):
        """this get_priority_status method get the priority status as per priority config"""
        if obj:
            return (
                obj.rule_name_in_italian if obj.rule_name_in_italian else obj.rule_name
            )
        else:
            return None

    @staticmethod
    def get_priority_status(obj):
        """this get_priority_status method get the priority status as per priority config"""
        if obj:
            if obj.priority_status:
                if obj.priority_status.priority_status_in_italian:
                    return obj.priority_status.priority_status_in_italian
                else:
                    return obj.priority_status.priority_status_name
            else:
                return None
        else:
            return None


class MatrixTaskMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixTaskMapping
        fields = "__all__"


class MatrixWithRuleConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixConfiguration
        fields = "__all__"

    # serializer methods fields
    color = serializers.SerializerMethodField("get_matrix_color")
    task_rule = serializers.SerializerMethodField("get_task_rule")
    task_count = serializers.SerializerMethodField("get_task_count")

    # mapping serializer fileds
    # task_type_config_serializer = TaskTypeConfigSerializer(many=True, read_only=True)

    @staticmethod
    def get_matrix_color(obj):
        """this get_matrix_color method used to get the color of matrix rule"""
        return str(obj.color.hex_symbol) if obj.color else ""

    @staticmethod
    def get_task_rule(obj):
        """this get_task_rule method get the task rule object as per priority config"""
        if not obj:
            return {}
        try:
            _matrix_task_mapping_instance = MatrixTaskMapping.objects.get(
                matrix_type=obj
            )
            return TaskTypeConfigSerializer(
                _matrix_task_mapping_instance.task_type_config.filter(is_active=True),
                many=True,
            ).data
        except Exception as e:
            print("MatrixTaskMapping.DoesNotExist")
            print(e)
            return {}

    def get_task_count(self, obj):
        """this get_task_rule method get the task rule object as per priority config"""
        try:
            try:
                print("auth-user", self.context["login_user"].id)
                _matrix_task_mapping_instance = MatrixTaskMapping.objects.get(
                    matrix_type=obj
                )
            except Exception as e:
                print("MatrixTaskMapping.DoesNotExist")
                print(e)
                return "0"
            print("_matrix_task_mapping_instance", _matrix_task_mapping_instance)
            # task_query_set = Tasks.objects.filter(
            #     Q(task_owner__id=self.context["login_user"].id)
            #     | Q(members__in=[self.context["login_user"].id]),
            #     matrix_type_config=_matrix_task_mapping_instance,
            #     is_deleted=False,
            # )
            task_query_set = Tasks.objects.filter(
                members__in=[self.context["login_user"].id],
                matrix_type_config=_matrix_task_mapping_instance,
                is_deleted=False,
            )
            print(task_query_set)
            print("task-counts", task_query_set.count())
            return str(task_query_set.distinct().count())
        except Exception as e:
            print("@get_task_countException")
            print(e)
            return "0"


class MatrixWithRuleConfigurationItalianSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixConfiguration
        fields = "__all__"

    # serializer methods fields
    color = serializers.SerializerMethodField("get_matrix_color")
    task_rule = serializers.SerializerMethodField("get_task_rule")
    task_count = serializers.SerializerMethodField("get_task_count")
    matrix_rule_name = serializers.SerializerMethodField("get_matrix_rule_name")

    # mapping serializer fileds
    # task_type_config_serializer = TaskTypeConfigSerializer(many=True, read_only=True)

    def get_matrix_rule_name(self, obj):
        """get_matrix_rule_name"""
        try:
            return (
                obj.matrix_rule_in_italian
                if obj.matrix_rule_in_italian
                else obj.matrix_rule_name
            )
        except Exception as e:
            print(e)
            return "Priority"

    @staticmethod
    def get_matrix_color(obj):
        """this get_matrix_color method used to get the color of matrix rule"""
        return str(obj.color.hex_symbol) if obj.color else ""

    @staticmethod
    def get_task_rule(obj):
        """this get_task_rule method get the task rule object as per priority config"""
        if not obj:
            return {}
        try:
            _matrix_task_mapping_instance = MatrixTaskMapping.objects.get(
                matrix_type=obj
            )
            return TaskTypeConfigItalianSerializer(
                _matrix_task_mapping_instance.task_type_config.filter(is_active=True),
                many=True,
            ).data
        except Exception as e:
            print("MatrixTaskMapping.DoesNotExist")
            print(e)
            return {}

    def get_task_count(self, obj):
        """this get_task_rule method get the task rule object as per priority config"""
        try:
            try:
                print("auth-user", self.context["login_user"].id)
                _matrix_task_mapping_instance = MatrixTaskMapping.objects.get(
                    matrix_type=obj
                )
            except Exception as e:
                print("MatrixTaskMapping.DoesNotExist")
                print(e)
                return "0"
            print("_matrix_task_mapping_instance", _matrix_task_mapping_instance)
            # task_query_set = Tasks.objects.filter(
            #     Q(task_owner__id=self.context["login_user"].id)
            #     | Q(members__in=[self.context["login_user"].id]),
            #     matrix_type_config=_matrix_task_mapping_instance,
            #     is_deleted=False,
            # )

            task_query_set = Tasks.objects.filter(
                members__in=[self.context["login_user"].id],
                matrix_type_config=_matrix_task_mapping_instance,
                is_deleted=False,
            )
            print(task_query_set)
            print("task-counts", task_query_set.count())
            return str(task_query_set.distinct().count())
        except Exception as e:
            print("@get_task_countException")
            print(e)
            return "0"
