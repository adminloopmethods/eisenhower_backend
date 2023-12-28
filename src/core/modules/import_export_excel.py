"""Import Export module
this import export module used to manage 
the all import and export related features with sample import sheet end 
export detail sheet
"""

# excel sheet related package
import csv
import json
import pathlib
# random number
from random import randint

from itertools import chain

import pandas as pd
import xlwt
# django module
# from django.contrib.auth.models import User
from account.models import User

from django.http import HttpResponse

# all models
from configuration.models import Departments, UserRoleMaster
from user.models import UserDepartmentMapping
# core module
from core.constants import ACCESS_STATUS
from core.messages import MSG, ITALIAN_MSG

from location.models import CountryMaster
from user.models import CustomUsers
# web apis
from web_api_service.cognito.aws_cognito_auth import AWSCognito
from web_api_service.helpers.all_config_func import get_department_id_from_name
from web_api_service.helpers.all_config_func import custom_user_id
from web_api_service.helpers.all_config_func import get_language_uuid
from web_api_service.helpers.all_config_func import get_role_id_from_name
# validation and memner service
from web_api_service.helpers.validations import APIValidation
from web_api_service.users.member_service import UserMemberService

from web_api_service.users.services import UserService

FILENAME = 'Sheet1'
CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'



# CONTENT_TYPE = 'text/csv'
# CONTENT_TYPE = 'application/ms-excel'


