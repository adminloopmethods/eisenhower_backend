from itertools import chain

from _thread import start_new_thread

from cards.models import BusinessCardAddress
from cards.models import BusinessCardDates
from cards.models import BusinessCardEmail
from cards.models import BusinessCardFax
from cards.models import BusinessCardJob
from cards.models import BusinessCardMobile
from cards.models import BusinessCardNotes
from cards.models import BusinessCardReaderManager
from cards.models import BusinessCardSocialNetwork
from cards.models import BusinessCardWeb

# import business card models
from cards.models import CategoryGroupMaster
from cards.models import UserCategoryGroupMaster
from configuration.models import TestFilesUploadForRequest
from core.constants import ACCESS_STATUS

# import custom user
from user.models import CustomUsers
from web_api_service.bcr.abby_apis.abby_ocr_services import AbbyOcrReader
from web_api_service.bcr.business_card_reader.business_card_qr_code_serializers import (
    QRBusinessCardReaderManagerSerializer,
)

#  import serializers
from web_api_service.bcr.business_card_reader.business_card_serializers import \
    BusinessCardReaderManagerSerializer
from web_api_service.bcr.business_card_reader.business_card_serializers import \
    CategoryGroupMastersSerializer
from web_api_service.bcr.business_card_reader.update_business_card_details import \
    UpdateBusinessCardDetails
# category group id
from web_api_service.helpers.all_config_func import get_category_group_id


