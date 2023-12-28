from django.urls import path

from web_api_service.bcr.abby_apis.upload_business_card import TestImagesUpload
from web_api_service.bcr.abby_apis.upload_business_card import UploadBusinessCardImages
from web_api_service.bcr.business_card_reader.business_card_api import BusinessCardDelete
from web_api_service.bcr.business_card_reader.business_card_api import BusinessCardDetail
# BCR APIs
# import buisness card apis
from web_api_service.bcr.business_card_reader.business_card_api import BusinessCardList
from web_api_service.bcr.business_card_reader.business_card_api import CategoryGroupList
from web_api_service.bcr.business_card_reader.business_card_api import SendBusinessCardEmail
from web_api_service.bcr.business_card_reader.business_card_api import UpdateBusinessCardDetail
from web_api_service.bcr.business_card_reader.business_card_qr_code import BusinessCardQrCardDetail
from web_api_service.bcr.export.api import ExportBusinessCardList
from web_api_service.bcr.search_filters.business_card_filter_api import BusinessCardFilter
# import business card serach and filter api
from web_api_service.bcr.search_filters.business_card_filter_api import BusinessCardSearch
from web_api_service.bem.expense_detail_apis import BusinessExpenseDetails
from web_api_service.bem.expense_detail_apis import BusinessExpenseList
from web_api_service.bem.expense_detail_apis import ExpenseMasterList
from web_api_service.bem.expense_detail_apis import UpdateBusinessExpenseDetail
from web_api_service.bem.expense_search_filter import BusinessExpenseFilter
from web_api_service.bem.expense_search_filter import BusinessExpenseSearch
from web_api_service.bem.export_expense_api import ExportBusinessExpenseList
from web_api_service.bem.upload_business_expense import UploadBusinessExpenseImages
from web_api_service.configuration.all_config_view import ColorMasterApi
from web_api_service.configuration.all_config_view import CountryMasterApi
from web_api_service.configuration.all_config_view import CurrencyMasterApi
from web_api_service.configuration.all_config_view import DepartmentMasterApi
# @@import master apis
from web_api_service.configuration.all_config_view import LanguageMasterApi
from web_api_service.configuration.all_config_view import StatusMasterApi
from web_api_service.configuration.all_config_view import TopicsMasterApi
from web_api_service.configuration.all_config_view import UserRoleMasterApi
# @@import department and topics apis
from web_api_service.configuration.viewsets import DepartmentApi
from web_api_service.configuration.viewsets import DepartmentTaskUpdateApi
from web_api_service.configuration.viewsets import DepartmentDetailApi
from web_api_service.configuration.viewsets import DepartmentImportSheetApi
from web_api_service.configuration.viewsets import DepartmentSampleSheetApi
from web_api_service.configuration.viewsets import DepartmentSearchApi
from web_api_service.configuration.viewsets import LanguageApi
from web_api_service.configuration.viewsets import TopicApi
from web_api_service.configuration.viewsets import TopicDetailApi
from web_api_service.configuration.viewsets import TopicDetailTaskUpdateApi
from web_api_service.configuration.viewsets import TopicSearchApi
# @@import dashboard and matrix apis
from web_api_service.matrix.viewsets import DashboardApi
# import notification record
from web_api_service.notification.viewsets import NotificationCountApi
from web_api_service.notification.viewsets import NotificationRecordApi
# @@import task management apis
from web_api_service.tasks.viewsets import CreateTaskApi, TaskCommentsApi
from web_api_service.tasks.viewsets import ExportTasks
from web_api_service.tasks.viewsets import TaskDetailsApi
from web_api_service.tasks.viewsets import TaskFilterApi
from web_api_service.tasks.viewsets import TaskImportExcelSheetApi
from web_api_service.tasks.viewsets import TaskListApi
from web_api_service.tasks.viewsets import TaskStatusChangeApi
from web_api_service.tasks.viewsets import TaskUpdateApi
from web_api_service.users.viewsets import ActiveMemberUserListApi
from web_api_service.users.viewsets import CognitoUserLoginApi
from web_api_service.users.viewsets import LoginUser
# @@import user and team member apis
from web_api_service.users.viewsets import MemberActivateDeactivateApi
from web_api_service.users.viewsets import MemberFilterApi
from web_api_service.users.viewsets import MemberImportExcelSheetApi
from web_api_service.users.viewsets import MemberSampleSheetApi
from web_api_service.users.viewsets import MemberSearchApi
from web_api_service.users.viewsets import MemberUpdateApi
from web_api_service.users.viewsets import MemberUserCreateApi
from web_api_service.users.viewsets import MemberUserListAddTaskApi
from web_api_service.users.viewsets import MemberUserListApi
from web_api_service.users.viewsets import UpdateTaskMemberUserListApi
from web_api_service.users.viewsets import TeamActivateDeactivateApi
from web_api_service.users.viewsets import TeamDetailApi
from web_api_service.users.viewsets import TeamMemberDetailsApi
from web_api_service.users.viewsets import TeamMemberListApi
from web_api_service.users.viewsets import UserDetails
from web_api_service.users.viewsets import UserDetailsUpdate
from web_api_service.users.viewsets import UserStickyNotesApi

