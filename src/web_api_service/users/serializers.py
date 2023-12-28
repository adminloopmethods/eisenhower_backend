# import rest apps
from django.db.models import Q
from rest_framework import serializers

# import models
from user.models import CustomUsers
from user.models import Team
# import member mapping
from user.models import UserMemberMapping
from user.models import UserStickyNotes


class CustomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'mobile_with_isd',
            'isd',
            'profile_picture',
            'department',
            'role',
            'color',
            'language',
            'language_code',
            'role_code'
        )

    role = serializers.SerializerMethodField('get_role')
    color = serializers.SerializerMethodField('get_color')
    language_code = serializers.SerializerMethodField('get_language_code')
    role_code = serializers.SerializerMethodField('get_role_code')

    @staticmethod
    def get_role(obj):
        """this get_role method used to get user role
        """
        try:
            if obj.language.language_code == 'ENG':
                return str(obj.role.role_name) if obj.role else None
            if obj.language.language_code == 'ITL':
                return str(obj.role.role_in_italian) if obj.role else None
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_role_code(self, obj):
        """
        get_role_code
        """
        try:
            return str(obj.role.role) if obj.role else None
        except Exception as e:
            print('RoleException')
            print(e)
            return None

    @staticmethod
    def get_color(obj):
        """this get_role method used to get user role
        """
        return str(obj.color_hex_code) if obj.color_hex_code else None

    @staticmethod
    def get_language_code(obj):
        """this get_role method used to get user role
        """
        return str(obj.language.language_code) if obj.language else None


class UpdateUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'mobile_with_isd',
            'isd',
            'profile_picture',
            'department',
        )


class MemberDetailSerializer(serializers.ModelSerializer):
    """
    MemberDetailSerializer
    """
    color = serializers.SerializerMethodField('get_color')
    role = serializers.SerializerMethodField('get_role')
    department = serializers.SerializerMethodField('get_department')
    role_id = serializers.SerializerMethodField('get_role_id')
    department_id = serializers.SerializerMethodField('get_department_id')
    team_association = serializers.SerializerMethodField('get_team_association')
    mobile = serializers.SerializerMethodField('get_mobile_with_isd')
    mobile_without_isd = serializers.SerializerMethodField('get_mobile_with_out_isd')
    isd = serializers.SerializerMethodField('get_mobile_isd')

    class Meta:
        model = CustomUsers
        exclude = ('created_by', 'updated_by', 'mobile_with_isd',
                   #    'isd',
                   'device_id',
                   'imei_no',
                   'device_name',
                   'code',
                   'designation',
                   'profile_picture',
                   'country',
                   'state',
                   'city')

    @staticmethod
    def get_color(obj):
        """this get_color method used to get user role
        """
        return str(obj.color_hex_code) if obj.color_hex_code else None

    @staticmethod
    def get_role(obj):
        """this get_role method used to get user role
        """
        return str(obj.role.role_name) if obj.role else None

    @staticmethod
    def get_department(obj):
        """this get_role method used to get user role
        """
        return str(obj.department.department_name) if obj.department else None

    @staticmethod
    def get_role_id(obj):
        """this get_role method used to get user role
        """
        return str(obj.role.id) if obj.role else None

    @staticmethod
    def get_department_id(obj):
        """this get_role method used to get user role
        """
        return str(obj.department.id) if obj.department else None

    @staticmethod
    def get_team_association(obj):
        """this get_team_association used to get user role
        """
        try:
            return TeamListSerializer(Team.objects.filter(members__id=obj.id),
                                      many=True).data
        except Exception as e:
            print('*get_team_association.Exception')
            print(e)
            return []

    @staticmethod
    def get_mobile_with_isd(obj):
        """this get_mobile_with_isd used to get user role
        """
        if not obj:
            return None
        try:
            if obj.isd:
                return ''.join([str('+'), str(obj.isd), ' ', str(obj.mobile)])
            else:
                return ''.join([str('+'), str('39'), ' ', str(obj.mobile)])
        except Exception as e:
            print('*get_mobile_with_isd.Exception')
            print(e)
            return None

    @staticmethod
    def get_mobile_with_out_isd(obj):
        """this get_mobile_with_isd used to get user role
        """
        if not obj:
            return None
        try:
            return str(obj.mobile)
        except Exception as e:
            print('*get_mobile_with_isd.Exception')
            print(e)
            return None

    @staticmethod
    def get_mobile_isd(obj):
        """this get_mobile_with_isd used to get user role
        """
        if not obj:
            return None
        try:
            return str(obj.isd) if obj.isd else str(91)
        except Exception as e:
            print('*get_mobile_with_isd.Exception')
            print(e)
            return None


