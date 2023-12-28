import uuid
# import django modules

from configuration.models import Language

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

from django.db import models

# import configuration modules
from configuration.models import CurrencyMaster

# import abstract modules
from core.models import ABSTRACTDateModel
from core.models import ABSTRACTStatusModel
from core.models import ABSTRACTCreateUpdateByModel


class CountryMaster(ABSTRACTDateModel,
                    ABSTRACTStatusModel,
                    ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    country = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )
    isd = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999),
                    MinValueValidator(1)],
        verbose_name='ISD/Country Code')
    mobile_no_digits = models.PositiveIntegerField(
        validators=[MaxValueValidator(15),
                    MinValueValidator(5)],
        null=True, blank=True,
        verbose_name='Mobile Number digit')
    currency = models.ForeignKey(
        CurrencyMaster, on_delete=models.CASCADE,
        related_name='currency_country_master',
        verbose_name='Currency',
        null=True, blank=True,
        limit_choices_to={'is_active': '1'})
    code = models.CharField(
        max_length=10,
        null=True, blank=True,
        verbose_name='ISO Code')
    timezone = models.CharField(
        max_length=100,
        help_text='Please add correct country timezone.',
        null=True, blank=True
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        verbose_name = "  Country Master"
        verbose_name_plural = "  Country Master"
        db_table = "country_master"

    def __str__(self):
        return self.country


class StateMaster(ABSTRACTDateModel,
                  ABSTRACTStatusModel,
                  ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    state = models.CharField(max_length=50, db_index=True)
    country = models.ForeignKey(
        CountryMaster,
        on_delete=models.CASCADE,
        db_column='country',
        limit_choices_to={'is_active': '1'})
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        verbose_name = " State Master"
        verbose_name_plural = " State Master"
        unique_together = ('country', 'state')
        db_table = "state_master"

    def __str__(self):
        return self.state


class CityMaster(ABSTRACTDateModel,
                 ABSTRACTStatusModel,
                 ABSTRACTCreateUpdateByModel):
    # for PK with UUID
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    city = models.CharField(max_length=50, db_index=True)
    state = models.ForeignKey(
        StateMaster,
        on_delete=models.CASCADE,
        verbose_name='State Name',
        db_column='state',
        limit_choices_to={'is_active': '1'})
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        verbose_name = "City Master"
        verbose_name_plural = "City Master"
        unique_together = ('state', 'city')
        db_table = "city_master"

    def __str__(self):
        return self.city
