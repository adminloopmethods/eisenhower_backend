from django.contrib import admin

# Register your models here.
from cards.models import (CategoryGroupMaster, 
                          UserCategoryGroupMaster,
                          BusinessCardReaderManager, 
                          BusinessCardSocialLink, 
                          BusinessCardFax,
                          BusinessCardJob,
                          BusinessCardMobile,
                          BusinessCardEmail,
                          BusinessCardSocialNetwork,
                          BusinessCardAddress,
                          BusinessCardDates,
                          BusinessCardWeb,
                          BusinessCardNotes,
                          BusinessExpenseManager)

# Register your models here.
admin.site.register(CategoryGroupMaster)
admin.site.register(UserCategoryGroupMaster)
admin.site.register(BusinessCardReaderManager)
admin.site.register(BusinessCardSocialLink)

# all object business card data
admin.site.register(BusinessCardFax)
admin.site.register(BusinessCardJob)
admin.site.register(BusinessCardMobile)
admin.site.register(BusinessCardEmail)
admin.site.register(BusinessCardSocialNetwork)
admin.site.register(BusinessCardAddress)
admin.site.register(BusinessCardDates)
admin.site.register(BusinessCardWeb)
admin.site.register(BusinessCardNotes)
admin.site.register(BusinessExpenseManager)