class GetMemberDetailSerializer(serializers.ModelSerializer):
    """
    MemberDetailSerializer
    """
    color = serializers.SerializerMethodField('get_color')
    role = serializers.SerializerMethodField('get_role')
    role_code = serializers.SerializerMethodField('get_role_code')
    department = serializers.SerializerMethodField('get_department')
    role_id = serializers.SerializerMethodField('get_role_id')
    department_id = serializers.SerializerMethodField('get_department_id')
    team_association = serializers.SerializerMethodField('get_team_association')
    mobile = serializers.SerializerMethodField('get_mobile_with_isd')
    mobile_without_isd = serializers.SerializerMethodField('get_mobile_with_out_isd')
    isd = serializers.SerializerMethodField('get_mobile_isd')

    class Meta:
        model = CustomUsers
        exclude = ('created_by', 'updated_by', 'mobile_with_isd',
                   #    'isd',
                   'device_id',
                   'imei_no',
                   'device_name',
                   'code',
                   'designation',
                   'profile_picture',
                   'country',
                   'state',
                   'city')

    @staticmethod
    def get_color(obj):
        """this get_color method used to get user role
        """
        return str(obj.color_hex_code) if obj.color_hex_code else None

    def get_role(self, obj):
        """this get_role method used to get user role
        """
        try:
            if self.context['user_instance'].language.language_code == 'ENG':
                return str(obj.role.role_name) if obj.role else None
            if self.context['user_instance'].language.language_code == 'ITL':
                return str(obj.role.role_in_italian) if obj.role else None
        except Exception as e:
            print('RoleException')
            print(e)
            return None

    def get_role_code(self, obj):
        """
        get_role_code
        """
        try:
            return str(obj.role.role) if obj.role else None
        except Exception as e:
            print('RoleException')
            print(e)
            return None

    @staticmethod
    def get_department(obj):
        """this get_role method used to get user role
        """
        return str(obj.department.department_name) if obj.department else None

    @staticmethod
    def get_role_id(obj):
        """this get_role method used to get user role
        """
        return str(obj.role.id) if obj.role else None

    @staticmethod
    def get_department_id(obj):
        """this get_role method used to get user role
        """
        return str(obj.department.id) if obj.department else None

    @staticmethod
    def get_team_association(obj):
        """this get_team_association used to get user role
        """
        try:
            return TeamListSerializer(Team.objects.filter(members__id=obj.id),
                                      many=True).data
        except Exception as e:
            print('*get_team_association.Exception')
            print(e)
            return []

    @staticmethod
    def get_mobile_with_isd(obj):
        """this get_mobile_with_isd used to get user role
        """
        if not obj:
            return None
        try:
            if obj.isd:
                return ''.join([str('+'), str(obj.isd), ' ', str(obj.mobile)])
            else:
                return ''.join([str('+'), str('39'), ' ', str(obj.mobile)])
        except Exception as e:
            print('*get_mobile_with_isd.Exception')
            print(e)
            return None

    @staticmethod
    def get_mobile_with_out_isd(obj):
        """this get_mobile_with_isd used to get user role
        """
        if not obj:
            return None
        try:
            return str(obj.mobile)
        except Exception as e:
            print('*get_mobile_with_isd.Exception')
            print(e)
            return None

    @staticmethod
    def get_mobile_isd(obj):
        """this get_mobile_with_isd used to get user role
        """
        if not obj:
            return None
        try:
            return str(obj.isd) if obj.isd else str(91)
        except Exception as e:
            print('*get_mobile_with_isd.Exception')
            print(e)
            return None


