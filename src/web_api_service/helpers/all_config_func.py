from task_management.models import Tasks
from user.models import CustomUsers, UserStickyNotes

# import user config
from configuration.models import Departments
from configuration.models import Topics
from configuration.models import TaskStatusMaster
from configuration.models import UserRoleMaster
from configuration.models import Language

from location.models import CountryMaster

from cards.models import CategoryGroupMaster


def get_user_instance(query_filter_params):
    """this get_user_instance method used to 
    get user instance using filter params variables
    params: query_filter_params
    return: class_object_instance
    """
    try:
        return CustomUsers.objects.get(**query_filter_params)
    except Exception as e:
        print('@get_user_instance.G12')
        print(e)
        return None


def get_task_instance(query_filter_params):
    """this get_task_instance method used to 
    get task instance using filter params variables
    params: query_filter_params
    return: class_object_instance
    """
    try:
        return Tasks.objects.get(**query_filter_params)
    except Exception as e:
        print('@get_user_instance.G12')
        print(e)
        return None


def already_exist_check(query_filter_params):
    """
    this already_exist_check method used 
    to check credentials already exist in db or not
    params: query_filter_params
    return: class_object_instance
    """
    try:
        return CustomUsers.objects.filter(**query_filter_params).exists()
    except Exception as e:
        print('@already_exist_check.G26')
        print(e)
        return None


def already_exist_check_for_department(department, access_status):
    """
    this already_exist_check method used 
    to check credentials already exist in db or not
    params: department
    return: department
    """
    try:
        return Departments.objects.filter(department_name=department,
                                          access_status=access_status).exists()
    except Exception as e:
        print('@already_exist_check_for_department.G26')
        print(e)
        return None


def get_department_instance(query_filter_params):
    """
    this department_id_exists method used 
    to check department id is exist or not
    params:
    return: department
    """
    try:
        # print()
        return Departments.objects.get(**query_filter_params)
    except Exception as e:
        print('@department_instance.G26')
        print(e)
        return None


def already_exist_check_for_topic(topic, access_status):
    """
    this already_exist_check method used 
    to check credentials already exist in db or not
    params: topic
    return: topic
    """
    try:
        return Topics.objects.filter(
            topic_name=topic,
            access_status=access_status).exists()
    except Exception as e:
        print('@already_exist_check_for_topic.G26')
        print(e)
        return None


def get_topic_instance(query_filter_params):
    """
    this get_topic_instance method used 
    to check department id is exists or not
    params:
    return: department
    """
    try:
        return Topics.objects.get(**query_filter_params)
    except Exception as e:
        print('@topics_instance.G26')
        print(e)
        return None


def get_user_level_instance(query_filter_params):
    """
    this get_user_level_instance method used 
    to check department id is exists or not
    params:
    return: department
    """
    try:
        return UserRoleMaster.objects.get(**query_filter_params)
    except Exception as e:
        print('@topics_instance.G26')
        print(e)
        return None


def get_status_instance(query_filter_params):
    """
    this get_topic_instance method used to check department id is exists or not
    params:
    return: department
    """
    try:
        return TaskStatusMaster.objects.get(**query_filter_params)
    except Exception as e:
        print('@topics_instance.G26')
        print(e)
        return None


def get_user_sticky_notes_instance(query_filter_params):
    """get_user_sticky_notes_instance
    """
    try:
        return UserStickyNotes.objects.filter(**query_filter_params)
    except Exception as e:
        print('UserStickyNotes.DoesNotExist: %s' % e)
        return None


def get_department_id_from_name(department_name):
    """
    this get_department_id_from_name method used 
    to get the department id using department name
    """
    try:
        department_instance = Departments.objects.filter(
            department_name__exact=department_name
        ).last()
        return department_instance.id if department_instance else None

    except Exception as e:
        print('Departments.DoesNotExit')
        print(e)
        return None


def get_topic_id_from_name(department_name):
    """
    this get_department_id_from_name method used 
    to get the department id using department name
    """
    try:
        department_instance = Topics.objects.filter(
            department_name=department_name.capitalize()
        ).last()
        return department_instance.id if department_instance else None

    except Exception as e:
        print('Departments.DoesNotExit')
        print(e)
        return None


def get_status_id(status_id):
    """
    this get_department_id_from_name method used 
    to get the department id using department name
    """
    try:
        status_instance = TaskStatusMaster.objects.filter(id=status_id).last()
        return status_instance.id if status_instance else None
    except Exception as e:
        print('Departments.DoesNotExit')
        print(e)
        return None


def get_role_id_from_name(role_name):
    """
    this get_role_id_from_name method used to 
    get the role id using role instance
    """
    try:
        role_instance = UserRoleMaster.objects.filter(
            role_name=role_name.title()
        ).last()
        return role_instance.id if role_instance else None
    except Exception as e:
        print('UserRoleMaster.DoesNotExit')
        print(e)
        return None


def custom_user_id(auth_user_id):
    """
    custom_user_id
    """
    try:
        return CustomUsers.objects.filter(auth_user=auth_user_id).last().id
    except Exception as e:
        print(e)


def get_language_uuid(language_code):
    """
    custom_user_id
    """
    try:
        return Language.objects.filter(language_code=language_code).last().id
    except Exception as e:
        print(e)


def get_country_from_isd(isd):
    """get_country_from_isd
    """
    try:
        return CountryMaster.objects.filter(isd=int(isd)).last()
    except Exception as e:
        print(e)


def get_auth_instance_from_user_id(custom_user):
    """get_auth_instance_from_user_id
    """
    custom_user_instance = CustomUsers.objects.filter(id=custom_user).last()
    return custom_user_instance.auth_user


def get_category_group_id(category_group_name):
    """
    this get_category_group_id get name from id
    """
    try:
        return CategoryGroupMaster.objects.get(category_name__icontains=category_group_name).id
    except CategoryGroupMaster.DoesNotExist:
        print('CategoryGroupMasterErr')
        return None


# def get_category_group_id(category_group_name):
#     """
#     this get_category_group_id get name from id
#     """
#     try:
#         return CategoryGroupMaster.objects.get(category_name__icontains=category_group_name).id
#     except Exception as e:
#         return None
#         print('CategoryGroupMasterErr')
#         print(e)


def get_member_details_using_member_id(member_id):
    """
    get member details id
    """
    custom_user_obj = CustomUsers.objects.filter(id=member_id).last()
    return {'full_name': ''.join([str(custom_user_obj.first_name), ' ', str(custom_user_obj.last_name)])}


def get_member_list_instance_exists(member_ids):
    """this get_member_list_instance get the instance of member list using the members list ids
    :param member_ids: all members ids
    :return: instance_obj
    """
    try:
        try:
            member_id_list = str(member_ids).split(',')
        except TypeError:
            member_id_list = []
        member_list_exist_instance = CustomUsers.objects.filter(
            id__in=member_id_list
        )
    except Exception as e:
        member_list_exist_instance = None
        print('CustomUser.DoesNotExist')
        print(e)

    return member_list_exist_instance
