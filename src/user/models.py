import uuid

# from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from configuration.models import ColorMaster, Departments
# import relation dependencies
from configuration.models import Language
from configuration.models import Topics
from configuration.models import UserRoleMaster
# import constant
from core.constants import ACCESS_STATUS, DEVICE_TYPE, APP_TYPE
from core.models import ABSTRACTCreateUpdateByModel
# Create your models here.
# import abstract modules\9oli'j
#ji[o9ip[h
# =[op8u[g
# v0hu97e[m78oup\cf8k6859tp'
# 055-=\df1from core.models import vkujku[;ioijmo[oihg]]
from core.models import ABSTRACTLocationMaster
from core.models import ABSTRACTStatusModel , ABSTRACTDateModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models, IntegrityError
import uuid
from account.models import User



class CustomUsers(
    ABSTRACTDateModel,
    ABSTRACTStatusModel,
    ABSTRACTCreateUpdateByModel,
    ABSTRACTLocationMaster
):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    # Customer basic details
    #########################
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=100,
        verbose_name='Email Id',
        null=True, blank=True
    )
    mobile = models.CharField(max_length=15, null=True, blank=True)
    mobile_with_isd = models.CharField(
        max_length=20,
        verbose_name='Mobile No. with ISD Code',
        null=True, blank=True
    )
    isd = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999), MinValueValidator(1)],
        verbose_name='ISD/Country Code',
        null=True, blank=True
    )
    access_status = models.CharField(
        max_length=100,
        choices=ACCESS_STATUS)

    # device related data
    #######################
    registration_type = models.CharField(
        max_length=255,
        choices=DEVICE_TYPE,
        verbose_name='Registration Type'
    )
    device_id = models.CharField(max_length=255, blank=True, null=True)
    imei_no = models.CharField(max_length=100, blank=True, null=True)
    device_name = models.CharField(max_length=100, blank=True, null=True)

    # other details
    ####################
    code = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name='Customer Code'
    )
    designation = models.CharField(
        max_length=100,
        verbose_name='Designation',
        null=True, blank=True
    )
    profile_picture = models.ImageField(
        upload_to='user_profile_images/',
        verbose_name='User Profile Pic',
        null=True, blank=True
    )

    # all FK relation models
    #############################
    department = models.ForeignKey(
        Departments,
        on_delete=models.CASCADE,
        related_name='_departments_users',
        null=True, blank=True
    )

    color = models.ForeignKey(
        ColorMaster,
        on_delete=models.CASCADE,
        related_name='color_master_user',
        null=True, blank=True
    )
    color_hex_code = models.CharField(max_length=20, null=True, blank=True)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, null=True, blank=True)
    is_cognito_user = models.BooleanField(default=False)
    role = models.ForeignKey(
        UserRoleMaster,
        on_delete=models.CASCADE,
        related_name='_role_user',
        null=True, blank=True
    )
    application_type = models.CharField(max_length=200, choices=APP_TYPE,
                                        null=True, blank=True)

    # auth user OneToOne for mapped the auth user for authentication
    # and use django auth user security features
    ##############################################
    auth_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_auth'
    )

    # cognito id and access token for manipulate 
    # the all cognito and third party services
    cognito_access_token = models.TextField(null=True, blank=True)
    cognito_id_token = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "     User Profile"
        verbose_name_plural = "     User Profile"
        db_table = 'user_profile'
        ordering = ('created_at',)

    def __str__(self):
        try:
            return ''.join([str(self.first_name), ' ', str(self.last_name)])
        except Exception as e:
            print('ExceptionCustomUsersErr')
            print(e)
            return self.first_name


class UserMemberMapping(ABSTRACTDateModel,
                        ABSTRACTStatusModel,
                        ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # mapping related fields
    user = models.OneToOneField(CustomUsers, on_delete=models.CASCADE, related_name='custom_user_member')
    members = models.ManyToManyField(CustomUsers)

    class Meta:
        verbose_name = "    User members"
        verbose_name_plural = "    User members"
        db_table = 'user_member_mapping'

    def __str__(self):
        return self.user.first_name

    def get_members_list(self):
        return ', '.join([str(i.first_name) for i in self.members.all()[:3]])

    get_members_list.short_description = 'Members'


class UserDepartmentMapping(ABSTRACTDateModel,
                            ABSTRACTStatusModel,
                            ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # mapping related fields
    user = models.OneToOneField(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='_custom_user_department')
    departments = models.ManyToManyField(Departments)

    class Meta:
        verbose_name = "    User Departments"
        verbose_name_plural = "    User Departments"
        db_table = 'user_department_mapping'

    def __str__(self):
        return self.user.first_name

    def get_departments_list(self):
        return ', '.join([str(i.department_name) for i in self.departments.all()[:3]])

    get_departments_list.short_description = 'Departments'


class UserTopicMapping(ABSTRACTDateModel,
                       ABSTRACTStatusModel,
                       ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    # mapping related fields
    user = models.OneToOneField(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='_custom_user_topics')
    topics = models.ManyToManyField(Topics)

    class Meta:
        verbose_name = "   User Topics"
        verbose_name_plural = "   User Topics"
        db_table = 'user_topic_mapping'

    def __str__(self):
        return self.user.first_name

    def get_topics_list(self):
        return ', '.join([str(i.topic_name) for i in self.topics.all()[:3]])

    get_topics_list.short_description = 'topics'


class UserStickyNotes(ABSTRACTDateModel,
                      ABSTRACTStatusModel,
                      ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    # notes details
    note = models.TextField(null=True, blank=True)
    user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '  Sticky Notes'
        verbose_name_plural = '  Sticky Notes'
        db_table = 'user_sticky_notes'

    def __str__(self):
        return self.note


class Team(ABSTRACTDateModel,
           ABSTRACTStatusModel,
           ABSTRACTCreateUpdateByModel):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    team_name = models.CharField(max_length=30, unique=True)
    access_status = models.CharField(max_length=100, choices=ACCESS_STATUS)
    members = models.ManyToManyField(CustomUsers)
    department = models.ForeignKey(Departments,
                                   on_delete=models.CASCADE,
                                   related_name='department_team_inst')
    user = models.ForeignKey(
        CustomUsers, on_delete=models.CASCADE, related_name='team_user')

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Team'
        db_table = 'teams'

    def __str__(self):
        return self.team_name
