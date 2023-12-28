"""ExportSampleExportExcelTask
this module used to get the sample xlsx and put the Excel file to database
created at 12/feb/2023
by Loop developer
"""

import xlwt
from django.http import HttpResponse


class ExportSampleExportExcelTask:
    """
    this module used to get the sample xlsx and put the Excel file to database
    dc: https://xlsxwriter.readthedocs.io/format.html
    GS: https://studygyaan.com/django/how-to-export-excel-file-with-django
    """

    def __init__(self, **kwargs):
        self.auth_instance = kwargs.get('auth_instance', None)
        self.custom_user_id = kwargs.get('custom_user_id', None)
        self.xlsx_column = []

    def export_task_sample_sheet_xlsx(self):
        """this export_task_sample_sheet method used to download the
        dynamic Excel sheet from task models
        :return: sample_sheet
        """
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="tasks.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        # this will make a sheet named Users Data
        ws = wb.add_sheet('Sheet1')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = self.xlsx_column