class ImportExportExcel:
    """
    ImportExportExcel
    https://stackoverflow.com/questions/20040965/how-to-export-data-in-python-with-excel-format

    https://stackoverflow.com/questions/25199507/writing-resutls-into-2-different-sheets-in-the-same-excel-file
    """

    def __init__(self, **kwargs):

        # for mutual helpfull variables
        self.input = kwargs
        self.auth_user_instance = kwargs.get('auth_user_instance', None)
        self.custom_user_id = kwargs.get('custom_user_id', None)
        self.request_input_data = None
        self.queryset = kwargs.get('queryset')
        self.model_class = kwargs.get('model_class')
        self.http_response = kwargs.get('http_response', HttpResponse)
        self.auth_instance = kwargs.get('auth_instance', None)
        self.customer_instance = kwargs.get('customer_id', None)
        

        # for only export related variables
        self.excel_field_list = kwargs.get('excel_field_list', [])
        self.excel_title_list = kwargs.get('excel_title_list', [])
        self.import_sample_filename = kwargs.get('import_sample_filename', FILENAME)
        self.file_content_type = kwargs.get('file_content_type', CONTENT_TYPE)
        self.import_sample_filename = 'attachment; filename={}.csv'.format(
            self.import_sample_filename
        )

        # for only import related variables
        self.import_db_dict = {
            'member': '__member__',
            'department': '__department__'
        }
        self.access_status_dict = {'Y': 'y', 'N': 'n'}
        self.new_old_status_dict = {'old': 'OLD', 'new': 'NEW'}

        self.excel_import_type = kwargs.get('import_type', None)
        self.excel_sheet_media = kwargs.get('excel_sheet', [])
        self.model_instance = kwargs.get('model_instance', None)
        self.mapping_model_class = kwargs.get('mapping_model_class')
        self.excel_sheet_path = kwargs.get('excel_sheet_path', [])
        self._json_input_data = None
        self.excel_sheet_name = kwargs.get('excel_sheet_name', FILENAME)
        self.member_serializer_data = None
        self.new_created_ids = []
        self.data_pool_list = []
        self.import_result_response = dict()
        self.models_id_list = list()
        self.query_params_var = dict()
        self._create_pool_params = dict()
        self.__pwd = 'Admin@123'

        self.success = True
        self.msg = MSG['DONE']
        self.excel_file_extension = ['.xlsx', '.csv', '.xls']
        self.display_alert_keyword = ""
        self.auth_user_language = kwargs.get('auth_user_language', None)
        self._is_cognito_user = False

    def _nested_getattr(self, obj, attribute, split_rule='__'):
        """
        This function is responsible for getting the nested
        record from the given obj parameter
        """
        _excel_split_attr = attribute.split(split_rule)
        for _attr_value in _excel_split_attr:
            if not obj:
                break
            obj = getattr(obj, _attr_value)
        return obj

    def _export_excel(self):
        """this function used to export the Excel file for
        sample with check validated and verified data.
        """
        # django models instance
        _excel_fields, _excel_titles = self.excel_field_list, self.excel_title_list
        _xlsx_model_instance = self.queryset.model

        # force download
        _response = self.http_response(content_type=self.file_content_type)
        _response['Content-Disposition'] = self.import_sample_filename

        # the csv writer
        writer = csv.writer(_response)
        if _excel_fields:
            _headers = _excel_fields
            if _excel_titles:
                _excel_titles = _excel_titles
            else:
                _excel_titles = _headers
        else:
            _headers = []

            for _field in _xlsx_model_instance._meta._excel_fields:
                _headers.append(_field.name)
            _excel_titles = _headers

        # Writes the title for the file
        writer.writerow(_excel_titles)
        # write data rows
        for _item in self.queryset:
            writer.writerow([self._nested_getattr(_item, _field) for _field in _headers])
        return _response

    @staticmethod
    def member_excel_data(ws):
        """this method member_excel_data used to collect member 
        related data to store data
        """
        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [
            'first_name',
            'last_name',
            'isd',
            'mobile',
            'email',
            'department',
            'role',
            'color',
            'access_status',
        ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        try:
            # single random object
            _random_instance_object = CustomUsers.objects.all()[
                randint(0, CustomUsers.objects.count() - 1)
            ]
        except Exception as e:
            print('Departments.DoesNotExist: %s' % e)
            _random_instance_object = None

        _query_rows = CustomUsers.objects.filter(
            id=_random_instance_object.id
        ).values_list('first_name',
                      'last_name',
                      'isd',
                      'mobile',
                      'email',
                      'access_status',
                      'department__department_name',
                      'color_hex_code',
                      'role__role_name'
                      )

        rows = [('Dummy',
                 'Cruise',
                 '39',
                 '9999999999',
                 'Dummy@gmail.com',
                 'Department',
                 'Dummy',
                 '#e69cb2',
                 'Y'),
                ('Dummy',
                 'Biden',
                 '39',
                 '9999999999',
                 'Dummybid@gmail.com',
                 'Department',
                 'Dummy',
                 '#e69cb2',
                 'N')]

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    @staticmethod
    def department_excel_data(ws, _custom_user_id):
        """this method member_excel_data used to collect member 
        related data to store data
        """
        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['department']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Departments.objects.filter(
            is_active=True,
            access_status=ACCESS_STATUS[0][0]
        ).values_list('department_name')
        
        try:
            _user_department_mapping = UserDepartmentMapping.objects.get(
                is_active=True,
                user_id=_custom_user_id
            )
        except UserDepartmentMapping.DoesNotExist:
            print('UserDepartmentMapping.DoesNotExist')
            _user_department_mapping = None

        try:
            departments_values_list = _user_department_mapping.departments.filter(
                is_active=True
            ).values_list('department_name')
        except Exception as e:
            departments_values_list = None
            print('userDepartmentMappingExpErr')
            print(e)

        try:
            rows = list(set(list(chain(rows, departments_values_list))))
        except Exception as e:
            print('concanateQuerySetExpErr')
            print(e)

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    @staticmethod
    def roles_excel_data(ws, _custom_user_id):
        """this method member_excel_data used to collect member 
        related data to store data
        """
        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['role']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        try:
            custom_user_instance = CustomUsers.objects.get(id=_custom_user_id)
        except CustomUsers.DoesNotExist:
            custom_user_instance = None

        if custom_user_instance:
            if custom_user_instance.role.role == 'MEMBER':
                rows = UserRoleMaster.objects.filter(
                    role='DUMMY',
                    is_active=True).values_list('role_name')
            else:
                rows = UserRoleMaster.objects.filter(
                    is_active=True).values_list('role_name')                
        else:
            rows = UserRoleMaster.objects.filter(
                is_active=True).values_list('role_name')

        # Sheet body,
        # remaining rows
        font_style = xlwt.XFStyle()
        # rows = UserRoleMaster.objects.filter(
        # is_active=True).values_list('role_name')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    @staticmethod
    def countries_excel_data(ws):
        """this countries_excel_data method collect the countries excel data
        """
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['country', 'isd']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = CountryMaster.objects.filter(is_active=True).values_list('country', 'isd')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    def export_excel(self):
        """this function used to export the Excel file for
        sample with check validated and verified data.
        """
        # django models instance
        # response = HttpResponse(content_type='application/ms-excel')
        # response['Content-Disposition'] = 'attachment; filename="users.xls"'
        response = HttpResponse(content_type=self.file_content_type)
        response['Content-Disposition'] = self.import_sample_filename

        wb = xlwt.Workbook(encoding='utf-8')
        members_ws = wb.add_sheet('Sheet1')
        department_ws = wb.add_sheet('department')
        roles_ws = wb.add_sheet('roles')
        countries_ws = wb.add_sheet('countries')

        self.member_excel_data(members_ws)
        # try:
        # self.department_excel_data(department_ws, self.customer_instance)
        # self.roles_excel_data(roles_ws, self.customer_instance.id)
        # # except Exception as e:
        # #     print('customer instance erroo')
        # #     print(e)
        self.department_excel_data(department_ws, self.custom_user_id)
        self.roles_excel_data(roles_ws, self.custom_user_id)
        self.countries_excel_data(countries_ws)

        wb.save(response)
        return response

    def _manage_import_response_msg(self):
        """this _manage_import_response_msg method used to 
        manage the all success import messages
        """
        if len(self.new_created_ids) >= 1 and len(self.data_pool_list) >= 1:
            self.display_alert_keyword = '2'
            try:
                if self.excel_import_type == self.import_db_dict['department']:
                    if self.auth_user_language == 'ENG':
                        self.msg = ''.join(
                            [
                                'In Total, ',
                                str(len(self._json_input_data)),
                                ' records, ',
                                str(len(self.data_pool_list)),
                                ' Department already exist, ',
                                str(len(self.new_created_ids)),
                                ' uploaded successfully'
                            ]
                        )
                    else:
                        self.msg = ''.join(
                            [
                                'In totale',
                                str(len(self._json_input_data)),
                                ' record ',
                                str(len(self.data_pool_list)),
                                ' Funzione / Team esiste già',
                                str(len(self.new_created_ids)),
                                ' caricati con successo'
                            ]
                        )
                else:
                    if self.auth_user_language == 'ENG':
                        self.msg = ''.join(
                            [
                                'In Total, ',
                                str(len(self._json_input_data)),
                                ' records, ',
                                str(len(self.data_pool_list)),
                                ' users already exist, ',
                                str(len(self.new_created_ids)),
                                ' uploaded successfully'
                            ]
                        )
                    else:
                        self.msg = ''.join(
                            [
                                'In totale',
                                str(len(self._json_input_data)),
                                ' record ',
                                str(len(self.data_pool_list)),
                                ' utenti esiste già',
                                str(len(self.new_created_ids)),
                                ' caricati con successo'
                            ]
                        )
            except Exception as e:
                self.msg = MSG['IMPORT_SUCCESSFULLY']
                print('NewWithAlreadyExistException')
                print(e)

        if len(self.new_created_ids) >= 1 and len(self.data_pool_list) == 0:
            self.display_alert_keyword = '1'
            if self.auth_user_language == 'ENG':
                self.msg = MSG['IMPORT_SUCCESSFULLY']
            else:
                self.msg = ITALIAN_MSG['IMPORT_SUCCESSFULLY']

        if len(self.new_created_ids) == 0 and len(self.data_pool_list) >= 1:
            self.display_alert_keyword = '3'
            try:
                if self.excel_import_type == self.import_db_dict['department']:
                    if self.auth_user_language == 'ENG':
                        self.msg = ''.join(
                            [
                                'In Total, ', str(len(self._json_input_data)),
                                ' records, ', str(len(self.data_pool_list)),
                                ' Department already exist.'
                            ]
                        )
                    else:
                        self.msg = ''.join(
                            [
                                'In totale, esistono già ', str(len(self._json_input_data)),
                                ' record ', str(len(self.data_pool_list)),
                                ' Funzione/Team'
                            ]
                        )
                else:
                    if self.auth_user_language == 'ENG':
                        self.msg = ''.join(
                            [
                                'In Total, ', str(len(self._json_input_data)),
                                ' records, ', str(len(self.data_pool_list)),
                                ' users already exist.'
                            ]
                        )
                    else:
                        self.msg = ''.join(
                            [
                                'In totale, esistono già ', str(len(self._json_input_data)),
                                ' record ', str(len(self.data_pool_list)), ' utenti'
                            ]
                        )
            except Exception as e:
                self.msg = MSG['IMPORT_SUCCESSFULLY']
                print('UserAlreadyExistException')
                print(e)

    def already_exist_continue(self):
        """this already_exist_continue method is used to check Whether
        """
        return self.model_class.objects.filter(**self.query_params_var).exists()

    def assign_user_data(self, _model_instance, _data):
        """assign_user_data
        """
        user_query_parameters = {
            'user': self.auth_instance.user_auth
        }
        self.models_id_list.append(_model_instance.id)
        _mapping_instance = self.mapping_model_class.objects.filter(**user_query_parameters).first()
        if not _mapping_instance:
            _mapping_instance = self.mapping_model_class.objects.create(**user_query_parameters)
        if _mapping_instance:
            if self.excel_import_type == self.import_db_dict['department']:
                _mapping_instance.departments.add(*self.models_id_list)
            if self.excel_import_type == self.import_db_dict['member']:
                _mapping_instance.members.add(*self.models_id_list)

    def _pool_data(self, _model_instance, _data, old_new_flag):
        """_pool_data this method used to get the pool data for the 
        models instance and json values
        """
        if self.excel_import_type == self.import_db_dict['department']:
            final_id_dict = {
                'id': _model_instance.id,
                'department_name': _model_instance.department_name
            }

        if old_new_flag == self.new_old_status_dict['old']:
            self.data_pool_list.append(final_id_dict)
        if old_new_flag == self.new_old_status_dict['new']:
            self.new_created_ids.append(final_id_dict)

    def _create_pool_data(self, _model_instance, _data):
        """this  _create_pool_data method used to create pool data for all type 
        models as per import type
        """
        if _data.get('access_status').lower() == self.access_status_dict['N']:
            self.assign_user_data(_model_instance, _data)
        self._pool_data(_model_instance, _data,
                        self.new_old_status_dict['new'])

    def get_or_create_pool_data(self, _data):
        """get_or_create_pool_data
        this method used to get and create pool data from models
        """
        _model_instance, _created = self.model_class.objects.get_or_create(**self._create_pool_params)
        if _created:
            self._create_pool_data(_model_instance, _data)
        if not _created:
            self._pool_data(_model_instance, _data,
                            self.new_old_status_dict['old'])

    def _instance_of_already_exist(self):
        """_instance_of_already_exist
        """
        try:
            return self.model_class.objects.filter(**self.query_params_var).last()
        except Exception as e:
            print('ModelS.DoesNotExist')
            print(e)
            return None

    def _assign_query_parameter(self, _data):
        """this assign_query_parameter used to assign params
        """
        if self.excel_import_type == self.import_db_dict['department']:
            department_name = str(_data['department_name']).title()
            department_name = " ".join(department_name.strip().split())

            # @@for already exist query parameters
            self.query_params_var['department_name'] = department_name

            # @@for create a department
            self._create_pool_params['department_name'] = department_name
            self._create_pool_params['access_status'] = (
                ACCESS_STATUS[0][0]
                if _data['access_status'].lower() == self.access_status_dict['Y'] else
                ACCESS_STATUS[1][0]
            )

        if self.excel_import_type == self.import_db_dict['member']:
            _email = _data['email'].lower()

            # @@for already exist query parameters
            self.query_params_var['username'] = _email

            # @@for auth user creation data
            self._create_pool_params['first_name'] = _data['first_name'].capitalize()
            self._create_pool_params['last_name'] = _data['last_name'].capitalize()
            self._create_pool_params['email'] = _email
            self._create_pool_params['username'] = _email
            self._create_pool_params['password'] = self.__pwd
            self._create_pool_params['is_active'] = True

    def _create_auth_user_with_member_details(self, _data):
        """this _create_auth_user_with_member_details
        method used to create the auth user with all user member details and access status
        """

        try:
            cognito_response_data = AWSCognito(
                data={
                    'first_name': _data['first_name'].capitalize(),
                    'last_name': _data['last_name'].capitalize(),
                    'email': _data['email'].lower(),
                    'isd': _data.get('isd', None),
                    'mobile': _data['mobile'],
                    'department': _data['department'],
                    'role': _data['role'],
                    'password': self.__pwd
                }
            ).confirm_sign_up()
        except Exception as e:
            cognito_response_data = None
            self._is_cognito_user = False
            _error_msg = str(e)
            print('AWSCognitoExceptionErr')
            print(e)

        try:
            self._is_cognito_user = True if cognito_response_data else False
        except Exception as e:
            print('cognitoCreateExpErr')
            print(e)

        try:
            self.member_auth_instance = UserService().create_auth_user(self._create_pool_params)
        except Exception as e:
            print('AuthUserCreation.DoesNotExist')
            print(e)

        if self.member_auth_instance:
            _department_id = get_department_id_from_name(_data['department'])
            _role_id = get_role_id_from_name(_data['role'])

            try:
                _language_uuid = get_language_uuid('ENG')
            except Exception as e:
                _language_uuid = None
                print(e)

            if _department_id and _role_id:
                member_data = {
                    'first_name': _data['first_name'].capitalize(),
                    'last_name': _data['last_name'].capitalize(),
                    'email': _data['email'].lower(),
                    'mobile': _data['mobile'],
                    'registration_type': 'web',
                    'department': _department_id,
                    'role': _role_id,
                    'auth_user': self.member_auth_instance.id,
                    'isd': _data.get('isd', None),
                    'language': _language_uuid,

                    'is_cognito_user': self._is_cognito_user,

                    'color_hex_code': (_data.get('color', '#000000')
                                       if _data.get('color', '#000000') else
                                       '#000000'),

                    'access_status': (ACCESS_STATUS[0][0]
                                      if _data['access_status'].lower() == self.access_status_dict['Y'] else
                                      ACCESS_STATUS[1][0])
                }
                try:
                    self.member_serializer_data = UserMemberService(

                    ).create_member_with_access_status(member_data)
                    if _data['access_status'].lower() == self.access_status_dict['Y']:
                        self.new_created_ids.append(
                            {
                                'id': self.member_serializer_data['id'],
                                'email': self.member_serializer_data['email']
                            }
                        )
                except Exception as e:
                    User.objects.filter(id=self.member_auth_instance.id).delete()
                    self.success = False
                    self.msg = str(e)
                    print('UserMemberService.Serializer')
                    print(e)

                if self.member_serializer_data:
                    if _data['access_status'].lower() == self.access_status_dict['N']:
                        _mapping_response_dict = UserMemberService(
                            auth_instance=self.auth_instance
                        ).assign_user_mapping(self.member_serializer_data)
                        if _mapping_response_dict['success'] is True:
                            self.new_created_ids.append(
                                {
                                    'id': self.member_serializer_data['id'],
                                    'email': self.member_serializer_data['email']
                                }
                            )

    def import_pool_data(self):
        """
        this import_pool_data method used to import the pool data
        """
        for _data in self._json_input_data:
            self._assign_query_parameter(_data)
            if self.already_exist_continue():
                self.data_pool_list.append(
                    custom_user_id(self._instance_of_already_exist().id)
                    if self.excel_import_type == self.import_db_dict['member'] else self._instance_of_already_exist().id
                )
                continue
            if self.excel_import_type == self.import_db_dict['member']:
                self._create_auth_user_with_member_details(_data)
            else:
                self.get_or_create_pool_data(_data)

    def get_file_extension(self):
        """this get_file_extension used to get the file
        extensions from pathlib library
        """
        try:
            return pathlib.Path(self.excel_sheet_path).suffix
        except Exception as e:
            print('getFileExtensionException')
            print(e)
            return None

    def get_json_from_excel(self):
        """this get_json_from_excel method used to get json the data using pandas lib
        """
        df_data = pd.read_excel(self.excel_sheet_path, self.excel_sheet_name)
        _json_format_data = df_data.to_json(orient='records')
        self._json_input_data = json.loads(_json_format_data)
        print(self._json_input_data)
        # pprint.pprint(self._json_input_data)

    def import_excel(self):
        """this function used to import the xlsx file for the global
        model level system.
        in this method we covered the department and member details import using excel sheet
        Excel sheet sample sheet import for member and department
        [{'first_name': 'Dummy', 
          'last_name': 'Cruise', 'isd': 39, 'mobile': 9999999999, 
          'email': 'aaaaaa@gmail.com', 
          'department': 'Department', 
          'role': 'Admin', 'color': '#e69cb2', 
          'access_status': 'Y'}]
        AWSCognitoExceptionErr
        sequence item 2: expected str instance, int found
        """
        _file_extension = self.get_file_extension()
        if not _file_extension:
            return False, {}, MSG['UPLOAD_VALID_EXCEL']
        if str(_file_extension) in self.excel_file_extension:
            self.get_json_from_excel()
            if not self._json_input_data:
                return False, {}, 'Please upload correct sheet'

            for row, _data in enumerate(self._json_input_data):

                # for members services validation call
                if self.excel_import_type == self.import_db_dict['member']:
                    if 'first_name' not in list(_data.keys()) or 'last_name' not in list(_data.keys()):
                        if self.auth_user_language == 'ENG':
                            return False, {}, 'Please upload correct sheet'
                        else:
                            return False, {}, 'Si prega di caricare il foglio corretto'

                    self.msg, self.success = APIValidation(
                        custom_user_role=self.auth_instance.user_auth.role.role
                    ).check_invalid_data_for_member(row + 1, _data)
                    if self.msg is not None:
                        return self.success, {}, self.msg

                # for department service call
                if self.excel_import_type == self.import_db_dict['department']:
                    if 'department_name' not in list(_data.keys()):
                        if self.auth_user_language == 'ENG':
                            return False, {}, 'Please upload correct sheet'
                        else:
                            return False, {}, 'Si prega di caricare il foglio corretto'

                    self.msg, self.success = APIValidation(

                    ).check_invalid_data_for_department(row + 1, _data)
                    if self.msg is not None:
                        return self.success, {}, self.msg

            # import sheet methods
            self.import_pool_data()
            if self.success is False:
                return self.success, {}, self.msg

            self._manage_import_response_msg()
            return self.success, {
                'new_created_ids': self.new_created_ids,
                'data_pool_list': self.data_pool_list,
                'display_alert_keyword': self.display_alert_keyword
            }, self.msg
