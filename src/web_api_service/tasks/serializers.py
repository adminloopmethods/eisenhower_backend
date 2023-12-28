from datetime import datetime

from rest_framework import serializers

from task_management.models import Tasks, TaskComments
from web_api_service.notification.push_notification import PushNotifications
from web_api_service.users.serializers import MemberSerializer, GetMemberDetailSerializer


class TasksSerializer(serializers.ModelSerializer):

    # start_date = serializers.DateField(format="%d/%m/%Y")
    # due_date = serializers.DateField(format="%d/%m/%Y")
    # reminder = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Tasks
        fields = (
            "id",
            "task_name",
            "customer_name",
            "description",
            "start_date",
            "due_date",
            "estimate",
            "notes",
            "comments",
            "reminder",
            "status",  # id
            "department",  # id
            "topic",  # id
            "members",  # ids
            "task_owner",  # ids
            "matrix_type_config",  # ids
            "is_deleted",
        )


class UpdateTaskDetailSerializerForMembers(serializers.ModelSerializer):
    """
    TaskDetailSerializer
    """

    status = serializers.SerializerMethodField("get_status_name")
    status_id = serializers.SerializerMethodField("get_status_id")
    department_name = serializers.SerializerMethodField("get_department_name")
    topic_name = serializers.SerializerMethodField("get_topic_name")
    members = serializers.SerializerMethodField("get_members_task_list")
    task_owner = serializers.SerializerMethodField("get_task_owner_name")
    matrix_type_config = serializers.SerializerMethodField(
        "get_matrix_type_config"
    )

    due_date = serializers.SerializerMethodField("get_due_date")
    start_date = serializers.SerializerMethodField("get_start_date")

    # matrix_config_details
    matrix_config_detail = serializers.SerializerMethodField(
        "get_matrix_config_detail"
    )
    reminder = serializers.SerializerMethodField("get_reminder_date")

    class Meta:
        model = Tasks
        fields = (
            "id",
            "task_name",
            "customer_name",
            "description",
            "start_date",
            "due_date",
            "estimate",
            "notes",
            "comments",
            "reminder",
            "status",  # id
            "department",  # id
            "topic",  # id
            "members",  # ids
            "task_owner",  # ids
            "matrix_type_config",  # ids
            "status_id",
            "matrix_config_detail",
            "department_name",
            "topic_name",
            "created_at",
        )

    @staticmethod
    def get_status_id(obj):
        """this get_status_name method get the status name for assign task"""
        if not obj:
            return {}
        return obj.status.id if obj.status else None

    # @staticmethod

    def get_status_name(self, obj):
        """this get_status_name method get the status name for assign task"""
        try:
            if not obj:
                return {}
            if self.context["user_instance"].language.language_code == "ENG":
                return obj.status.status_name if obj.status else None
            if self.context["user_instance"].language.language_code == "ITL":
                return obj.status.status_name_in_italian if obj.status else None
            else:
                return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_department_name(obj):
        """this get_priority_status method get the priority
        status as per priority config
        """
        if not obj:
            return {}
        return obj.department.department_name if obj.department else None

    @staticmethod
    def get_topic_name(obj):
        """this get_priority_status method get the priority status
        as per priority config
        """
        if not obj:
            return {}
        return obj.topic.topic_name if obj.topic else None

    # @staticmethod
    def get_members_task_list(self, obj):
        """this get_priority_status method get the priority
        status as per priority config
        """
        try:
            return GetMemberDetailSerializer(

                obj.members.order_by("-created_at"),
                context={'user_instance': self.context['user_instance']},
                many=True
            ).data
        except Exception as e:
            print(e)
            return obj.members if obj.members else []

    @staticmethod
    def get_task_owner_name(obj):
        """this get_priority_status method get the priority
        status as per priority config
        """
        if not obj:
            return {}
        return (
            "".join(
                [
                    str(obj.task_owner.first_name),
                    " ", str(obj.task_owner.last_name)
                ]
            )
            if obj.task_owner else None
        )

    @staticmethod
    def get_matrix_type_config(obj):
        """this get_matrix_type_config method get the priority
        status as per priority config
        """
        if not obj:
            return {}
        return (
            obj.matrix_type_config.matrix_type.matrix_rule_name
            if obj.matrix_type_config
            else None
        )

    @staticmethod
    def get_due_date(obj):
        """this get_due_date method get due date with
        the correct format
        """
        if not obj:
            return None

        try:
            if obj.due_date > datetime.now().date():
                try:
                    push_notification_instance = PushNotifications(
                        api_service_name="__OVERDUEDATE__",
                        TO="admin",
                        user=obj.task_owner.id,
                        user_notification_data={
                            "username": "".join(
                                [
                                    str(obj.task_owner.first_name),
                                    " ",
                                    str(obj.task_owner.last_name),
                                ]
                            ),
                            "task_name": str(obj.task_name),
                            "due_datetime": obj.due_date.strftime("%d-%m-%Y"),
                        },
                    )
                    push_notification_instance()
                except Exception as e:
                    print("OverDueTaskOwenerExpErr")
                    print(e)

                try:
                    members = obj.members.filter()
                    for member in members:
                        push_notification_instance = PushNotifications(
                            api_service_name="__OVERDUEDATE__",
                            TO="admin",
                            user=member.id,
                            user_notification_data={
                                "username": "".join(
                                    [str(member.first_name),
                                     " ", str(member.last_name)]
                                ),
                                "task_name": str(obj.task_name),
                                "due_datetime": obj.due_date.strftime(
                                    "%d-%m-%Y"
                                ),
                            },
                        )
                        push_notification_instance()
                except Exception as e:
                    print("OverDueMemeberNotificationExpErr")
                    print(e)
        except Exception as e:
            print("GS#get_due_date")
            print(e)

        try:
            return obj.due_date.strftime("%d-%m-%Y")
        except Exception as e:
            print("Err")
            print(e)
            return None

    @staticmethod
    def get_start_date(obj):
        """this get_start_date method get due date
        with the correct format
        """
        if not obj:
            return None
        try:
            return obj.start_date.strftime("%d-%m-%Y")
        except Exception as e:
            print("GS#get_due_date")
            print(e)
            return obj.start_date

    @staticmethod
    def get_reminder_date(obj):
        """this get_reminder_date method get due date
        with the correct format
        """
        if not obj:
            return None
        try:
            return obj.reminder.strftime("%d-%m-%Y")
        except Exception as e:
            print("GS#get_due_date")
            print(e)
            return obj.reminder

    @staticmethod
    def get_matrix_config_detail(obj):
        """get_matrix_config_detail"""
        matrix_config_detail_dict = {}
        _imp_urg_dict = {"High": "0", "Medium": "50", "Low": "100"}
        try:
            matrix_instance = obj.matrix_type_config.task_type_config.all()
            for matrix_data in matrix_instance:
                matrix_config_detail_dict[
                    str(matrix_data.rule_name)] = _imp_urg_dict[
                        str(matrix_data.priority_status)
                    ]
            return matrix_config_detail_dict
        except Exception as e:
            print("#Gs164-get_matrix_config_detail")
            print(e)
            return matrix_config_detail_dict


