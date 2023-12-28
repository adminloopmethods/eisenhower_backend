import re
from datetime import datetime

from web_api_service.helpers.all_config_func import get_country_from_isd
from web_api_service.helpers.all_config_func import get_department_id_from_name
from web_api_service.helpers.all_config_func import get_member_list_instance_exists
from web_api_service.helpers.all_config_func import get_role_id_from_name
from web_api_service.helpers.all_config_func import get_status_id
from web_api_service.helpers.all_config_func import get_topic_instance
# date formatter
from web_api_service.helpers.date_format_manager import find_date_format_using_excel


# DATE_FORMAT_FOR_TIMESTAMP_CODE = "%m/%d/%Y"
DATE_FORMAT_FOR_TIMESTAMP_CODE = "%d/%m/%Y"


class APIValidation:
    """
    all api request and data validation
    """

    def __init__(self, **kwargs):
        self.regex_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        self.alpha_numeric_pattern = '^[a-zA-Z0-9]+$'
        self.custom_user_role = kwargs.get('custom_user_role', None)

    def email_validation(self, email):
        """for email_validation checker"""
        return True if (re.fullmatch(self.regex_pattern, email)) else False

    @staticmethod
    def check_name(name: str):
        return re.match(r"^[\-'a-zA-Z ]+$", name) is not None

    # @staticmethod
    def check_invalid_data_for_member(self, row, _data):
        """
        this check_invalid_data used to check all Excel sheet format details
        """
        row += 1
        if _data.get("first_name") != "Dummy":
            if not _data.get("first_name"):
                return "Error in 'first_name' field in row %s" % str(row), False

            if _data.get("first_name"):
                if self.check_name(_data["first_name"]):
                    _data["first_name"] = str(_data["first_name"])
                else:
                    return (
                        " please enter valid 'first_name' Error in 'first_name' field in row %s"
                        % str(row),
                        False,
                    )

            if not _data.get("last_name"):
                return "Error in 'last_name' field in row %s" % str(row), False

            if _data.get("last_name"):
                if self.check_name(_data["last_name"]):
                    _data["last_name"] = str(_data["last_name"])
                else:
                    return (
                        " please enter valid 'last_name' Error in 'last_name' field in row %s"
                        % str(row),
                        False,
                    )

            # @@email with regex validation
            if not _data.get("email"):
                return "Error in 'email' field in row %s" % str(row), False
            if not re.search(
                    "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$",
                    str(_data.get("email", None)),
            ):
                return "Email field not valid in row %s" % str(row), False

            # @@mobile with isd
            if not _data.get("isd"):
                return "Error in 'isd' field in row %s" % str(row), False
            if _data.get("isd"):
                country_code_instance = get_country_from_isd(_data.get("isd"))
                if not country_code_instance:
                    return (
                        "Error in 'isd' field please provide valid isd in row %s"
                        % str(row),
                        False,
                    )

            if not _data.get("mobile"):
                return "Error in 'mobile' field in row %s" % str(row), False

            if _data.get("mobile"):
                if isinstance(_data["mobile"], (float, int)):
                    _data["mobile"] = str(int(_data["mobile"]))
                else:
                    return (
                        " please enter valid Error in 'mobile' field in row %s"
                        % str(row),
                        False,
                    )

            # _data['mobile'] = str(int(_data['mobile'])) \
            #     if isinstance(_data['mobile'], (float, int)) else \
            #     str(_data['mobile'])
            # if not re.search("^[0-9]{10}$", str(_data.get('mobile', None))):
            #     return "Mobile no must be 10 digits in row %s" % str(row), False

            # @@department with check db role id
            if not _data.get("department"):
                return "Error in 'department' field in row %s" % str(row), False
            if _data.get("department"):
                print('---------------------Departments', _data.get("department"))
                _department_id = get_department_id_from_name(_data["department"])
                print('-----------------------------department_D', _department_id)
                if not _department_id:
                    return (
                        "Error in 'department' field please Provide valid department in row %s"
                        % str(row),
                        False,
                    )

            # @@role with check db role id
            if not _data.get("role"):
                return "Error in 'role' field in row %s" % str(row), False
            if _data.get("role"):
                if self.custom_user_role == 'MEMBER':
                    if _data['role'] != 'DUMMY':
                        return (
                            "Error in 'role' field please Provide valid role in row %s"
                            % str(row),
                            False,
                        )
                    # else:
                    #     _role_id = get_role_id_from_name(_data["role"])
                    #     if not _role_id:
                    #         return (
                    #             "Error in 'role' field please Provide valid role in row %s"
                    #             % str(row),
                    #             False,
                    #         )
                else:
                    _role_id = get_role_id_from_name(_data["role"])
                    if not _role_id:
                        return (
                            "Error in 'role' field please Provide valid role in row %s"
                            % str(row),
                            False,
                        )

            # if not _data.get('color'):
            #     return "Error in 'color' field in row %s" % str(row), False
            if not _data.get("access_status"):
                return "Error in 'access_status' field in row %s" % str(row), False
            if (
                    _data.get("access_status").lower() != "y"
                    and _data.get("access_status").lower() != "n"
            ):
                return "please enter valid 'Y/N' field in row %s" % str(row), False

            return None, True

        elif _data.get("first_name") == "Dummy" or _data.get("first_name") == "dummy":
            return "first_name can't be Dummy", False
        else:
            return None, True


    @staticmethod
    def check_invalid_data_for_department(row, _data):
        """
        this check_invalid_data_for_department method used
        check all validation of department
        """
        row += 1
        if (
                _data.get("department_name") != "Test"
                or _data.get("department_name") != "test"
        ):
            if not _data.get("department_name"):
                return "Error in 'department_name' field in row %s" % str(row), False
            if not _data.get("access_status"):
                return "Error in 'access_status' field in row %s" % str(row), False
            if (
                    _data.get("access_status").lower() != "y"
                    and _data.get("access_status").lower() != "n"
            ):
                return "please enter valid 'Y/N' field in row %s" % str(row), False

        return None, True

    @staticmethod
    def check_invalid_data_for_task(row, _data):
        """this check_invalid_data_for_task method used
        to check all validation of task list
        """
        row += 1
        print('print_data------------------------------------------->', _data)
        if _data.get("task_name") != "Enter name" or _data.get("task_name") != "enter name":
            if not _data.get("department"):
                return "Error in 'department' field in row %s" % str(row), False
            # check department name using id
            if _data.get("department"):
                _department_id = get_department_id_from_name(_data["department"])
                if not _department_id:
                    return (
                        "Error in 'department' field please Provide valid department in row %s"
                        % str(row),
                        False,
                    )

            if _data.get("topic_id"):
                _topic_instance = get_topic_instance({"id": _data.get("topic_id")})
                if not _topic_instance:
                    return (
                        "Error in 'topic_id' field please Provide valid topic id in row %s"
                        % str(row),
                        False,
                    )

            if not _data.get("members_id"):
                return "Error in 'members' field in row %s" % str(row), False

            if _data.get("members_id"):
                _member_list_instance_exists = get_member_list_instance_exists(
                    _data.get("members_id")
                )
                if not _member_list_instance_exists:
                    return (
                        "Error in 'members' field in please check the members ids row %s"
                        % str(row),
                        False,
                    )

            if not _data.get("task_name"):
                return "Error in 'task_name' field in row %s" % str(row), False

            # if not _data.get('description'):
            #     return "Error in 'description' field in row %s" % str(row), False
            if not _data.get("start_date"):
                return "Error in 'start_date' field in row %s" % str(row), False

            if _data.get("start_date"):
                try:
                    _data["start_date"] = datetime.fromtimestamp(
                        _data["start_date"] / 1000
                    ).strftime(DATE_FORMAT_FOR_TIMESTAMP_CODE)
                except Exception as e:
                    print("startDateTimeStampExp")
                    print(e)

                date_format = find_date_format_using_excel(_data.get("start_date"))
                if not date_format:
                    return (
                        "Error in 'start_date' field please use 'dd/mm/yyyy' date format in row %s"
                        % str(row),
                        False,
                    )

            if not _data.get("end_date"):
                return "Error in 'end_date' field in row %s" % str(row), False

            if _data.get("end_date"):
                try:
                    _data["end_date"] = datetime.fromtimestamp(
                        _data["end_date"] / 1000
                    ).strftime(DATE_FORMAT_FOR_TIMESTAMP_CODE)
                except Exception as e:
                    print("startDateTimeStampExp")
                    print(e)
                date_format = find_date_format_using_excel(_data.get("end_date"))
                if not date_format:
                    return (
                        "Error in 'end_date' field please use 'dd/mm/yyyy' date format in row %s"
                        % str(row),
                        False,
                    )
            try:
                if _data.get("start_date") and _data.get("end_date"):
                    if _data.get("end_date") < _data.get("start_date"):
                        return "End_date should be greater than start_date", False
            except Exception as e:
                print("enderStartEndErr")
                print(e)
            if _data.get("reminder") is None:
                _data['reminder'] = None

            if _data.get("reminder"):
                try:
                    _data["reminder"] = datetime.fromtimestamp(
                        _data["reminder"] / 1000
                    ).strftime(DATE_FORMAT_FOR_TIMESTAMP_CODE)
                except Exception as e:
                    print("reminderDateTimeStampExp")
                    print(e)
                try:
                    date_format = find_date_format_using_excel(_data.get("reminder"))
                    if not date_format:
                        return (
                            "Error in 'reminder' field please use 'dd/mm/yyyy' date format in row %s"
                            % str(row),
                            False,
                        )
                except Exception as e:
                    print("reminderExpErr")
                    print(e)

            print('rrrrrrrrrrrrrrrrrr----------------------->', _data)

            if not _data.get("status_id"):
                return "Error in 'status' field in row %s" % str(row), False

            if _data.get("status_id"):
                _status_id = get_status_id(_data.get("status_id"))
                if not _status_id:
                    return (
                        "Error in 'status_id' field please Provide valid status id in row %s"
                        % str(row),
                        False,
                    )
            if not _data.get("importance"):
                return "Error in 'importance' field in row %s" % str(row), False

            if _data.get("importance"):
                if _data.get("importance").title() not in ["High", "Low", "Medium"]:
                    return (
                        "Error in 'importance' field please update valid keyword in row %s"
                        % str(row),
                        False,
                    )

            if not _data.get("urgency"):
                return "Error in 'urgency' field in row %s" % str(row), False

            if _data.get("urgency"):
                if _data.get("urgency").title() not in ["High", "Low", "Medium"]:
                    return (
                        "Error in 'urgency' field please update valid keyword in row %s"
                        % str(row),
                        False,
                    )

            return None, True
            # if not _data.get('reminder'):
            #     return "Error in 'reminder' field in row %s" % str(row), False
        # else:

        elif _data.get("task_name") == "Enter name" or _data.get("task_name") == "enter name":
            return "this is sample sheet, please update the data", False
        else:
            return None, True
