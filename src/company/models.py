"""company models for organigation maintain
"""
import uuid

from django.core.validators import FileExtensionValidator
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator

from django.db import models
from django.utils.safestring import mark_safe

# Third Party Module Imports
from smart_selects.db_fields import ChainedForeignKey

# module imports
from core.models import ABSTRACTDateModel
from core.models import ABSTRACTStatusModel
from core.models import ABSTRACTCreateUpdateByModel
from core.models import ABSTRACTLocationMaster

from core.messages import MODEL_MESSAGES


# Create your models here.


class Company(ABSTRACTLocationMaster,
              ABSTRACTDateModel,
              ABSTRACTStatusModel,
              ABSTRACTCreateUpdateByModel):
    """
    company details models for registration create for who owen this system
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    # regex for phone and e-mail
    zip_regex = RegexValidator(
        regex=r"^[a-zA-Z0-9]+$", message=MODEL_MESSAGES['ZIPCODEMSG']
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$", message=MODEL_MESSAGES['PHONENOMSG']
    )

    # company basic details
    company_name = models.CharField(max_length=50, unique=True)
    business_nature = models.CharField(max_length=100)
    address = models.TextField()
    zip_code = models.CharField(
        validators=[zip_regex, MinLengthValidator(3)],
        max_length=6,
    )
    owner_name = models.CharField(max_length=50, null=True)
    owner_email_id = models.EmailField(unique=True)
    owner_mobile_no = models.CharField(validators=[phone_regex], max_length=15)
    company_logo = models.FileField(
        upload_to="company_logo",
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])],
    )
    company_contact_no = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        verbose_name="company Mobile No.",
    )
    company_email_id = models.EmailField(unique=True)
    company_registration_no = models.CharField(max_length=200)
    website = models.URLField(max_length=250, blank=True, null=True)
    currency = models.ForeignKey(
        "configuration.CurrencyMaster",
        related_name="company_currency",
        on_delete=models.CASCADE,
        verbose_name="Currency",
        limit_choices_to={"is_active": "1"},
    )

    # contact support details
    contact_person = models.CharField(
        max_length=100, verbose_name="Support Person Name"
    )
    contact_person_mobile_no = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        verbose_name="Support Mobile No.",
    )
    contact_person_email_id = models.EmailField(
        unique=True, verbose_name="Support Email ID"
    )

    # Billings details with address
    billing_address = models.CharField(max_length=100, null=True, blank=True)
    billing_country = models.ForeignKey(
        "location.CountryMaster",
        related_name="billing_country",
        on_delete=models.CASCADE,
        db_column="billing_country",
        null=True, blank=True,
        limit_choices_to={"is_active": "1"},
    )
    billing_state = ChainedForeignKey(
        "location.StateMaster",
        chained_field="billing_country",
        chained_model_field="country",
        db_column="billing_state",
        related_name="billing_state",
        on_delete=models.CASCADE,
        null=True, blank=True, show_all=True,
        auto_choose=True, sort=True,
        limit_choices_to={"is_active": "1"},
    )
    billing_city = ChainedForeignKey(
        "location.CityMaster",
        chained_field="billing_state",
        chained_model_field="state",
        related_name="billing_city",
        on_delete=models.CASCADE,
        db_column="billing_city",
        null=True, blank=True, show_all=True,
        auto_choose=True, sort=True,
        limit_choices_to={"is_active": "1"},
    )
    billing_currency = models.ForeignKey(
        "configuration.CurrencyMaster",
        related_name="billing_currency",
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': "1"},
        blank=True, null=True,
    )

    class Meta:
        verbose_name = " Company Master"
        verbose_name_plural = " Company Master"
        db_table = "company_master"

    def __str__(self):
        return self.company_name
