from datetime import timedelta

"""
all constants varialbes for using this projects
"""

# Device type for using data identify
DEVICE_TYPE = [("android", "Mobile/Android"), ("ios", "Mobile/iOS"), ("web", "Web")]

# Notification configuration choice fields
NOTIFICATION_FOR = [
    ("member", "member"),
    ("customer", "customer"),
    ("manager", "manager"),
    ("admin", "Admin"),
    ("bcr_user", "BCR"),
]

# Notification category choice fields
NOTIFICATION_CATEGORY = [("PUSH", "PUSH"), ("SMS", "SMS"), ("EMAIL", "EMAIL")]

# Otp status choice fields
OTP_STATUS = [
    ("delivered", "Delivered"),
    ("not_delivered", "Not Delivered"),
    ("successful", "Successful"),
    ("expired", "Expired"),
]

# Otp Service types
SERVICE_TYPE = [("phone", "Phone Number"), ("email", "Email ID")]

ACCESS_STATUS = [("allow_to_all", "allow"), ("self_only", "self")]

APP_TYPE = [("BCR", "BCR"), ("BEM", "BEM"), ("EISEN", "Eisenhower")]

# OTP EXPIRY TIME PERIOD
SMS_OTP_EXPIRY = timedelta(minutes=30)

RETRIVE_STATUS_DATA = [
    ("initiate", "INITIATE"),
    ("pending", "PENDING"),
    ("retrive", "RETRIVE"),
    ("failed", "FAILED"),
    ("discard", "DISCARD"),
]

EXPENSE_TYPE_DATA = [
    ("manual", "Manual"),
    ("automated", "Automated"),
]

REIMBURSEMENT_STATUS_DATA = [
    ("drafted", "Drafted"),
    ("submitted", "Submitted"),
    ("reimbursed", "Reimbursed"),
]

# all business card object enum choice fields
JOB_TYPE = [
    ("company", "company"),
    ("position", "position"),
    ("department", "department"),
]

COMMON_WORK_TYPE = [
    ("work", "work"),
    ("home", "home"),
    ("other", "other"),
    ("main", "main"),
]

FAX_TYPE = COMMON_WORK_TYPE
MOBILE_TYPE = COMMON_WORK_TYPE
EMAIL_TYPE = COMMON_WORK_TYPE

SOCIAL_NETWORK_TYPE = [
    ("facebook", "facebook"),
    ("linkedin", "linkedin"),
    ("twitter", "twitter"),
    ("googletalk", "googletalk"),
    ("hangout", "hangout"),
    ("skype", "skype"),
    ("gadugadu", "gadugadu"),
    ("yahoo", "yahoo"),
    ("msn", "msn"),
    ("qq", "qq"),
    ("icq", "icq"),
    ("aim", "aim"),
]

ADDRESS_TYPE = [
    ("company", "company"),
    ("home", "home"),
    ("other", "other"),
    ("main", "main"),
]

DATE_BIRTH_TYPE = [
    ("birthday", "birthday"),
    ("anniversary", "anniversary"),
    ("other", "other"),
]

WEBSITE_TYPE = [
    ("work", "work"),
    ("home", "home"),
    ("personal", "personal"),
    ("other", "other"),
]

NOTES_TYPE = [("rough", "rough"), ("fair", "fair")]
