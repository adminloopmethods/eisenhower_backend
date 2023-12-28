from rest_framework import serializers

from cards.models import BusinessCardAddress
from cards.models import BusinessCardDates
from cards.models import BusinessCardEmail
from cards.models import BusinessCardFax
from cards.models import BusinessCardJob
from cards.models import BusinessCardMobile
from cards.models import BusinessCardNotes
from cards.models import BusinessCardReaderManager
from cards.models import BusinessCardSocialLink
from cards.models import BusinessCardSocialNetwork
from cards.models import BusinessCardWeb
# Register your models here.
from cards.models import CategoryGroupMaster
from configuration.models import TestFilesUploadForRequest
from core.constants import ACCESS_STATUS


class TestFilesUploadForRequestSerializer(serializers.ModelSerializer):
    """
    TestFilesUploadForRequestSerializer
    """

    class Meta:
        model = TestFilesUploadForRequest
        fields = "__all__"


class BusinessCardFaxSerializer(serializers.ModelSerializer):
    """
    BusinessCardFaxSerializer
    """

    class Meta:
        model = BusinessCardFax
        fields = "__all__"


class BusinessCardJobSerializer(serializers.ModelSerializer):
    """
    BusinessCardJobSerializer
    """

    class Meta:
        model = BusinessCardJob
        fields = ("id", "type", "job_value")


class BusinessCardMobileSerializer(serializers.ModelSerializer):
    """
    BusinessCardMobileSerializer
    """

    class Meta:
        model = BusinessCardMobile
        fields = "__all__"


class BusinessCardEmailSerializer(serializers.ModelSerializer):
    """
    BusinessCardEmailSerializer
    """

    class Meta:
        model = BusinessCardEmail
        fields = "__all__"


class BusinessCardSocialNetworkSerializer(serializers.ModelSerializer):
    """
    BusinessCardSocialNetworkSerializer
    """

    class Meta:
        model = BusinessCardSocialNetwork
        fields = "__all__"


class BusinessCardAddressSerializer(serializers.ModelSerializer):
    """
    BusinessCardAddressSerializer
    """

    class Meta:
        model = BusinessCardAddress
        fields = "__all__"


class BusinessCardDatesSerializer(serializers.ModelSerializer):
    """
    BusinessCardDatesSerializer
    """

    class Meta:
        model = BusinessCardDates
        fields = "__all__"


class BusinessCardWebSerializer(serializers.ModelSerializer):
    """
    BusinessCardWebSerializer
    """

    class Meta:
        model = BusinessCardWeb
        fields = "__all__"


class BusinessCardNotesSerializer(serializers.ModelSerializer):
    """
    BusinessCardNotesSerializer
    """

    class Meta:
        model = BusinessCardNotes
        fields = "__all__"


class CategoryGroupMastersSerializer(serializers.ModelSerializer):
    """
    CategoryGroupMastersSerializer
    """

    is_predefined = serializers.SerializerMethodField("get_is_predefined")

    class Meta:
        model = CategoryGroupMaster
        fields = "__all__"

    def get_is_predefined(self, obj):
        """
        Args:
            obj (_type_): all predefined status manage from category
            access_status field
        Returns:
            True/False
        """
        try:
            if not obj:
                return None
            if obj.access_status == ACCESS_STATUS[0][0]:  # allow_to_all check
                return True
            if obj.access_status == ACCESS_STATUS[1][0]:  # self only check
                return False
        except Exception as e:
            print("getIsPredefinedErr")
            print(e)
            return None


