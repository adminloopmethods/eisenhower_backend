import uuid

from django.db import models

from configuration.models import ExpenseTypeMaster
from core.constants import ACCESS_STATUS
from core.constants import ADDRESS_TYPE
from core.constants import DATE_BIRTH_TYPE
from core.constants import EMAIL_TYPE
# import constant
from core.constants import EXPENSE_TYPE_DATA
from core.constants import FAX_TYPE
from core.constants import JOB_TYPE
from core.constants import MOBILE_TYPE
from core.constants import NOTES_TYPE
from core.constants import REIMBURSEMENT_STATUS_DATA
# import constance
from core.constants import RETRIVE_STATUS_DATA
from core.constants import SOCIAL_NETWORK_TYPE
from core.constants import WEBSITE_TYPE
from core.models import ABSTRACTCreateUpdateByModel
# import abstract modules
from core.models import ABSTRACTDateModel
from core.models import ABSTRACTStatusModel
# import user models
from user.models import CustomUsers


# import django modules
# Create your models here.


class CategoryGroupMaster(ABSTRACTDateModel,
                          ABSTRACTStatusModel,
                          ABSTRACTCreateUpdateByModel):
    """
    CategoryGroupMaster
    """
    # uuid
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    category_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    color_hex_code = models.CharField(max_length=20, null=True, blank=True)
    access_status = models.CharField(
        max_length=100,
        choices=ACCESS_STATUS)

    class Meta:
        verbose_name = 'Category Group Master'
        verbose_name_plural = 'Category Group Master'
        db_table = 'category_group_master'

    def __str__(self):
        return str(self.category_name)


class UserCategoryGroupMaster(ABSTRACTDateModel,
                              ABSTRACTStatusModel,
                              ABSTRACTCreateUpdateByModel):
    """
    CategoryGroupMaster
    """
    # uuid
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    user = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='user_group_category')
    category_group = models.ForeignKey(CategoryGroupMaster,
                                       on_delete=models.CASCADE,
                                       related_name='card_group_master_user')

    class Meta:
        verbose_name = 'User Category Group Master'
        verbose_name_plural = 'User Category Group Master'
        db_table = 'user_category_group_master'

    def __str__(self):
        return str(self.category_group)


class BusinessCardReaderManager(ABSTRACTDateModel,
                                ABSTRACTStatusModel,
                                ABSTRACTCreateUpdateByModel):
    """
    CardManager models
    """
    # uuid
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    # image media file
    business_image = models.ImageField(
        upload_to='business_card_images/',
        verbose_name='Business Card Images',
    )
    # abby screen attributes
    # for name attr
    prefix = models.CharField(max_length=255, null=True, blank=True)
    nick_name = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    email_work = models.CharField(max_length=255, null=True, blank=True)
    email_personal = models.CharField(max_length=255, null=True, blank=True)
    contact_number_personal = models.CharField(
        max_length=255, null=True, blank=True)
    contact_number_work = models.CharField(
        max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    address_type = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)

    # all api response attr refr from abby
    title = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    suffix = models.CharField(max_length=255, null=True, blank=True)

    # company and department attributes
    company_name = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)

    telephone_office = models.CharField(max_length=255, null=True, blank=True)
    telephone_mobile = models.CharField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=255, null=True, blank=True)
    telephone_home = models.CharField(max_length=255, null=True, blank=True)
    e_mail = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    failed_count = models.CharField(max_length=255, null=True, blank=True)

    notes = models.TextField(null=True, blank=True)

    # manipulate the card reader data
    category_group = models.ForeignKey(CategoryGroupMaster,
                                       on_delete=models.CASCADE,
                                       related_name='card_group_master',
                                       null=True, blank=True)

    # manage the flag to handle abby services
    is_card_retrived = models.BooleanField(default=False)
    retrive_status = models.CharField(max_length=255, choices=RETRIVE_STATUS_DATA)
    is_editable = models.BooleanField(default=False)
    reason_for_failed = models.CharField(max_length=255, null=True, blank=True)
    abby_response_id = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='user_business_card')

    class Meta:
        verbose_name = 'Card Reader Manager'
        verbose_name_plural = 'Card Reader Manager'
        db_table = 'business_card_reader_manager'

    def __str__(self):
        return str(self.id)


