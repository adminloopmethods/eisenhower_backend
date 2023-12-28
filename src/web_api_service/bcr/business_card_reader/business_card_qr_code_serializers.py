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
from core.constants import ACCESS_STATUS


class QRBusinessCardFaxSerializer(serializers.ModelSerializer):
    """
    BusinessCardFaxSerializer
    """

    class Meta:
        model = BusinessCardFax
        fields = ("fax_value", "type")


class QRBusinessCardJobSerializer(serializers.ModelSerializer):
    """
    BusinessCardJobSerializer
    """

    class Meta:
        model = BusinessCardJob
        fields = ("job_value", "type")


class QRBusinessCardMobileSerializer(serializers.ModelSerializer):
    """
    BusinessCardMobileSerializer
    """

    class Meta:
        model = BusinessCardMobile
        fields = ("mobile_value", "type")


class QRBusinessCardEmailSerializer(serializers.ModelSerializer):
    """
    BusinessCardEmailSerializer
    """

    class Meta:
        model = BusinessCardEmail
        fields = ("email_value", "type")


class QRBusinessCardSocialNetworkSerializer(serializers.ModelSerializer):
    """
    BusinessCardSocialNetworkSerializer
    """

    class Meta:
        model = BusinessCardSocialNetwork
        fields = ("social_network_value", "type")


class QRBusinessCardAddressSerializer(serializers.ModelSerializer):
    """
    BusinessCardAddressSerializer
    """

    class Meta:
        model = BusinessCardAddress
        fields = ("type", "street", "city", "region", "country", "zip_code")


class QRBusinessCardDatesSerializer(serializers.ModelSerializer):
    """
    BusinessCardDatesSerializer
    """

    class Meta:
        model = BusinessCardDates
        fields = ("date", "type")


class QRBusinessCardWebSerializer(serializers.ModelSerializer):
    """
    BusinessCardWebSerializer
    """

    class Meta:
        model = BusinessCardWeb
        fields = ("website", "type")


class QRCategoryGroupMastersSerializer(serializers.ModelSerializer):
    """
    CategoryGroupMastersSerializer
    """

    is_predefined = serializers.SerializerMethodField("get_is_predefined")

    class Meta:
        model = CategoryGroupMaster
        fields = ("category_name", "color_hex_code", "is_predefined")

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


class QRBusinessCardReaderManagerSerializer(serializers.ModelSerializer):
    """
    BusinessCardReaderManagerSerializer
    this serializer used to convert the all business card data
    """

    jobs = serializers.SerializerMethodField("get_jobs")
    webs = serializers.SerializerMethodField("get_webs")
    # notes = serializers.SerializerMethodField('get_notes')
    social_network = serializers.SerializerMethodField("get_social_network")
    category_data = serializers.SerializerMethodField("category_group")
    color_hex_code = serializers.SerializerMethodField("get_color_code")
    mobile_numbers = serializers.SerializerMethodField("get_mobile_numbers")
    faxs = serializers.SerializerMethodField("get_faxs")
    dates = serializers.SerializerMethodField("get_dates")
    emails = serializers.SerializerMethodField("get_emails")
    address = serializers.SerializerMethodField("get_address")

    class Meta:
        model = BusinessCardReaderManager
        fields = (
            # 'id',
            # 'business_image',
            # 'nick_name',
            # 'title',
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
            # 'category_group',
            "category_data",
            "color_hex_code",
            # 'user',
            # 'is_card_retrived',
            # 'retrive_status',
            # 'reason_for_failed',
            # 'created_at',
            # all abby attr
            "prefix",
            "department",
            "position",
            "email_work",
            "email_personal",
            "contact_number_personal",
            "contact_number_work",
            "website",
            # 'address_type',
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
        )

    @staticmethod
    def category_group(instance):
        try:
            if not instance.category_group:
                return {}
            return {
                # 'id': instance.category_group.id,
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
        qr_code_address_dict = {}
        try:
            qr_code_address = QRBusinessCardAddressSerializer(
                instance.bussines_card_master_address.filter(), many=True
            ).data
            for _data in qr_code_address:
                qr_code_address_dict[_data["type"]] = {
                    "street": _data["street"],
                    "city": _data["city"],
                    "region": _data["region"],
                    "country": _data["country"],
                    "zip_code": _data["zip_code"],
                }
            return qr_code_address_dict
        except Exception as e:
            print("BuisnessAddressErr")
            print(e)
            return {}

    @staticmethod
    def get_social_network(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        qr_code_social_network_dict = {}
        try:
            qr_social_network_data = QRBusinessCardSocialNetworkSerializer(
                instance.bussines_card_master_social_network.filter(), many=True
            ).data
            for _data in qr_social_network_data:
                qr_code_social_network_dict[_data["type"]] = {
                    _data["type"]: _data["social_network_value"],
                }
            return qr_code_social_network_dict
        except Exception as e:
            print("getSocialNetworkErr")
            print(e)
            return {}

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
            qr_business_data = QRBusinessCardEmailSerializer(
                instance.bussines_card_master_email.filter(), many=True
            ).data
            for _data in qr_business_data:
                business_email_dict[_data["type"]] = {
                    _data["type"]: _data["email_value"],
                }
            return business_email_dict
        except Exception as e:
            print("BusinessEmailErr")
            print(e)
            return {}

    @staticmethod
    def get_mobile_numbers(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        qr_mobile_numers_dict = {}
        try:
            qr_mobile_numers = QRBusinessCardMobileSerializer(
                instance.bussines_card_master_mobile.filter(), many=True
            ).data
            for _data in qr_mobile_numers:
                qr_mobile_numers_dict[_data["type"]] = {
                    _data["type"]: _data["mobile_value"],
                }
            return qr_mobile_numers_dict
        except Exception as e:
            print("BusinessMobileErr")
            print(e)
            return {}

    @staticmethod
    def get_faxs(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        qr_fax_dict = {}
        try:
            qr_fax_data = QRBusinessCardFaxSerializer(
                instance.bussines_card_master_fax.filter(), many=True
            ).data
            for _data in qr_fax_data:
                qr_fax_dict[_data["type"]] = {
                    _data["type"]: _data["fax_value"],
                }
            return qr_fax_dict
        except Exception as e:
            print("BusinessFaxErr")
            print(e)
            return {}

    @staticmethod
    def get_jobs(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        job_response_list = []
        qr_job_dict = {}
        try:
            job_serializer_data = QRBusinessCardJobSerializer(
                instance.bussines_card_master_Job.filter(), many=True
            ).data
            if not job_serializer_data:
                return job_response_list

            for _data in job_serializer_data:
                qr_job_dict[_data["type"]] = {_data["type"]: _data["job_value"]}
            return qr_job_dict
        except Exception as e:
            print("BusinessJobsErr")
            print(e)
            return []

    @staticmethod
    def get_dates(instance):
        """
        Args:
            instance (obj): this instance used to mapping
            all instance variable of serializers

        return : []: address array
        """
        qr_dates_dict = {}
        try:
            qr_dates_data = QRBusinessCardDatesSerializer(
                instance.bussines_card_master_date.filter(), many=True
            ).data
            for _data in qr_dates_data:
                qr_dates_dict[_data["type"]] = {_data["type"]: _data["date"]}
            return qr_dates_dict
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
            qr_web_data = QRBusinessCardWebSerializer(
                instance.bussines_card_master_web.filter(), many=True
            ).data

            for _data in qr_web_data:
                business_card_web_dict[_data["type"]] = {
                    _data["type"]: _data["website"]
                }
            return business_card_web_dict
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
            return QRBusinessCardNotesSerializer(
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