class BusinessCardReader:
    """
    BusinessCardReader
    """

    def __init__(self, **kwargs):
        self.business_card_instance = None
        self.auth_user_instance = kwargs.get("auth_user_instance", None)
        self.business_card_id = kwargs.get("business_card_id", None)
        self.business_card_data = kwargs.get("business_card_data", {})
        self.category_group_data = kwargs.get("category_group_data", {})
        self.card_data = kwargs.get("business_card_request_data", {})

        # for abby service attrs
        self.data_set_type = ""
        self.service_function = "recognition"
        self.application_type = "BCM"
        self._user_category_value_list = []

        # initiate the categoryGroupMaster Models
        self.category_group_entity = CategoryGroupMaster.objects.filter(
            is_active=True, access_status=ACCESS_STATUS[0][0]
        )

    def business_card_delete(self):
        """this business_card_delete method used to delete card using business
        card id

        args: self body {'business_card_id': 43}

        return: response: {}
        """
        try:
            business_card_obj = BusinessCardReaderManager.objects.filter(
                id=self.business_card_data["business_card_id"],
                user=self.auth_user_instance.user_auth,
                is_active=True,
            )
            if not business_card_obj:
                return None
            business_card_deleted = business_card_obj.delete()
            return (
                {"is_deleted": True}
                if business_card_deleted else
                {"is_deleted": False}
            )
        except Exception as e:
            print("businessCardDeleteErr")
            print(e)
            return None

    def business_card_list(self):
        """this business_card_list method used to get the
        all business card list from models
        """
        business_card_reader = BusinessCardReaderManager.objects.filter(
            user=self.auth_user_instance.user_auth, is_active=True
        ).order_by("-created_at")

        if not business_card_reader:
            return None

        # # for every time failed status
        try:
            UpdateBusinessCardDetails(
                auth_user_instance=self.auth_user_instance
            ).business_card_update_by_abby_response()
        except Exception as e:
            print("BusinessCardReaderManagerErr")
            print(e)

        try:
            return BusinessCardReaderManagerSerializer(
                business_card_reader, many=True
            ).data
        except Exception as e:
            print("ListSerializerErr")
            print(e)
            return None

    def get_business_card_instance(self):
        """this get_business_card_instance method used to
        get the business card instance
        """
        try:
            self.business_card_instance = BusinessCardReaderManager.objects.get(
                user_id=self.auth_user_instance.user_auth.id,
                id=self.business_card_id,
                is_active=True,
            )
        except BusinessCardReaderManager.DoesNotExist:
            print("BusinessCardReaderManager.DoesNotExist")
            self.business_card_instance = None

    def business_card_detail(self):
        """this business_card_detail method used to get the business card
        details by according a valid id
        """
        self.get_business_card_instance()
        if not self.business_card_instance:
            return None
        try:
            return BusinessCardReaderManagerSerializer(
                self.business_card_instance
            ).data
        except Exception as e:
            print("DictSerializerErr")
            print(e)
            return None

    def qr_code_business_card_detail(self):
        """this business_card_detail method used to get the business card
        details by according a valid id
        """
        self.get_business_card_instance()
        if not self.business_card_instance:
            return None
        try:
            return QRBusinessCardReaderManagerSerializer(
                self.business_card_instance
            ).data
        except Exception as e:
            print("DictSerializerErr")
            print(e)
            return None

    def update_business_card_address(self, address_data):
        """in this update_business_card_address method we
        update the business card address details

        args: self
              address_data: [{"type" :"company",
              "street": "Safdarjung enclave new Delhi seelampur delhi",
              "city": "Neww Delhi", "region": "North", "country": "India",
              "zip_code": "110051"},
              {"type": "home",
              "street": "Safdarjung enclave new Delhi seelampur delhi",
              "city": "Neww Delhi", "region": "North", "country": "India",
              "zip_code": "110051"}]

        return: None
        """
        # list_comprehension_update = [
        #     BusinessCardAddress.objects.update_or_create(
        #         business_card_id=self.business_card_id,
        #         type=address['type'], street=address['street'],
        #         defaults={
        #             'street': address['street'],
        #             'city': address['city'],
        #             'region': address['region'],
        #             'country': address['country'],
        #             'zip_code': address['zip_code'],
        #
        #         }
        #     ) for address in address_data
        # ]
        # return True if list_comprehension_update else False

        for address in address_data:
            business_card_create_instance = BusinessCardAddress.objects.filter(
                business_card_id=self.business_card_id,
                id=address.get("id", None)
            ).last()
            if business_card_create_instance:
                try:
                    BusinessCardAddress.objects.filter(
                        id=address.get("id", None)
                    ).update(
                        type=address["type"],
                        stree=address["street"],
                        city=address["city"],
                        region=address["region"],
                        country=address["country"],
                        zip_code=address["zip_code"],
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    BusinessCardAddress.objects.create(
                        business_card_id=self.business_card_id,
                        type=address["type"],
                        stree=address["street"],
                        city=address["city"],
                        region=address["region"],
                        country=address["country"],
                        zip_code=address["zip_code"],
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False

    def update_business_card_social_network(self, social_network_data):
        """in this update_business_card_social_network method we
        update the business card address details

        args: self
              social_network_data: [{"type": "facebook",
                                     "social_network_value": "fb,comss"}]

        return: True/False
        """
        # list_comprehension_update = [
        #     BusinessCardSocialNetwork.objects.update_or_create(
        #         business_card_id=self.business_card_id,
        #         type=social_network['type'],
        #         social_network_value=social_network['social_network_value'],
        #         defaults={
        #             'type': social_network['type'],
        #             'social_network_value': social_network['social_network_value'],
        #         }
        #     ) for social_network in social_network_data
        # ]
        # return True if list_comprehension_update else False

        for social_network in social_network_data:
            business_card_create_obj = BusinessCardSocialNetwork.objects.filter(
                business_card_id=self.business_card_id,
                id=social_network.get("id", None),
            ).last()
            if business_card_create_obj:
                try:
                    BusinessCardSocialNetwork.objects.filter(
                        id=social_network.get("id", None)
                    ).update(
                        type=social_network["type"],
                        social_network_value=social_network[
                            "social_network_value"
                        ],
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    BusinessCardSocialNetwork.objects.create(
                        business_card_id=self.business_card_id,
                        type=social_network["type"],
                        social_network_value=social_network[
                            "social_network_value"
                        ],
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False

    def update_business_card_emails(self, emails_data):
        """in this update_business_card_emails method we
        update the business card emails details
        args: self: emails_data: "emails": [{"type": "home", "email_value": "gousha@gmail.com"}],
        return: True/False
        """
        # email_data_list = emails_data
        print("emails_data", emails_data)
        # list_comprehension_update = [
        #     BusinessCardEmail.objects.update_or_create(business_card_id=self.business_card_id,
        #                                                # id=emails['id'],
        #                                                type=emails['type'],
        #                                                email_value=emails['email_value'],
        #                                                defaults={'type': emails['type'],
        #                                                          'email_value': emails['email_value']})
        #     for emails in emails_data
        # ]
        # return True if list_comprehension_update else False
        for emails in emails_data:
            business_card_create_instance = BusinessCardEmail.objects.filter(
                business_card_id=self.business_card_id,
                id=emails.get("id", None)
            ).last()
            if business_card_create_instance:
                try:
                    BusinessCardEmail.objects.filter(
                        id=emails.get("id", None)
                    ).update(
                        type=emails["type"], email_value=emails["email_value"]
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    BusinessCardEmail.objects.create(
                        business_card_id=self.business_card_id,
                        type=emails["type"],
                        email_value=emails["email_value"],
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False

    def update_business_card_mobile_numbers(self, mobile_numbers):
        """in this update_business_card_mobile_numbers method we
        update the business card mobile numbers details

        args: self
              mobile_numbers: [{"type": "home", "mobile_value": "88989898978"}]

        return: True/False
        """
        # list_comprehension_update = [
        #     BusinessCardMobile.objects.update_or_create(
        #         business_card_id=self.business_card_id,
        #         type=mobile_number['type'],
        #         mobile_value=mobile_number['mobile_value'],
        #         defaults={
        #             'type': mobile_number['type'],
        #             'mobile_value': mobile_number['mobile_value'],
        #         }
        #     ) for mobile_number in mobile_numbers
        # ]
        # return True if list_comprehension_update else False

        for mobile_number in mobile_numbers:
            business_card_create_instance = BusinessCardMobile.objects.filter(
                business_card_id=self.business_card_id,
                id=mobile_number.get("id", None)
            ).last()
            if business_card_create_instance:
                try:
                    BusinessCardMobile.objects.filter(
                        id=mobile_number.get("id", None)
                    ).update(
                        type=mobile_number["type"],
                        mobile_value=mobile_number["mobile_value"],
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    BusinessCardMobile.objects.create(
                        type=mobile_number["type"],
                        mobile_value=mobile_number["mobile_value"],
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False

    def update_business_card_faxs(self, faxs):
        """in this update_business_card_faxs method we
        update the business card fax details

        args: self
              faxs: [{"type": "home", "fax_value": "comss"}]

        return: True/False
        """
        # list_comprehension_update = [
        #     BusinessCardFax.objects.update_or_create(
        #         business_card_id=self.business_card_id,
        #         type=fax['type'],
        #         fax_value=fax['fax_value'],
        #         defaults={
        #             'type': fax['type'],
        #             'fax_value': fax['fax_value'],
        #         }
        #     ) for fax in faxs
        # ]
        # return True if list_comprehension_update else False

        for fax in faxs:
            business_card_create_instance = BusinessCardFax.objects.filter(
                business_card_id=self.business_card_id, id=fax.get("id", None)
            ).last()
            if business_card_create_instance:
                try:
                    BusinessCardFax.objects.filter(
                        id=fax.get("id", None)
                    ).update(
                        type=fax["type"], fax_value=fax["fax_value"]
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    BusinessCardFax.objects.create(
                        type=fax["type"], fax_value=fax["fax_value"]
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False

    def update_business_card_jobs(self, jobs):
        """in this update_business_card_jobs method we
        update the business card jobs details

        args: self
              mobile_numbers: [{"type": "facebook", "": "fb,comss"}]

        return: True/False
        """
        # list_comprehension_update = [
        #     BusinessCardJob.objects.update_or_create(
        #         business_card_id=self.business_card_id,
        #         type=job['type'],
        #         job_value=job['job_value'],
        #         defaults={
        #             'type': job['type'],
        #             'job_value': job['job_value'],
        #         }
        #     ) for job in jobs
        # ]
        # return True if list_comprehension_update else False

        for job in jobs:
            business_card_create_instance = BusinessCardJob.objects.filter(
                business_card_id=self.business_card_id, id=job.get("id", None)
            ).last()
            if business_card_create_instance:
                try:
                    BusinessCardJob.objects.filter(
                        id=job.get("id", None)
                    ).update(
                        type=job["type"], job_value=job["job_value"]
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    BusinessCardJob.objects.create(
                        type=job["type"], job_value=job["job_value"]
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False

    def update_business_card_dates(self, dates):
        """in this update_business_card_dates method we
        update the business card dates details

        args: self
              dates: [{"type": "facebook", "date": "33/22/3333"}]

        return: True/False
        """
        # list_comprehension_update = [
        #     BusinessCardDates.objects.update_or_create(
        #         business_card_id=self.business_card_id,
        #         type=date_value['type'],
        #         date=date_value['date'],
        #         defaults={
        #             'type': date_value['type'],
        #             'date': date_value['date'],
        #         }
        #     ) for date_value in dates
        # ]
        # return True if list_comprehension_update else False

        for date_value in dates:
            business_card_create_instance = BusinessCardDates.objects.filter(
                business_card_id=self.business_card_id,
                id=date_value.get("id", None)
            ).last()
            if business_card_create_instance:
                try:
                    BusinessCardDates.objects.filter(
                        id=date_value.get("id", None)
                    ).update(type=date_value["type"], date=date_value["date"])
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    BusinessCardDates.objects.create(
                        type=date_value["type"], date=date_value["date"]
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False

    def update_business_card_webs(self, webs):
        """in this update_business_card_faxs method we
        update the business card fax details

        args: self
              webs: [{"type": "home", "website": "suys.com"}]

        return: True/False
        """
        # list_comprehension_update = [
        #     BusinessCardWeb.objects.update_or_create(
        #         business_card_id=self.business_card_id,
        #         type=web['type'],
        #         website=web['website'],
        #         defaults={
        #             'type': web['type'],
        #             'website': web['website'],
        #         }
        #     ) for web in webs
        # ]
        # return True if list_comprehension_update else False

        for web in webs:
            business_card_create_instance = BusinessCardWeb.objects.filter(
                business_card_id=self.business_card_id, id=web.get("id", None)
            ).last()
            if business_card_create_instance:
                try:
                    BusinessCardWeb.objects.filter(
                        id=web.get("id", None)
                    ).update(
                        type=web["type"], website=web["website"]
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                try:
                    BusinessCardWeb.objects.create(
                        type=web["type"], website=web["website"]
                    )
                    return True
                except Exception as e:
                    print(e)
                    return False

    def update_business_card_notes(self, notes):
        """in this update_business_card_notes method we
        update the business card fax details

        args: self
              notes: [{"type": "home", "notes": "test"}]

        return: True/False
        """
        list_comprehension_update = [
            BusinessCardNotes.objects.update_or_create(
                business_card_id=self.business_card_id,
                type=note["type"],
                notes=note["notes"],
                defaults={
                    "type": note["type"],
                    "notes": note["notes"],
                },
            )
            for note in notes
        ]
        return True if list_comprehension_update else False

    def update_business_card_other_details(self):
        """this update_business_card_other_details
        method used to update all business related all details
        in this method we will call all mapping linkage models
        to update other details according to array request

        methods call as per request object;
        address: update_business_card_address;
        social_network:update_business_card_social_network;
        emails: update_business_card_emails;
        mobile_numbers: update_business_card_mobile_numbers;
        faxs: update_business_card_faxs;
        jobs: update_business_card_jobs;
        dates: update_business_card_dates;
        webs: update_business_card_webs;
        notes:update_business_card_notes;
        """
        if self.business_card_data.get("address", None):
            try:
                self.update_business_card_address(
                    self.business_card_data["address"]
                )
            except Exception as e:
                print("BusinessAddressErr")
                print(e)

        if self.business_card_data.get("social_network", None):
            try:
                self.update_business_card_social_network(
                    self.business_card_data["social_network"]
                )
            except Exception as e:
                print("BusinessSocialNetErr")
                print(e)

        if self.business_card_data.get("emails", None):
            try:
                self.update_business_card_emails(
                    self.business_card_data["emails"]
                )
            except Exception as e:
                print("BusinessCardEmailsErr")
                print(e)

        if self.business_card_data.get("mobile_numbers", None):
            try:
                self.update_business_card_mobile_numbers(
                    self.business_card_data["mobile_numbers"]
                )
            except Exception as e:
                print("BusinessSocialNetErr")
                print(e)

        if self.business_card_data.get("faxs", None):
            try:
                self.update_business_card_faxs(self.business_card_data["faxs"])
            except Exception as e:
                print("BusinessCardErr")
                print(e)

        if self.business_card_data.get("jobs", None):
            try:
                self.update_business_card_jobs(self.business_card_data["jobs"])
            except Exception as e:
                print("BusinessJobsErr")
                print(e)

        if self.business_card_data.get("dates", None):
            try:
                self.update_business_card_dates(
                    self.business_card_data["dates"]
                )
            except Exception as e:
                print("BusinessDatesErr")
                print(e)

        if self.business_card_data.get("webs", None):
            try:
                self.update_business_card_webs(self.business_card_data["webs"])
            except Exception as e:
                print("BusinessWebsErr")
                print(e)

        if self.business_card_data.get("notes", None):
            try:
                self.update_business_card_notes(
                    self.business_card_data["notes"]
                )
            except Exception as e:
                print("BusinessNotesErr")
                print(e)

    def update_business_card_detail(self):
        """this update_business_card_detail method used to update
        the business card detail
        """
        self.business_card_id = self.business_card_data.pop("id")
        self.get_business_card_instance()

        if not self.business_card_instance:
            return None

        # self.business_card_id = self.business_card_data.pop('id')
        business_card_serializer = BusinessCardReaderManagerSerializer(
            self.business_card_instance,
            data=self.business_card_data, partial=True
        )

        if business_card_serializer.is_valid(raise_exception=True):
            business_card_serializer.save()
            self.update_business_card_other_details()
            return business_card_serializer.data
        else:
            return None

    def category_group_user_value_list(self):
        """in this category_group_user_value_list method get
        the all user related category group list id
        """
        self._user_category_value_list = UserCategoryGroupMaster.objects.filter(
            user=self.auth_user_instance.user_auth
        ).values_list("category_group_id", flat=True)

    def category_group_list(self):
        """this category_group_list method used to get the
        all category group list from models
        """
        self.category_group_user_value_list()
        category_group_instance = self.category_group_entity
        user_category_group_instance = CategoryGroupMaster.objects.filter(
            is_active=True, id__in=self._user_category_value_list
        )
        if user_category_group_instance:
            category_group_instance = list(
                chain(category_group_instance, user_category_group_instance)
            )

        if not category_group_instance:
            return None

        try:
            category_group_master_data = CategoryGroupMastersSerializer(
                category_group_instance, many=True
            ).data

            category_group_master_data = [
                i
                for n, i in enumerate(category_group_master_data)
                if i not in category_group_master_data[n + 1 :]
            ]
            return category_group_master_data
        except Exception as e:
            print("CategoryGroupSerializerErr")
            print(e)
            return []

    def map_category_group_to_user(self, category_group_serializer_data):
        """in this map_category_group_to_user method we update
        category group name with the user

        args: self
              category_group_serializer_data: category group serializer data
              after valid serializer save data

        return: None
        """
        UserCategoryGroupMaster.objects.create(
            user_id=self.auth_user_instance.user_auth.id,
            category_group_id=category_group_serializer_data["id"],
        )

    def create_category_group(self):
        """this create_category_group method used to create
        the category group of cards
        """
        category_name = self.category_group_data["category_name"].title()
        category_name = " ".join(category_name.strip().split())

        if CategoryGroupMaster.objects.filter(
                category_name=category_name
        ).exists():
            return None

        self.category_group_data["category_name"] = category_name
        self.category_group_data["access_status"] = ACCESS_STATUS[1][0]
        self.category_group_data["color_hex_code"] = (
            self.category_group_data.get("color_hex_code", None)
            if self.category_group_data.get("color_hex_code", None)
            else "#368C89"
        )

        category_group_serializer = CategoryGroupMastersSerializer(
            data=self.category_group_data
        )
        if category_group_serializer.is_valid(raise_exception=True):
            category_group_serializer.save()
            try:
                self.map_category_group_to_user(category_group_serializer.data)
            except Exception as e:
                print("mapCategoryToUserErr")
                print(e)
            return category_group_serializer.data
        else:
            return None

    def upload_business_card(self):
        """this upload_business_card method used to upload
        the business card image in bcr db
        """
        self.card_data["retrive_status"] = "initiate"
        self.card_data["user"] = self.auth_user_instance.user_auth.id

        business_card_create = BusinessCardReaderManager.objects.create(
            business_image=self.card_data["business_image"],
            retrive_status="initiate",
            user_id=self.auth_user_instance.user_auth.id,
        )
        if not business_card_create:
            return None

        print("businessCardImage", self.card_data["business_image"])
        # print('businessCardImage', self.card_data['business_image'])

        try:
            print("card data", self.card_data)
            # image_data = business_card_create.business_image.open(mode='rb')
            # print('image_data', image_data)
            print("business images", self.card_data["business_image"])
            # print('read', self.card_data['business_image'].open(mode='rb'))

            _abby_ocr_obj = AbbyOcrReader(
                business_image=business_card_create.business_image.path,
                business_image_name=business_card_create.business_image.name,
                application_type=self.application_type,
                service_function=self.service_function,
                data_set_type=self.data_set_type,
                auth_user_instance=self.auth_user_instance,
                business_card_id=(business_card_create.id
                                  if business_card_create else
                                  None),
            )
            _abby_ocr_obj.upload_business_card()
            # start_new_thread(_abby_ocr_obj.upload_business_card, ())
        except Exception as e:
            ocr_result_data, ocr_result_message = None, str(e)
            print("AbbyOcrErr")
            print(e)
            return str(e)

        try:
            # update default category inbox
            BusinessCardReaderManager.objects.filter(
                id=business_card_create.id,
            ).update(category_group_id=get_category_group_id("inbox"))
        except Exception as e:
            print("DefaultCategoryErr")
            print(e)

        return {"business_image": str(business_card_create.business_image)}

    def test_file_upload(self):
        """
        this test_file_upload method upload the test file without token
        """
        print("cardData", self.card_data)
        create_file_obj = TestFilesUploadForRequest.objects.create(
            test_file=self.card_data["test_file"]
        )
        if create_file_obj:
            return create_file_obj.id
        else:
            return None

    def upload_image_local_for_testing_purpose(self):
        """this upload_business_card method used to upload
        the business card image in bcr db
        """
        user_instance = CustomUsers.objects.filter(is_active=True).last()
        business_card_create = BusinessCardReaderManager.objects.create(
            business_image=self.card_data["business_image"],
            retrive_status="initiate",
            user_id=user_instance.id,
        )
        if not business_card_create:
            return None

        try:
            print("card data", self.card_data)
            self.card_data[
                "business_image"
            ] = business_card_create.business_image.path
            api_response_status = AbbyOcrReader(
                business_image=self.card_data["business_image"],
            ).test_upload_file_local(self.card_data)
        except Exception as e:
            api_response_status = None
            print("AbbyLocalTestErr")
            print(e)

        if api_response_status:
            return True
        else:
            return False