# import apis urls
configuration_urls_path = [
    path("config/language/", LanguageApi.as_view()),
    path("config/languages/", LanguageMasterApi.as_view()),
    path("config/topics/", TopicsMasterApi.as_view()),
    path("config/departments/", DepartmentMasterApi.as_view()),
    path("config/status/", StatusMasterApi.as_view()),
    path("config/currencies/", CurrencyMasterApi.as_view()),
    path("config/colors/", ColorMasterApi.as_view()),
    path("config/userRoles/", UserRoleMasterApi.as_view()),
    path("config/countries/", CountryMasterApi.as_view()),
    path("config/department/", DepartmentApi.as_view()),
    path("config/department/task/update/", DepartmentTaskUpdateApi.as_view()),
    path("config/topic/", TopicApi.as_view()),
    path("config/department/detail/", DepartmentDetailApi.as_view()),
    path("config/topic/detail/", TopicDetailApi.as_view()),
    path("config/topic/detail/task/update/", TopicDetailTaskUpdateApi.as_view()),
    # department and topics search
    path("config/department/search/", DepartmentSearchApi.as_view()),
    path("config/topic/search/", TopicSearchApi.as_view()),
    # department import and sample sheet api
    path("config/department/sample/sheet/", DepartmentSampleSheetApi.as_view()),
    path("config/department/import/sheet/", DepartmentImportSheetApi.as_view()),
]

user_urls_path = [
    # list of member details
    path("user/detail/", UserDetails.as_view()),
    path("user/detail/update/", UserDetailsUpdate.as_view()),
    path("user/login/", LoginUser.as_view()),
    # add member api
    path("user/create/", MemberUserCreateApi.as_view()),
    path("user/members/", MemberUserListApi.as_view()),
    path("user/members/task/update/", UpdateTaskMemberUserListApi.as_view()),
    
    path("user/active/members/", ActiveMemberUserListApi.as_view()),
    path("user/members/add/task/", MemberUserListAddTaskApi.as_view()),
    path("user/members/active/", MemberActivateDeactivateApi.as_view()),
    path("user/sample/sheet/", MemberSampleSheetApi.as_view()),
    path("user/import/", MemberImportExcelSheetApi.as_view()),
    path("user/cognito/login/", CognitoUserLoginApi.as_view()),
    # team paths
    path("team/", TeamDetailApi.as_view()),
    path("team/active/", TeamActivateDeactivateApi.as_view()),
    path("team/member/list/", TeamMemberListApi.as_view()),
    path("team/member/detail/", TeamMemberDetailsApi.as_view()),
    path("team/member/search/", MemberSearchApi.as_view()),
    path("team/member/filter/", MemberFilterApi.as_view()),
    path("team/member/update/", MemberUpdateApi.as_view()),
    path("user/sticky/notes/", UserStickyNotesApi.as_view()),
]

matrix_urls_path = [
    path("matrix/dashboard/", DashboardApi.as_view()),
]

tasks_urls_path = [
    path("task/create/", CreateTaskApi.as_view()),
    path("task/detail/", TaskDetailsApi.as_view()),
    path("task/list/", TaskListApi.as_view()),
    path("task/statusUpdate/", TaskStatusChangeApi.as_view()),
    path("task/filter/", TaskFilterApi.as_view()),
    path("task/export/", ExportTasks.as_view()),
    path("task/update/", TaskUpdateApi.as_view()),
    path("task/comments/", TaskCommentsApi.as_view()),
    path("task/bulk/import/", TaskImportExcelSheetApi.as_view()),
]

notification_urls_path = [
    path("notification/count/", NotificationCountApi.as_view()),
    path("notification/record/", NotificationRecordApi.as_view()),
]

bcr_urls_path = [
    path("business/card/list/", BusinessCardList.as_view()),
    path("business/card/detail/", BusinessCardDetail.as_view()),
    path("business/card/update/", UpdateBusinessCardDetail.as_view()),
    path("business/card/delete/", BusinessCardDelete.as_view()),
    path("business/card/email/send/", SendBusinessCardEmail.as_view()),
    path("business/card/qr/code/", BusinessCardQrCardDetail.as_view()),
    # category list
    path("business/card/category/", CategoryGroupList.as_view()),
    # search and filter apis
    path("business/card/search/", BusinessCardSearch.as_view()),
    path("business/card/filter/", BusinessCardFilter.as_view()),
    # export business card
    path("business/card/export/", ExportBusinessCardList.as_view()),
    # upload business card img
    path("business/card/upload/", UploadBusinessCardImages.as_view()),
    path("business/card/test/upload/", TestImagesUpload.as_view()),
]

bem_urls_path = [
    path("business/expense/list/", BusinessExpenseList.as_view()),
    path("business/expense/detail/", BusinessExpenseDetails.as_view()),
    path("business/expense/update/", UpdateBusinessExpenseDetail.as_view()),
    path("business/expense/search/", BusinessExpenseSearch.as_view()),
    path("business/expense/filter/", BusinessExpenseFilter.as_view()),
    path("business/expense/type/", ExpenseMasterList.as_view()),
    path("business/expense/upload/", UploadBusinessExpenseImages.as_view()),
    path("business/expense/export/", ExportBusinessExpenseList.as_view()),
]

urlpatterns = (
        configuration_urls_path
        + user_urls_path
        + matrix_urls_path
        + tasks_urls_path
        + notification_urls_path
        + bcr_urls_path
        + bem_urls_path
)
