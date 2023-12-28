from datetime import datetime

from cards.models import BusinessCardAddress, BusinessExpenseManager
from cards.models import BusinessCardDates
from cards.models import BusinessCardEmail
from cards.models import BusinessCardFax
from cards.models import BusinessCardJob
from cards.models import BusinessCardMobile
from cards.models import BusinessCardReaderManager
from cards.models import BusinessCardSocialNetwork
from cards.models import BusinessCardWeb
# import business card models
from cards.models import CategoryGroupMaster
from core.constants import MOBILE_TYPE
from web_api_service.bcr.abby_apis.abby_ocr_services import AbbyOcrReader
# import custom user
from web_api_service.bcr.business_card_reader.business_card_serializers import (
    BusinessCardReaderManagerSerializer,
)


class UpdateBusinessCardDetails:
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

        self._user_category_value_list = []

        # initiate the categoryGroupMaster Models
        self.category_group_entity = CategoryGroupMaster.objects.filter(
            is_active=True
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
                is_active=True
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

    def get_business_card_instance(self):
        """this get_business_card_instance method used to
        get the business card instance
        """
        try:
            self.business_card_instance = BusinessCardReaderManager.objects.get(
                user_id=self.auth_user_instance.user_auth.id,
                id=self.business_card_id,
                is_active=True
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

    def update_business_card_address(self, address_data):
        """in this update_business_card_address method we
        update the business card address details
        return: None
        """
        try:
            BusinessCardAddress.objects.filter(
                business_card_id=self.business_card_id
            ).delete()
        except Exception as e:
            print(e)
        for address in address_data:
            try:
                if address["type"] and address["country"]:
                    BusinessCardAddress.objects.create(
                        business_card_id=self.business_card_id,
                        type=address.get('type', None),
                        street=address.get('street', None),
                        city=address.get('city', None),
                        region=address.get('region', None),
                        country=address.get('country', None),
                        zip_code=address.get('zip_code', None)
                    )
            except Exception as e:
                print("AddressCardErr")
                print(e)

    def update_business_card_social_network(self, social_network_data):
        """in this update_business_card_social_network method we
        update the business card address details

        args: self
              social_network_data: [{"type": "facebook",
                                     "social_network_value": "fb,comss"}]

        return: True/False
        """
        try:
            BusinessCardSocialNetwork.objects.filter(
                business_card_id=self.business_card_id
            ).delete()
        except Exception as e:
            print(e)
        for social_network in social_network_data:
            try:
                if (social_network["type"]
                        and social_network["social_network_value"]):
                    BusinessCardSocialNetwork.objects.create(
                        business_card_id=self.business_card_id,
                        type=social_network["type"],
                        social_network_value=social_network[
                            "social_network_value"
                        ]
                    )
            except Exception as e:
                print(e)

    def update_business_card_emails(self, emails_data):
        """in this update_business_card_emails method we
        update the business card emails details
        args: self: emails_data: "emails": [
        {"type": "home", "email_value": "gousha@gmail.com"}
        ],
        return: True/False
        """
        try:
            BusinessCardEmail.objects.filter(
                business_card_id=self.business_card_id
            ).delete()
        except Exception as e:
            print(e)
        for emails in emails_data:
            try:
                if emails["type"] and emails["email_value"]:
                    BusinessCardEmail.objects.create(
                        business_card_id=self.business_card_id,
                        type=emails["type"],
                        email_value=emails["email_value"],
                    )
            except Exception as e:
                print(e)

    def update_business_card_mobile_numbers(self, mobile_numbers):
        """in this update_business_card_mobile_numbers method we
        update the business card mobile numbers details

        args: self
              mobile_numbers: [{"type": "home", "mobile_value": "88989898978"}]

        return: True/False
        """
        try:
            BusinessCardMobile.objects.filter(
                business_card_id=self.business_card_id
            ).delete()
        except Exception as e:
            print(e)
        for mobile_number in mobile_numbers:
            try:
                if mobile_number["type"] and mobile_number["mobile_value"]:
                    BusinessCardMobile.objects.create(
                        business_card_id=self.business_card_id,
                        type=mobile_number["type"],
                        mobile_value=mobile_number["mobile_value"],
                    )
            except Exception as e:
                print(e)

    def update_business_card_faxs(self, faxs):
        """in this update_business_card_faxs method we
        update the business card fax details

        args: self
              faxs: [{"type": "home", "fax_value": "comss"}]

        return: True/False
        """
        try:
            BusinessCardFax.objects.filter(
                business_card_id=self.business_card_id
            ).delete()
        except Exception as e:
            print(e)
        for fax in faxs:
            try:
                if fax["type"] and fax["fax_value"]:
                    BusinessCardFax.objects.create(
                        business_card_id=self.business_card_id,
                        type=fax["type"],
                        fax_value=fax["fax_value"],
                    )
            except Exception as e:
                print(e)

    def get_business_card_obj(self, job_type):
        """get_business_card_obj object fields provide business card job in stance"""
        try:
            return BusinessCardJob.objects.get(
                business_card_id=self.business_card_id,
                type=job_type
            )
        except Exception as e:
            print(e)
            print("businessCardJobExpErr")
            return None

    def update_business_card_jobs(self, jobs):
        """in this update_business_card_jobs method we
        update the business card jobs details

        args: self
              mobile_numbers: [{"type": "facebook", "": "fb,comss"}]

        return: True/False
        """
        try:
            BusinessCardJob.objects.filter(
                business_card_id=self.business_card_id
            ).delete()
        except Exception as e:
            print('deleteExpForJobExp')
            print(e)

        try:
            BusinessCardReaderManager.objects.filter(
                id=self.business_card_id).update(company_name=None)
        except Exception as e:
            print('updateBusinessExpErr')
            print(e)

        for job in jobs:
            try:
                if job["type"] and job["job_value"]:
                    if job["type"] == "company":
                        try:
                            BusinessCardReaderManager.objects.filter(
                                id=self.business_card_id
                            ).update(company_name=job["job_value"])
                        except Exception as e:
                            print("BusinessCardReaderManagerErr")
                            print(e)
                        business_card_obj = self.get_business_card_obj(
                            job["type"]
                        )
                        if business_card_obj:
                            BusinessCardJob.objects.filter(
                                type=job["type"],
                                id=business_card_obj.id
                            ).update(job_value=job["job_value"])
                        else:
                            try:
                                BusinessCardJob.objects.create(
                                    business_card_id=self.business_card_id,
                                    type=job["type"],
                                    job_value=job["job_value"],
                                )
                                BusinessCardJob.objects.create(
                                    business_card_id=self.business_card_id,
                                    type="position",
                                    job_value=None,
                                )
                                BusinessCardJob.objects.create(
                                    business_card_id=self.business_card_id,
                                    type="department",
                                    job_value=None,
                                )
                            except Exception as e:
                                print('updateCodeCompanyType')
                                print(e)

                    if job["type"] == "position":
                        business_card_obj = self.get_business_card_obj(
                            job["type"]
                        )
                        if business_card_obj:
                            BusinessCardJob.objects.filter(
                                type=job["type"],
                                id=business_card_obj.id
                            ).update(job_value=job["job_value"])
                        else:
                            BusinessCardJob.objects.create(
                                business_card_id=self.business_card_id,
                                type=job["type"],
                                job_value=job["job_value"],
                            )
                            BusinessCardJob.objects.create(
                                business_card_id=self.business_card_id,
                                type="company",
                                job_value=None,
                            )
                            BusinessCardJob.objects.create(
                                business_card_id=self.business_card_id,
                                type="department",
                                job_value=None,
                            )

                    if job["type"] == "department":
                        business_card_obj = self.get_business_card_obj(
                            job["type"]
                        )
                        if business_card_obj:
                            BusinessCardJob.objects.filter(
                                type=job["type"],
                                id=business_card_obj.id
                            ).update(job_value=job["job_value"])
                        else:
                            BusinessCardJob.objects.create(
                                business_card_id=self.business_card_id,
                                type=job["type"],
                                job_value=job["job_value"],
                            )
                            BusinessCardJob.objects.create(
                                business_card_id=self.business_card_id,
                                type="company",
                                job_value=None,
                            )
                            BusinessCardJob.objects.create(
                                business_card_id=self.business_card_id,
                                type="position",
                                job_value=None,
                            )
            except Exception as e:
                print('jobUpdateExceptionErr')
                print(e)

    def update_business_card_dates(self, dates):
        """in this update_business_card_dates method we
        update the business card dates details

        args: self
              dates: [{"type": "facebook", "date": "33/22/3333"}]

        return: True/False
        """
        try:
            BusinessCardDates.objects.filter(
                business_card_id=self.business_card_id
            ).delete()
        except Exception as e:
            print(e)
        for date_value in dates:
            try:
                if date_value["type"] and date_value["date"]:
                    BusinessCardDates.objects.create(
                        business_card_id=self.business_card_id,
                        type=date_value["type"],
                        date=date_value["date"],
                    )
            except Exception as e:
                print(e)

    def update_business_card_webs(self, webs):
        """in this update_business_card_faxs method we
        update the business card fax details

        args: self
              webs: [{"type": "home", "website": "suys.com"}]

        return: True/False
        """
        try:
            BusinessCardWeb.objects.filter(
                business_card_id=self.business_card_id
            ).delete()
        except Exception as e:
            print(e)
        for web in webs:
            try:
                if web["type"] and web["website"]:
                    BusinessCardWeb.objects.create(
                        business_card_id=self.business_card_id,
                        type=web["type"],
                        website=web["website"],
                    )
            except Exception as e:
                print(e)

    def update_business_card_other_details(self):
        """this update_business_card_other_details method used to update all
        business related all details
        in this method we will call all mapping
        linkage models to update other details according to array request
        """
        try:
            self.update_business_card_address(
                self.business_card_data.get("address", None)
            )
        except Exception as e:
            print("BusinessAddressErr")
            print(e)

        try:
            self.update_business_card_social_network(
                self.business_card_data.get("social_network", None)
            )
        except Exception as e:
            print("BusinessSocialNetErr")
            print(e)

        try:
            self.update_business_card_emails(
                self.business_card_data.get("emails", None)
            )
        except Exception as e:
            print("BusinessCardEmailsErr")
            print(e)

        try:
            self.update_business_card_mobile_numbers(
                self.business_card_data.get("mobile_numbers", None)
            )
        except Exception as e:
            print("BusinessSocialNetErr")
            print(e)

        try:
            self.update_business_card_faxs(
                self.business_card_data.get("faxs", None)
            )
        except Exception as e:
            print("BusinessCardErr")
            print(e)

        try:
            self.update_business_card_jobs(
                self.business_card_data.get("jobs", None)
            )
        except Exception as e:
            print("BusinessJobsErr")
            print(e)

        try:
            self.update_business_card_dates(
                self.business_card_data.get("dates", None)
            )
        except Exception as e:
            print("BusinessDatesErr")
            print(e)

        try:
            self.update_business_card_webs(
                self.business_card_data.get("webs", None)
            )
        except Exception as e:
            print("BusinessWebsErr")
            print(e)

    def update_business_card_detail(self):
        """this update_business_card_detail method used to update
        the business card detail
        """
        self.business_card_id = self.business_card_data.pop("id")
        self.get_business_card_instance()

        if not self.business_card_instance:
            return None

        print('request_data:   ', self.business_card_data)
        # self.business_card_id = self.business_card_data.pop('id')
        # try:
        #     print('jjjjjjjjjjjjjjjjjj', self.business_card_data['jobs'])
        #     for job_data in list(self.business_card_data['jobs']):
        #         if str(job_data['type']) == 'company':
        #             print('jobvalud', job_data.get('job_value'))
        #             self.business_card_data['company_name'] = job_data.get('job_value', None)
        #         else:
        #             self.business_card_data['company_name'] = None
        # except Exception as e:
        #     print('CompanyUpdateExpErr')
        #     print(e)
        self.business_card_data["is_card_retrived"] = True

        print('request_data_seconds:   ', self.business_card_data)
        try:
            self.business_card_data[
                'first_name'
            ] = self.business_card_data['first_name'].title()
        except Exception as e:
            print('e')

        print('--------------data', self.business_card_data)

        business_card_serializer = BusinessCardReaderManagerSerializer(
            self.business_card_instance, data=self.business_card_data,
            partial=True
        )
        if business_card_serializer.is_valid(raise_exception=True):
            business_card_serializer.save()
            self.update_business_card_other_details()
            return business_card_serializer.data
        else:
            return None

    @staticmethod
    def update_business_card_details_from_abby_response(
            business_card_id, business_card_data
    ):
        """
        update_business_card_details_from_abby_response
        this update_business_card_details_from_abby_response called the abby response retrive
        status and update values
        """
        try:
            BusinessCardReaderManager.objects.filter(
                id=business_card_id
            ).update(**business_card_data)
        except Exception as e:
            print("BusinessCardReaderManagerExceptionErr")
            print(e)

        if business_card_data.get('e_mail'):
            try:
                BusinessCardEmail.objects.filter(
                    business_card_id=business_card_id
                ).delete()
            except Exception as e:
                print(e)
            try:
                BusinessCardEmail.objects.create(
                    business_card_id=business_card_id,
                    type='work',
                    email_value=business_card_data.get('e_mail', None),
                )
                # BusinessCardEmail.objects.create(
                #     business_card_id=business_card_id,
                #     type='home',
                #     email_value=business_card_data.get('e_mail', None),
                # )
            except Exception as e:
                print(e)

        try:
            BusinessCardMobile.objects.filter(
                business_card_id=business_card_id
            ).delete()
        except Exception as e:
            print(e)

        try:
            if "telephone_office" in business_card_data.keys():
                if business_card_data["telephone_office"]:
                    mobile_type = MOBILE_TYPE[0][1]  # works
                    mobile_number = business_card_data["telephone_office"]
                    BusinessCardMobile.objects.create(
                        business_card_id=business_card_id,
                        type=mobile_type,
                        mobile_value=mobile_number,
                    )

            if "telephone_mobile" in business_card_data.keys():
                if business_card_data["telephone_mobile"]:
                    mobile_type = MOBILE_TYPE[2][1]  # other
                    mobile_number = business_card_data["telephone_mobile"]
                    BusinessCardMobile.objects.create(
                        business_card_id=business_card_id,
                        type=mobile_type,
                        mobile_value=mobile_number,
                    )

            if "telephone_home" in business_card_data.keys():
                if business_card_data["telephone_home"]:
                    mobile_type = MOBILE_TYPE[1][1]  # home
                    mobile_number = business_card_data["telephone_home"]
                    BusinessCardMobile.objects.create(
                        business_card_id=business_card_id,
                        type=mobile_type,
                        mobile_value=mobile_number,
                    )
        except Exception as e:
            print(e)
        if business_card_data["fax"]:
            try:
                BusinessCardFax.objects.filter(
                    business_card_id=business_card_id
                ).delete()
            except Exception as e:
                print(e)
            try:
                BusinessCardFax.objects.create(
                    business_card_id=business_card_id,
                    type="work",
                    fax_value=business_card_data["fax"],
                )
            except Exception as e:
                print("BusinessCardFaxExceptionErr")
                print(e)

        if business_card_data["web"]:
            try:
                BusinessCardWeb.objects.filter(
                    business_card_id=business_card_id
                ).delete()
            except Exception as e:
                print(e)
            try:
                BusinessCardWeb.objects.create(
                    business_card_id=business_card_id,
                    type="work",
                    website=business_card_data["web"],
                )
            except Exception as e:
                print("BusinessCardFaxExceptionErr")
                print(e)

        if business_card_data.get("facebook"):
            try:
                BusinessCardSocialNetwork.objects.filter(
                    business_card_id=business_card_id
                ).delete()
            except Exception as e:
                print(e)
            try:
                BusinessCardSocialNetwork.objects.create(
                    business_card_id=business_card_id,
                    type="facebook",
                    social_network_value=business_card_data.get(
                        "facebook", "www.info-doc.it"
                    ),
                )
            except Exception as e:
                print("BusinessCardFaxExceptionErr")
                print(e)

        if (
                business_card_data["country"]
                or business_card_data["street"]
                or business_card_data["city"]
                or business_card_data["province"]
                or business_card_data["postal_code"]
        ):
            try:
                BusinessCardAddress.objects.filter(
                    business_card_id=business_card_id
                ).delete()
            except Exception as e:
                print(e)
            try:
                BusinessCardAddress.objects.create(
                    business_card_id=business_card_id,
                    type="company",
                    street=business_card_data["street"],
                    city=business_card_data["city"],
                    region=business_card_data["province"],
                    country=business_card_data["country"],
                    zip_code=business_card_data["postal_code"],
                )
            except Exception as e:
                print("AddressCardErr")
                print(e)

        try:
            BusinessCardReaderManager.objects.filter(
                id=business_card_id).update(is_card_retrived=True,
                                            retrive_status="retrive")
        except Exception as e:
            print("BusinessCardReaderManagerUpdateExpr")
            print(e)

        try:
            BusinessCardJob.objects.filter(
                business_card_id=business_card_id
            ).delete()
        except Exception as e:
            print(e)
        try:
            BusinessCardJob.objects.create(
                business_card_id=business_card_id,
                type="company",
                job_value=business_card_data["company_name"],
            )
            BusinessCardJob.objects.create(
                business_card_id=business_card_id,
                type="position",
                job_value=business_card_data.get("title", None)
            )
            BusinessCardJob.objects.create(
                business_card_id=business_card_id,
                type="department",
                job_value=None
            )
        except Exception as e:
            print(e)

    def business_card_update_by_abby_response_old(self, business_card_queryset):
        """this business_card_update_by_abby_response method used to update 
        the abby response
        """
        for business_card_read in business_card_queryset:
            abby_status_data, abby_response_msg = AbbyOcrReader(
                abby_response_id=business_card_read.abby_response_id,
                auth_user_instance=self.auth_user_instance,
            ).abby_retrieve_call()
            if abby_status_data:
                business_card_data = {
                    "prefix": abby_status_data["suffix"],
                    "nick_name": None,
                    "title": abby_status_data["title"],
                    "first_name": abby_status_data["first_name"],
                    "second_name": abby_status_data["second_name"],
                    "last_name": abby_status_data["last_name"],
                    "suffix": abby_status_data["suffix"],
                    "company_name": abby_status_data["company_name"],
                    # mobile numbers arrays
                    "telephone_office": abby_status_data["telephone_office"],
                    "telephone_mobile": abby_status_data["telephone_mobile"],
                    "telephone_home": abby_status_data["telephone_home"],
                    # fax array
                    "fax": abby_status_data["fax"],
                    # website
                    "web": abby_status_data["web"],
                    # social network array
                    "facebook": abby_status_data["facebook"],
                    # address array
                    "country": abby_status_data["country"],
                    "province": abby_status_data["province"],
                    "city": abby_status_data["city"],
                    "street": abby_status_data["street"],
                    "postal_code": abby_status_data["postal_code"],
                }
                self.update_business_card_details_from_abby_response(
                    business_card_read.id,
                    business_card_data)

    def business_card_update_by_abby_response(self):
        """this business_card_update_by_abby_response method used to update
        the abby response.
        business_card_queryset: this query set help to manage the our BCR models 
        instance update, add, delete, and get the BCr card details
        new_abby_bcm_response: {
            "lastName": null,
            "country": null,
            "city": null,
            "telephoneMobile": null,
            "companyName": null,
            "postalCode": null,
            "facebook": null,
            "title": null,
            "telephoneOffice": null,
            "eMail": null,
            "firstName": null,
            "province": null,
            "web": null,
            "street": null,
            "nomeBatch": "e99b5f96-de02-4bbe-971d-7fe1d43bf61f",
            "fax": null
        }
        """
        business_card_reader_qs = BusinessCardReaderManager.objects.filter(
            user=self.auth_user_instance.user_auth,
            is_card_retrived=False,
            retrive_status="initiate",
            is_active=True
        )
        for business_card_read in business_card_reader_qs:
            abby_status_data, abby_response_msg = AbbyOcrReader(
                abby_response_id=business_card_read.abby_response_id,
                auth_user_instance=self.auth_user_instance,
            ).abby_retrieve_call()

            try:
                business_card_instance = BusinessCardReaderManager.objects.get(
                    id=business_card_read.id
                )
            except Exception as e:
                business_card_instance = None
                print('Exp')
                print(e)

            if abby_status_data == 425:
                try:
                    if business_card_instance:
                        count_failed_number = (
                            int(business_card_instance.failed_count)
                            if business_card_instance.failed_count else
                            None
                        )
                        if count_failed_number:
                            count_failed_number += 1
                        else:
                            count_failed_number = 1
                    BusinessCardReaderManager.objects.filter(
                        id=business_card_read.id
                    ).update(failed_count=count_failed_number)
                except Exception as e:
                    print("AbbyFailedBusinessCardReaderManagerErr")
                    print(e)

            try:
                if int(business_card_instance.failed_count):
                    if int(business_card_instance.failed_count) >= 65:
                        BusinessCardReaderManager.objects.filter(
                            id=business_card_read.id
                        ).update(retrive_status='discard')
            except Exception as e:
                print("retrivStatusBusinessCardReaderManagerErr")
                print(e)

            if abby_status_data:
                business_card_data = {
                    "nick_name": None,
                    "title": abby_status_data.get("title", None),
                    "first_name": abby_status_data.get("firstName", None),
                    "second_name": abby_status_data.get("middleName", None),
                    "last_name": abby_status_data.get("lastName", None),
                    "company_name": abby_status_data.get("companyName", None),
                    "e_mail": abby_status_data.get("eMail", None),
                    # mobile numbers arrays
                    "telephone_office": abby_status_data.get(
                        "telephoneOffice", None
                    ),
                    "telephone_mobile": abby_status_data.get(
                        "telephoneMobile", None
                    ),
                    # fax array
                    "fax": abby_status_data.get("fax", None),
                    # website
                    "web": abby_status_data.get("web", None),
                    # social network array
                    "facebook": abby_status_data.get("facebook", None),
                    # address array
                    "country": abby_status_data.get("country", None),
                    "province": abby_status_data.get("province", None),
                    "city": abby_status_data.get("city", None),
                    "street": abby_status_data.get("street", None),
                    "postal_code": abby_status_data.get("postalCode", None),
                }
                self.update_business_card_details_from_abby_response(
                    business_card_read.id,
                    business_card_data)

    @staticmethod
    def update_business_expense_details_from_abby_response(
            business_expense_id,
            business_expense_data):
        """
        :param business_expense_id: for  update expense qs
        :param business_expense_data: abby response data in input format
        :return: True/False
        """
        try:
            BusinessExpenseManager.objects.filter(
                id=business_expense_id
            ).update(
                merchant_name=business_expense_data['merchant_name'],
                purchased_on=business_expense_data['purchased_on'],
                amount=business_expense_data['amount'],
                expense_process_status='drafted',
                is_card_retrived=True,
                retrive_status='retrive',
                # expense_type=id
            )
        except Exception as e:
            print('BusinessExpenseManagerUpdateErr')
            print(e)

    def business_expense_update_by_abby_response(
            self, business_expense_queryset
    ):
        """this business_expense_update_by_abby_response method used to update 
        the abby response, 
        business_card_queryset---this query set help to manage 
        the our BEM models instance update, add, delete, and get 
        the BCr card details
        new_abby_bem_response--- {
            "date": "08/11/2022",
            "amount": null,
            "address": "PIAZZALE G. FOR",
            "province": " NO",
            "city": "NOVARA",
            "vat_number": null,
            "company_name": "1 UMIDA S R I",
            "post_code": "28100",
            "doc_number": "N:",
            "nomeBatch": "681e8dfc-ea67-4fc5-b31c-34721e774201",
            "time": "20:35"
        }
        response: {
            "date": "08/11/22",
            "amount": "16.00",
            "address": "CORSO DELLA VITTORIA 2/0",
            "province": null,
            "city": "NOVARA",
            "vat_number": "02666680034",
            "company_name": null,
            "post_code": "28100",
            "doc_number": "0658 0097",
            "nomeBatch": "ebab3bbe-97e1-468c-9ead-735b6e7eabba",
            "time": "20:19"
        }
        """
        for business_expense_read in business_expense_queryset:
            abby_status_data, abby_response_msg = AbbyOcrReader(
                abby_response_id=business_expense_read.abby_response_id,
                auth_user_instance=self.auth_user_instance,
            ).abby_retrieve_call()

            try:
                business_card_instance = BusinessExpenseManager.objects.get(
                    id=business_expense_read.id
                )
            except Exception as e:
                business_card_instance = None
                print('Exp')
                print(e)

            try:
                if len(abby_status_data) == 0:
                    try:
                        if business_card_instance:
                            count_failed_number = (
                                int(business_card_instance.failed_count)
                                if business_card_instance.failed_count else
                                None
                            )
                            if count_failed_number:
                                count_failed_number += 1
                            else:
                                count_failed_number = 1
                        BusinessExpenseManager.objects.filter(
                            id=business_expense_read.id
                        ).update(failed_count=count_failed_number)
                    except Exception as e:
                        print("AbbyFailedBusinessCardReaderManagerErr")
                        print(e)
            except Exception as e:
                print(e)

            try:
                if abby_status_data == 425:
                    try:
                        if business_card_instance:
                            count_failed_number = (
                                int(business_card_instance.failed_count)
                                if business_card_instance.failed_count else
                                None
                            )
                            if count_failed_number:
                                count_failed_number += 1
                            else:
                                count_failed_number = 1
                        BusinessExpenseManager.objects.filter(
                            id=business_expense_read.id
                        ).update(failed_count=count_failed_number)
                    except Exception as e:
                        print("AbbyFailedBusinessCardReaderManagerErr")
                        print(e)
            except Exception as e:
                print(e)

            try:
                if int(business_card_instance.failed_count):
                    if int(business_card_instance.failed_count) >= 30:
                        BusinessExpenseManager.objects.filter(
                            id=business_expense_read.id
                        ).update(retrive_status='failed')
            except Exception as e:
                print("retrivStatusBusinessCardReaderManagerErr")
                print(e)

            if abby_status_data or len(abby_status_data) > 0:
                try:
                    purchased_on = datetime.strptime(
                        str(abby_status_data.get('date', None)),
                        '%d/%m/%y'
                    )
                except Exception as e:
                    print('datePick')
                    print(e)
                    try:
                        purchased_on = datetime.strptime(
                            str(abby_status_data.get('date', None)),
                            '%d/%m/%Y'
                        )
                    except Exception as e:
                        print('purchasedErr')
                        print(e)
                        try:
                            purchased_on = None
                        except Exception as e:
                            print('purchasedErr')
                            print(e)
                business_expense_data = {
                    "purchased_on": purchased_on if purchased_on else None,
                    "amount": (
                        abby_status_data.get('amount')
                        if abby_status_data.get('amount', None) else
                        None
                    ),
                    "merchant_name": (
                        abby_status_data.get('company_name')
                        if abby_status_data.get('company_name', None) else
                        None
                    ),
                }
                self.update_business_expense_details_from_abby_response(
                    business_expense_read.id,
                    business_expense_data
                )
