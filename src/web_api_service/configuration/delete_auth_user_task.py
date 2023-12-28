# import customuser
from user.models import CustomUsers

# from django.contrib.auth.models import User
from account.models import User


from task_management.models import Tasks


def delete_auth_user_from_department_id(department_id):
    """this collect_auth_user_id method used to collect the auth user id
    """
    print('department_idssssssssssssssss', department_id)
    auth_user_ids = CustomUsers.objects.filter(
        department_id=department_id
    ).values_list('auth_user_id', flat=True)
    # custom_user_ids = CustomUsers.objects.filter(department_id=department_id).values_list('id', flat=True)
    # task_qs = Tasks.objects.filter(members__in=custom_user_ids)
    # print('taaaaatask_qs', task_qs)
    try:
        if User.objects.filter(id__in=list(auth_user_ids)).delete():
            print('deleteAuthUSer00000000000000000')
            print(True)
            return True
        else:
            return False
    except Exception as e:
        print('------------------DepartmentUserDeleteExpetion')
        return None
        print(e)


def delete_auth_user_frsom_department_id(auth_user_ids):
    """this delete_auth_user_from_department_id method used to delete the auth user with the help 
    of department id
    """
    pass
    # User.objects.filter(id__in=auth_user_ids).delete()