class MemberSerializer(serializers.ModelSerializer):

    color = serializers.SerializerMethodField('get_color')


    class Meta:
        model = CustomUsers
        exclude = ('created_by', 'updated_by', 'mobile_with_isd',
                   # 'access_status',
                   #    'isd',
                   'device_id',
                   'imei_no',
                   'device_name',
                   'code',
                   'designation',
                   'profile_picture',
                   'country',
                   'state',
                   'city')

    @staticmethod
    def get_color(obj):
        """this get_color method used to get user role
        """
        return str(obj.color_hex_code) if obj.color_hex_code else None


class UserMemberMappingSerializer(serializers.ModelSerializer):
    # members = MemberDetailSerializer(many=True, read_only=True)
    # members = GetMemberDetailSerializer(many=True, read_only=True)
    members = serializers.SerializerMethodField('get_member_list')

    # members = serializers.SerializerMethodField('get_member_list_exclude_login_user')

    class Meta:
        model = UserMemberMapping
        fields = ('id', 'user', 'members')

    def get_member_list_exclude_login_user(self, obj):
        """
        this get_member_list_exclude_login_user serializer method return a list of member by deparment
        """
        try:
            return MemberDetailSerializer(
                CustomUsers.objects.exclude(auth_user_id=self.context['auth_user_id']).filter(),
                many=True).data
        except Exception as e:
            print(e)
            return []

    def get_member_list(self, obj):
        """
        get_member_list
        """
        try:
            member_serializer = GetMemberDetailSerializer(
                obj.members.filter(),
                context={'user_instance': self.context['user_instance']},
                many=True)
            return member_serializer.data if member_serializer else []
        except Exception as e:
            print('getMemberListErr')
            print(e)


class UserMemberSearchMappingSerializer(serializers.ModelSerializer):
    # members = MemberDetailSerializer(many=True, read_only=True)

    members = serializers.SerializerMethodField('get_member_list_exclude_login_user')

    class Meta:
        model = UserMemberMapping
        fields = ('id', 'user', 'members')

    def get_member_list_exclude_login_user(self, obj):
        """
        this get_member_list_exclude_login_user serializer method return a list of member by deparment
        """
        try:
            # member_serializer = GetMemberDetailSerializer(
            #     CustomUsers.objects.exclude(
            #         auth_user_id=self.context['user_instance'].auth_user.id
            #     ).filter(
            #         Q(first_name__istartswith=self.context['first_name']) &
            #         Q(last_name__istartswith=self.context['last_name'])
            #     ),
            #     context={'user_instance': self.context['user_instance']},
            #     many=True
            # )
            member_serializer = GetMemberDetailSerializer(
                obj.members.filter(
                    Q(first_name__istartswith=self.context['first_name']) &
                    Q(last_name__istartswith=self.context['last_name'])
                ),
                context={'user_instance': self.context['user_instance']},
                many=True
            )
            if member_serializer:
                return member_serializer.data
            else:
                return []
        except Exception as e:
            print('getMemberListExampleLoginUserExceptionErr')
            print(e)
            return []


class UserMemberMappingByDepartmentSerializer(serializers.ModelSerializer):
    # members = MemberDetailSerializer(many=True, read_only=True)

    members = serializers.SerializerMethodField(
        'get_member_list_by_department')

    class Meta:
        model = UserMemberMapping
        fields = ('id', 'user', 'members')

    def get_member_list_by_department(self, obj):
        """
        this get_member_list_by_department serializer method return a list of member by deparment
        """
        try:
            return MemberDetailSerializer(
                CustomUsers.objects.filter(
                    department=self.context['department']),
                many=True).data
        except Exception as e:
            print(e)
            return []


class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamDetailSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField('get_department_value')

    class Meta:
        model = Team
        fields = '__all__'

    @staticmethod
    def get_department_value(obj):
        """this get_department_value method used to get department name
        """
        return str(obj.department.department_name) if obj.department else ""


class TeamMemberSerializer(serializers.ModelSerializer):
    members = MemberDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class TeamListSerializer(serializers.ModelSerializer):
    """
    TeamListSerializer
    """

    class Meta:
        model = Team
        fields = ('team_name',)


class UserStickyNotesSerializer(serializers.ModelSerializer):
    """
    UserStickyNotesSerializer
    """

    class Meta:
        model = UserStickyNotes
        fields = '__all__'