class BusinessCardReaderManagerSerializer(serializers.ModelSerializer):
    """
    BusinessCardReaderManagerSerializer
    this serializer used to convert the all business card data
    """

    jobs = serializers.SerializerMethodField("get_jobs")
    webs = serializers.SerializerMethodField("get_webs")
    social_network = serializers.SerializerMethodField("get_social_network")
    category_data = serializers.SerializerMethodField("category_group")
    color_hex_code = serializers.SerializerMethodField("get_color_code")
    mobile_numbers = serializers.SerializerMethodField("get_mobile_numbers")
    faxs = serializers.SerializerMethodField("get_faxs")
    dates = serializers.SerializerMethodField("get_dates")
    emails = serializers.SerializerMethodField("get_emails")
    address = serializers.SerializerMethodField("get_address")
    is_editable = serializers.SerializerMethodField("get_is_editable")

    # notes = serializers.SerializerMethodField('get_notes')

    class Meta:
        model = BusinessCardReaderManager
        fields = (
            "id",
            "business_image",
            "nick_name",
            "title",
            "first_name",
            "second_name",
            "last_name",
            "suffix",
            "company_name",
            "telephone_office",
            "telephone_mobile",
            "fax",
            "telephone_home",
            "e_mail",
            "country",
            "city",
            "street",
            "postal_code",
            "web",
            "facebook",
            "category_group",
            "category_data",
            "color_hex_code",
            "user",
            "is_card_retrived",
            "retrive_status",
            "reason_for_failed",
            "created_at",
            # all abby attr
            "prefix",
            "department",
            "position",
            "email_work",
            "email_personal",
            "contact_number_personal",
            "contact_number_work",
            "website",
            "address_type",
            "region",
            "zip_code",
            "address",
            "social_network",
            "emails",
            "mobile_numbers",
            "faxs",
            "jobs",
            "dates",
            "webs",
            "notes",
            "is_editable"
        )

    @staticmethod
    def get_is_editable(instance):
        try:
            if (
                    instance.retrive_status == 'discard' or 
                    instance.retrive_status == 'failed' and
                    instance.first_name or
                    instance.last_name or
                    instance.nick_name or
                    instance.company_name or
                    instance.telephone_mobile or
                    instance.telephone_mobile or
                    instance.telephone_mobile or
                    instance.dates
            ):
                BusinessCardReaderManager.objects.filter(
                    id=instance.id, is_active=True
                ).update(is_editable=True)
                return True
            else:
                False
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def category_group(instance):
        try:
            if not instance.category_group:
                return {}
            return {
                "id": instance.category_group.id,
                "category_name": instance.category_group.category_name,
                "color_hex_code": instance.category_group.color_hex_code,
            }
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_color_code(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers
        """
        try:
            return (
                instance.category_group.color_hex_code
                if instance.category_group
                else ""
            )
        except Exception as e:
            print("getColorErr")
            print(e)
            return ""

    @staticmethod
    def get_address(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        try:
            return BusinessCardAddressSerializer(
                instance.bussines_card_master_address.filter(), many=True
            ).data
        except Exception as e:
            print("BuisnessAddressErr")
            print(e)
            return []

    @staticmethod
    def get_social_network(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        try:
            return BusinessCardSocialNetworkSerializer(
                instance.bussines_card_master_social_network.filter(), many=True
            ).data
        except Exception as e:
            print("getSocialNetworkErr")
            print(e)
            return []

    @staticmethod
    def get_emails(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        business_email_dict = {}
        try:
            return BusinessCardEmailSerializer(
                instance.bussines_card_master_email.filter(), many=True
            ).data
        except Exception as e:
            print("BusinessEmailErr")
            print(e)
            return []

    @staticmethod
    def get_mobile_numbers(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        try:
            return BusinessCardMobileSerializer(
                instance.bussines_card_master_mobile.filter(), many=True
            ).data
        except Exception as e:
            print("BusinessEmailErr")
            print(e)
            return []

    @staticmethod
    def get_faxs(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        try:
            return BusinessCardFaxSerializer(
                instance.bussines_card_master_fax.filter(), many=True
            ).data
        except Exception as e:
            print("BusinessFaxErr")
            print(e)
            return []

    @staticmethod
    def get_jobs(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        job_response_list = [
            {"id": None, "type": "company", "job_value": None},
            {"id": None, "type": "position", "job_value": None},
            {"id": None, "type": "department", "job_value": None},
        ]
        jobs_response_data = {}
        try:
            job_serializer_data = BusinessCardJobSerializer(
                instance.bussines_card_master_Job.filter(), many=True
            ).data
            # if not job_serializer_data:
            #     return job_response_list

            # print('job_serializer_data', job_serializer_data)
            # count = 0
            # for job_data in job_serializer_data:
            #     print('countssssssssssss', count)
            #     jobs_response_data = {}
            #     print('job_data', job_data['type'])
            #     if job_data['type'] == 'company':
            #         jobs_response_data['id'] = job_data['id']
            #         jobs_response_data['type'] = job_data['type']
            #         jobs_response_data['job_value'] = job_data['job_value']
            #     if job_data['type'] == 'position':
            #         jobs_response_data['id'] = job_data['id']
            #         jobs_response_data['type'] = job_data['type']
            #         jobs_response_data['job_value'] = job_data['job_value']
            #     if job_data['type'] == 'department':
            #         jobs_response_data['id'] = job_data['id']
            #         jobs_response_data['type'] = job_data['type']
            #         jobs_response_data['job_value'] = job_data['job_value']

            #     print('jobs_response_data', jobs_response_data)
            #     job_response_list.append(jobs_response_data)
            #     count += 1
            # job_response_list = [
            #     i for i in job_response_list if not (
            #         (i['type'] == 'company' and i['job_value'] == None) or
            #         (i['type'] == 'position' and i['job_value'] == None) or
            #         (i['type'] == 'department' and i['job_value'] == None))
            # ]

            # return job_response_list
            if len(job_serializer_data) > 0:
                return job_serializer_data
            else:
                return job_response_list
        except Exception as e:
            print("BusinessJobsErr")
            print(e)
            return job_response_list

    @staticmethod
    def get_dates(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        try:
            return BusinessCardDatesSerializer(
                instance.bussines_card_master_date.filter(), many=True
            ).data
        except Exception as e:
            print("BusinessFaxErr")
            print(e)
            return []

    @staticmethod
    def get_webs(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        business_card_web_dict = {}
        try:
            return BusinessCardWebSerializer(
                instance.bussines_card_master_web.filter(), many=True
            ).data
        except Exception as e:
            print("BusinessWebsErr")
            print(e)
            return []

    @staticmethod
    def get_notes(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        try:
            return BusinessCardNotesSerializer(
                instance.bussines_card_master_notes.filter(), many=True
            ).data
        except Exception as e:
            print("BusinessNotesErr")
            print(e)
            return []


class BusinessCardSocialLinkSerializer(serializers.ModelSerializer):
    """
    BusinessCardSocialLinkSerializer
    """

    class Meta:
        model = BusinessCardSocialLink
        fields = "__all__"
