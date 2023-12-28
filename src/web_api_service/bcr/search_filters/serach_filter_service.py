# import business card models
from django.db.models import Q

from cards.models import BusinessCardReaderManager

#  import serializers
from web_api_service.bcr.business_card_reader.business_card_serializers import (
    BusinessCardReaderManagerSerializer,
)


class BusinessCardSearchFilter:
    """
    BusinessCardReader
    """

    def __init__(self, **kwargs):
        self.business_card_instance = None
        self.auth_user_instance = kwargs.get("auth_user_instance", None)
        self.search_data = kwargs.get("business_card_search_data", None)
        self.filter_data = kwargs.get("business_card_filter_data", {})

    @staticmethod
    def business_card_data(business_card_reader_queryset):
        """this  business_card_data method used to collect serializers data"""
        try:
            return BusinessCardReaderManagerSerializer(
                business_card_reader_queryset, many=True
            ).data
        except Exception as e:
            print("ListSerializerErr")
            print(e)
            return None

    def business_card_search_list(self):
        """this business_card_list method used to get the
        all business card list from models
        """
        if self.search_data == "":
            business_card_reader_qs = BusinessCardReaderManager.objects.filter(
                user=self.auth_user_instance.user_auth, is_active=True
            ).order_by("-created_at")

        if self.search_data:
            business_card_reader_qs = BusinessCardReaderManager.objects.filter(
                user=self.auth_user_instance.user_auth,
                first_name__istartswith=self.search_data,
                is_active=True,
            ).order_by("-created_at")

        if not business_card_reader_qs:
            return None

        return self.business_card_data(business_card_reader_qs)

    def business_card_filter_list(self):
        """this business_card_filter_list method used to get
        the all business card filter data according to the request
        """
        business_card_reader_queryset = None
        business_card_reader_queryset = BusinessCardReaderManager.objects.filter(
            user=self.auth_user_instance.user_auth, is_active=True
        ).order_by("-created_at")

        if self.filter_data["sort_by"] and self.filter_data["category_group_id"]:
            try:
                business_card_reader_queryset = business_card_reader_queryset.filter(
                    ~Q(first_name=None)
                )
                if self.filter_data["sort_by"] == "asc":
                    business_card_reader_queryset = (
                        business_card_reader_queryset.order_by("first_name")
                    )
                if self.filter_data["sort_by"] == "dsc":
                    business_card_reader_queryset = (
                        business_card_reader_queryset.order_by("-first_name")
                    )

                business_card_reader_queryset = business_card_reader_queryset.filter(
                    category_group_id=self.filter_data["category_group_id"]
                )

            except Exception as e:
                business_card_reader_queryset = None
                print("CategoryAndSortByExceptionErr")
                print(e)

        if self.filter_data["sort_by"]:
            try:
                business_card_reader_queryset = business_card_reader_queryset.filter(
                    ~Q(first_name=None)
                )
                if self.filter_data["sort_by"] == "asc":
                    business_card_reader_queryset = (
                        business_card_reader_queryset.order_by("first_name")
                    )
                if self.filter_data["sort_by"] == "dsc":
                    business_card_reader_queryset = (
                        business_card_reader_queryset.order_by("-first_name")
                    )
            except Exception as e:
                business_card_reader_queryset = None
                print("SortByException")
                print(e)

        if self.filter_data["category_group_id"]:
            try:
                business_card_reader_queryset = business_card_reader_queryset.filter(
                    category_group_id=self.filter_data["category_group_id"]
                )
            except Exception as e:
                business_card_reader_queryset = None
                print("business_card_reader_queryset_exception")
                print(e)

        if (
            not self.filter_data["sort_by"]
            and not self.filter_data["category_group_id"]
        ):
            business_card_reader_queryset = business_card_reader_queryset

        if not business_card_reader_queryset:
            return None
        else:
            return self.business_card_data(business_card_reader_queryset)