class BusinessCardSocialLink(ABSTRACTDateModel,
                             ABSTRACTStatusModel,
                             ABSTRACTCreateUpdateByModel):
    """
    card social link
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master')
    social_link = models.CharField(max_length=255, null=True, blank=True)
    social_link_url = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card Social Link'
        verbose_name_plural = 'Business Card Social Link'
        db_table = 'business_card_social_link'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardFax(ABSTRACTDateModel,
                      ABSTRACTStatusModel,
                      ABSTRACTCreateUpdateByModel):
    """
    BusinessCardFax
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_fax')
    type = models.CharField(max_length=255, choices=FAX_TYPE)
    fax_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card Fax'
        verbose_name_plural = 'Business Card Fax'
        db_table = 'business_card_fax'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardJob(ABSTRACTDateModel,
                      ABSTRACTStatusModel,
                      ABSTRACTCreateUpdateByModel):
    """
    BusinessCardFax
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_Job')
    type = models.CharField(max_length=255, choices=JOB_TYPE)
    job_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card job'
        verbose_name_plural = 'Business Card job'
        db_table = 'business_card_job'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardMobile(ABSTRACTDateModel,
                         ABSTRACTStatusModel,
                         ABSTRACTCreateUpdateByModel):
    """
    BusinessCardMobile
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_mobile')
    type = models.CharField(max_length=255, choices=MOBILE_TYPE)
    mobile_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card Mobile'
        verbose_name_plural = 'Business Card Mobile'
        db_table = 'business_card_mobile'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardEmail(ABSTRACTDateModel,
                        ABSTRACTStatusModel,
                        ABSTRACTCreateUpdateByModel):
    """
    BusinessCardMobile
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_email')
    type = models.CharField(max_length=255, choices=EMAIL_TYPE)
    email_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card Email'
        verbose_name_plural = 'Business Card Email'
        db_table = 'business_card_email'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardSocialNetwork(ABSTRACTDateModel,
                                ABSTRACTStatusModel,
                                ABSTRACTCreateUpdateByModel):
    """
    BusinessCardMobile
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_social_network')
    type = models.CharField(max_length=255, choices=SOCIAL_NETWORK_TYPE)
    social_network_value = models.CharField(max_length=255,
                                            null=True,
                                            blank=True)

    class Meta:
        verbose_name = 'Business Card Social Network'
        verbose_name_plural = 'Business Card Social Network'
        db_table = 'business_card_social_network'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardAddress(ABSTRACTDateModel,
                          ABSTRACTStatusModel,
                          ABSTRACTCreateUpdateByModel):
    """
    BusinessCardAddress
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_address')
    type = models.CharField(max_length=255, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card Address'
        verbose_name_plural = 'Business Card Address'
        db_table = 'business_card_address'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardDates(ABSTRACTDateModel,
                        ABSTRACTStatusModel,
                        ABSTRACTCreateUpdateByModel):
    """
    BusinessCardAddress
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_date')
    type = models.CharField(max_length=255, choices=DATE_BIRTH_TYPE)
    date = models.DateField(auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card Dates'
        verbose_name_plural = 'Business Card Dates'
        db_table = 'business_card_dates'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardWeb(ABSTRACTDateModel,
                      ABSTRACTStatusModel,
                      ABSTRACTCreateUpdateByModel):
    """
    BusinessCardAddress
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_web')
    type = models.CharField(max_length=255, choices=WEBSITE_TYPE)
    website = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card Web'
        verbose_name_plural = 'Business Card Web'
        db_table = 'business_card_web'

    def __str__(self):
        return str(self.business_card.id)


class BusinessCardNotes(ABSTRACTDateModel,
                        ABSTRACTStatusModel,
                        ABSTRACTCreateUpdateByModel):
    """
    BusinessCardNotes
    """
    # social link share
    business_card = models.ForeignKey(
        BusinessCardReaderManager,
        on_delete=models.CASCADE,
        related_name='bussines_card_master_notes')
    type = models.CharField(max_length=255, choices=NOTES_TYPE)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Business Card Notes'
        verbose_name_plural = 'Business Card Notes'
        db_table = 'business_card_notes'

    def __str__(self):
        return str(self.business_card.id)


class BusinessExpenseManager(ABSTRACTDateModel,
                             ABSTRACTStatusModel,
                             ABSTRACTCreateUpdateByModel):
    """
    CardManager models
    """
    # uuid
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    # image media file
    expense_process_status = models.CharField(
        max_length=255,
        choices=REIMBURSEMENT_STATUS_DATA)
    expense_image = models.FileField(
        upload_to='expense_images/',
        null=True, blank=True)

    # abby screen attributes for name attr
    # expense_date = models.CharField(max_length=255, null=True, blank=True)
    merchant_name = models.CharField(max_length=255, null=True, blank=True)
    purchased_on = models.DateField(auto_now_add=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=255, null=True, blank=True)
    submit_to = models.CharField(max_length=255, null=True, blank=True)
    expense_type = models.ForeignKey(
        ExpenseTypeMaster,
        on_delete=models.CASCADE,
        related_name='business_card_expense_type',
        null=True, blank=True)

    # reimbursed details
    reimbursed_on = models.DateField(auto_now_add=False, null=True, blank=True)
    submitted_on = models.DateField(auto_now_add=True)
    reimbursed_by = models.CharField(max_length=255, null=True, blank=True)
    reimbursed_method = models.CharField(max_length=255, null=True, blank=True)
    expense_capture_type = models.CharField(max_length=255,
                                            null=True, blank=True,
                                            choices=EXPENSE_TYPE_DATA)

    # all api response attr refr from abby manage the flag to handle abby services
    abby_response_id = models.CharField(max_length=255, null=True, blank=True)
    is_card_retrived = models.BooleanField(default=False)
    retrive_status = models.CharField(max_length=255,
                                      choices=RETRIVE_STATUS_DATA)
    reason_for_failed = models.CharField(max_length=255, null=True, blank=True)
    failed_count = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='user_business_card_expense')

    class Meta:
        verbose_name = 'Expense Reader Manager'
        verbose_name_plural = 'Expense Reader Manager'
        db_table = 'business_expense_reader_manager'

    def __str__(self):
        return str(self.id)