class TaskDetailSerializer(serializers.ModelSerializer):
    """
    TaskDetailSerializer
    """

    status = serializers.SerializerMethodField("get_status_name")
    status_id = serializers.SerializerMethodField("get_status_id")
    department_name = serializers.SerializerMethodField("get_department_name")
    topic_name = serializers.SerializerMethodField("get_topic_name")
    members = serializers.SerializerMethodField("get_members_list")
    task_owner = serializers.SerializerMethodField("get_task_owner_name")
    matrix_type_config = serializers.SerializerMethodField(
        "get_matrix_type_config"
    )

    due_date = serializers.SerializerMethodField("get_due_date")
    start_date = serializers.SerializerMethodField("get_start_date")

    # matrix_config_details
    matrix_config_detail = serializers.SerializerMethodField(
        "get_matrix_config_detail"
    )
    reminder = serializers.SerializerMethodField("get_reminder_date")

    class Meta:
        model = Tasks
        fields = (
            "id",
            "task_name",
            "customer_name",
            "description",
            "start_date",
            "due_date",
            "estimate",
            "notes",
            "comments",
            "reminder",
            "status",  # id
            "department",  # id
            "topic",  # id
            "members",  # ids
            "task_owner",  # ids
            "matrix_type_config",  # ids
            "status_id",
            "matrix_config_detail",
            "department_name",
            "topic_name",
            "created_at",
        )

    @staticmethod
    def get_status_id(obj):
        """this get_status_name method get the status name for assign task"""
        if not obj:
            return {}
        return obj.status.id if obj.status else None

    # @staticmethod

    def get_status_name(self, obj):
        """this get_status_name method get the status name for assign task"""
        try:
            if not obj:
                return {}
            if self.context["user_instance"].language.language_code == "ENG":
                return obj.status.status_name if obj.status else None
            if self.context["user_instance"].language.language_code == "ITL":
                return obj.status.status_name_in_italian if obj.status else None
            else:
                return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_department_name(obj):
        """this get_priority_status method get the priority 
        status as per priority config
        """
        if not obj:
            return {}
        return obj.department.department_name if obj.department else None

    @staticmethod
    def get_topic_name(obj):
        """this get_priority_status method get the priority status 
        as per priority config
        """
        if not obj:
            return {}
        return obj.topic.topic_name if obj.topic else None

    @staticmethod
    def get_members_list(obj):
        """this get_priority_status method get the priority 
        status as per priority config
        """
        try:
            return MemberSerializer(
                obj.members.order_by("-created_at"), many=True
            ).data
        except Exception as e:
            print(e)
            return obj.members if obj.members else []

    @staticmethod
    def get_task_owner_name(obj):
        """this get_priority_status method get the priority 
        status as per priority config
        """
        if not obj:
            return {}
        return (
            "".join(
                [   
                    str(obj.task_owner.first_name), 
                    " ", str(obj.task_owner.last_name)
                ]
            )
            if obj.task_owner else None
        )

    @staticmethod
    def get_matrix_type_config(obj):
        """this get_matrix_type_config method get the priority
        status as per priority config
        """
        if not obj:
            return {}
        return (
            obj.matrix_type_config.matrix_type.matrix_rule_name
            if obj.matrix_type_config
            else None
        )

    @staticmethod
    def get_due_date(obj):
        """this get_due_date method get due date with
        the correct format
        """
        if not obj:
            return None

        try:
            if obj.due_date > datetime.now().date():
                try:
                    push_notification_instance = PushNotifications(
                        api_service_name="__OVERDUEDATE__",
                        TO="admin",
                        user=obj.task_owner.id,
                        user_notification_data={
                            "username": "".join(
                                [
                                    str(obj.task_owner.first_name),
                                    " ",
                                    str(obj.task_owner.last_name),
                                ]
                            ),
                            "task_name": str(obj.task_name),
                            "due_datetime": obj.due_date.strftime("%d-%m-%Y"),
                        },
                    )
                    push_notification_instance()
                except Exception as e:
                    print("OverDueTaskOwenerExpErr")
                    print(e)

                try:
                    members = obj.members.filter()
                    for member in members:
                        push_notification_instance = PushNotifications(
                            api_service_name="__OVERDUEDATE__",
                            TO="admin",
                            user=member.id,
                            user_notification_data={
                                "username": "".join(
                                    [str(member.first_name), 
                                     " ", str(member.last_name)]
                                ),
                                "task_name": str(obj.task_name),
                                "due_datetime": obj.due_date.strftime(
                                    "%d-%m-%Y"
                                ),
                            },
                        )
                        push_notification_instance()
                except Exception as e:
                    print("OverDueMemeberNotificationExpErr")
                    print(e)
        except Exception as e:
            print("GS#get_due_date")
            print(e)

        try:
            return obj.due_date.strftime("%d-%m-%Y")
        except Exception as e:
            print("Err")
            print(e)
            return None

    @staticmethod
    def get_start_date(obj):
        """this get_start_date method get due date 
        with the correct format
        """
        if not obj:
            return None
        try:
            return obj.start_date.strftime("%d-%m-%Y")
        except Exception as e:
            print("GS#get_due_date")
            print(e)
            return obj.start_date

    @staticmethod
    def get_reminder_date(obj):
        """this get_reminder_date method get due date 
        with the correct format
        """
        if not obj:
            return None
        try:
            return obj.reminder.strftime("%d-%m-%Y")
        except Exception as e:
            print("GS#get_due_date")
            print(e)
            return obj.reminder

    @staticmethod
    def get_matrix_config_detail(obj):
        """get_matrix_config_detail"""
        matrix_config_detail_dict = {}
        _imp_urg_dict = {"High": "0", "Medium": "50", "Low": "100"}
        try:
            matrix_instance = obj.matrix_type_config.task_type_config.all()
            for matrix_data in matrix_instance:
                matrix_config_detail_dict[
                    str(matrix_data.rule_name)] = _imp_urg_dict[
                        str(matrix_data.priority_status)
                    ]
            return matrix_config_detail_dict
        except Exception as e:
            print("#Gs164-get_matrix_config_detail")
            print(e)
            return matrix_config_detail_dict


class CreateTaskCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComments
        fields = "__all__"


class TaskCommentsSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField("get_members_list")
    owner_status = serializers.SerializerMethodField("get_owner_status")

    class Meta:
        model = TaskComments
        fields = "__all__"

    def get_owner_status(self, obj):
        """
        This get_comment_owner_status method used to get
        this comment owner is self or other user
        """
        try:
            return (True 
                    if self.context["login_user"].id == obj.members.id else 
                    False)
        except Exception as e:
            print("getOwnerStatus.Exception.Errors")
            print(e)
            return False

    @staticmethod
    def get_members_list(obj):
        """this get_members_list method get the priority status as
        per priority config
        """
        try:
            if obj.members:
                return MemberSerializer(obj.members).data
            else:
                return {}
        except Exception as e:
            print("MemberSerializer.DoesNotExist: %s" % e)
            return obj.members if obj.members else {}
