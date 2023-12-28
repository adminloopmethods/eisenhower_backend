"""core abstract level models for add all common tables 
"""
# from django.contrib.auth.models import User
from account.models import User

from django.db import models

# smart-select library
from smart_selects.db_fields import ChainedForeignKey


class ABSTRACTDateModel(models.Model):
    """
    created at and updated at fields
    abstract models
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class ABSTRACTStatusModel(models.Model):
    """
    is active status abstract model
    """
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class ABSTRACTCreateUpdateByModel(models.Model):
    """
    created updated by abstract model
    """
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='created_%(class)ss',
        verbose_name='Created By',
        limit_choices_to=~models.Q(is_staff=0, is_superuser=0),
        db_column='created_by',
        blank=True, null=True
    )

    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='updated_%(class)ss',
        verbose_name='Updated By',
        limit_choices_to=~models.Q(is_staff=0, is_superuser=0),
        db_column='updated_by',
        blank=True, null=True
    )

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class ABSTRACTLocationMaster(models.Model):
    """
    location master abstract model
    """
    country = models.ForeignKey(
        'location.CountryMaster',
        related_name='country_%(class)ss',
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': '1'},
        db_column='country',
        null=True, blank=True
    )
    state = ChainedForeignKey(
        'location.StateMaster',
        chained_field="country",
        chained_model_field="country",
        limit_choices_to={'is_active': '1'},
        related_name='state_%(class)ss',
        on_delete=models.CASCADE,
        show_all=True, auto_choose=True, sort=True,
        null=True, blank=True,
        db_column='state'
    )
    city = ChainedForeignKey(
        'location.CityMaster',
        chained_field='state',
        chained_model_field='state',
        limit_choices_to={'is_active': '1'},
        related_name='city_%(class)ss',
        on_delete=models.CASCADE,
        null=True, blank=True,
        show_all=True, auto_choose=True, sort=True,
        db_column='city'
    )

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True
