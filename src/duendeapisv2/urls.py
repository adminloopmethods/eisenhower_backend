"""DuendeV2ApiUrls
created at 12/feb/2023
by Loop developer
"""

from django.urls import path

from duendeapisv2.views_api.task_import_export import \
    TaskExportSampleImportExcelSheetApi

task_urls_path = [
    path("task/bulk/import/", TaskExportSampleImportExcelSheetApi.as_view()),
]

urlpatterns = task_urls_path
