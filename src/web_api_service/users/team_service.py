from core.api_response_parser import bad_request_response
from core.api_response_parser import final_response_ok
from core.api_response_parser import not_acceptable_response
from core.constants import ACCESS_STATUS
from core.custom_serializer_error import SerializerErrorParser
from core.messages import MSG
from core.serializer_getter import SerializerManipulationService
from user.models import CustomUsers
from user.models import UserMemberMapping
from user.models import Team
from web_api_service.helpers.all_config_func import get_user_instance
# import instance methods
from web_api_service.helpers.all_config_func import get_user_sticky_notes_instance
from web_api_service.users.member_service import UserMemberService
# import member serializers
from web_api_service.users.serializers import CreateTeamSerializer
from web_api_service.users.serializers import GetMemberDetailSerializer
from web_api_service.users.serializers import MemberSerializer
from web_api_service.users.serializers import TeamDetailSerializer
from web_api_service.users.serializers import TeamMemberSerializer
from web_api_service.users.serializers import UserStickyNotesSerializer


class TeamService:
    """
    all ConfigService
    create_topic_detail
    """

    def __init__(self, **kwargs):
        self.department_master_data = []
        self.auth_instance = kwargs.get('auth_instance', None)
        self.team_req_data = kwargs.get('team_req_data', None)
        self.department_id_list = []
        self.user_id_list = []
        self.final_response = final_response_ok()
        self.not_acceptable_response = not_acceptable_response()
        self.bad_request_response = bad_request_response()
        self.topic_master_data = []
        self.member_user_data = []
        self.query_params = kwargs.get('query_params', None)

    def not_acceptable_with_serializer_error_parser(self, serializer_errors):
        """
        not_acceptable_with_serializer_error_parser
        """
        _serializer_error_instance = SerializerErrorParser(serializer_errors)
        key_name, error = _serializer_error_instance()
        self.not_acceptable_response['message'] = ''.join([str(key_name), str(error)])
        return self.not_acceptable_response

    def team_detail_list(self):
        """
        this team_detail_list get the all team listing details
        """
        team_instance = Team.objects.filter(
            access_status=ACCESS_STATUS[0][0],
            user=self.auth_instance.user_auth
        )
        if not team_instance:
            self.not_acceptable_response['message'] = MSG['No_ACTIVE_DATA']
            return self.not_acceptable_response

        team_serializer = TeamDetailSerializer(team_instance, many=True)
        if not team_serializer:
            return self.not_acceptable_with_serializer_error_parser(team_serializer.errors)

        self.final_response['data'] = team_serializer.data
        return self.final_response

    def create_team_detail(self):
        """
        this create_team_detail method used to create team with add member with the system
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        self.team_req_data['user'] = self.auth_instance.user_auth.id
        self.team_req_data['access_status'] = ACCESS_STATUS[0][0]
        team_serializer = CreateTeamSerializer(data=self.team_req_data)
        if team_serializer.is_valid(raise_exception=True):
            team_serializer.save()
            self.final_response['data'] = team_serializer.data
            return self.final_response
        else:
            return self.not_acceptable_with_serializer_error_parser(
                team_serializer.errors)

    def team_activate_deactivate(self):
        """
        this team_activate_deactivate method used to activate and deactivate the team status
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        try:
            Team.objects.get(id=self.query_params.get('team_id'))
        except Exception as e:
            print('#G101-team.exception')
            print(e)
            self.bad_request_response['errors'] = [
                {'team_id': MSG.get('TEAM_NOT_EXISTS')}
            ]
            self.bad_request_response['message'] = MSG.get('TEAM_NOT_EXISTS')
            return self.bad_request_response

        if Team.objects.filter(
                id=self.query_params.get('team_id')
        ).update(is_active=self.query_params.get('is_active')):
            self.final_response['data'] = {'is_active': self.query_params.get('is_active')}
            return self.final_response
        else:
            self.not_acceptable_response['message'] = MSG['No_ACTIVE_DATA']
            return self.not_acceptable_response

    def team_members(self):
        """
        this team_members method used to get all team related members
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        team_instance = Team.objects.filter(
            access_status=ACCESS_STATUS[0][0],
            user=self.auth_instance.user_auth
        ).last()
        if not team_instance:
            self.not_acceptable_response['message'] = MSG.get('TEAM_NOT_EXISTS')
            return self.not_acceptable_response

        team_member_serializer = TeamMemberSerializer(team_instance)
        if team_member_serializer:
            self.final_response['data'] = team_member_serializer.data['members']
            return self.final_response
        else:
            return self.not_acceptable_with_serializer_error_parser(team_member_serializer.errors)

    def team_member_details(self):
        """
        this team_member_details method used to get team member details using id
        """
        user_instance = get_user_instance(
            {'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response
        try:
            member_instance = CustomUsers.objects.get(id=self.query_params.get('member_id'))
        except Exception as e:
            print('#G157')
            print(e)
            self.bad_request_response['errors'] = [
                {'member_id': MSG['MEMBER_NOT_FOUND']}
            ]
            self.bad_request_response['message'] = MSG['MEMBER_NOT_FOUND']
            return self.bad_request_response

        member_detail_serializer = GetMemberDetailSerializer(
            member_instance,
            context={'user_instance': user_instance}
        )
        if not member_detail_serializer:
            return self.not_acceptable_with_serializer_error_parser(member_detail_serializer.errors)
        self.final_response['data'] = member_detail_serializer.data
        return self.final_response

    def _manage_related_fields_from_name(self):
        """this manage_related_fields_from_name method used to manage all related fields from name
        """
        # for department alias id 
        # _department = self.team_req_data.get('department', None)
        # if _department:
        #     _department_instance = get_department_instance({'department_name': _department})
        #     if _department_instance:
        #         self.team_req_data['department'] = _department_instance.id

        # # for user level alias id 
        # _level = self.team_req_data.get('level', None)
        # if _level:
        #     _user_level_instance = get_user_level_instance({'role_name': _level})
        #     if _user_level_instance:
        #         self.team_req_data['role'] = _user_level_instance.id

        _level = self.team_req_data.get('level', None)
        if _level:
            self.team_req_data['role'] = self.team_req_data.get('level', None)

        _access_status = self.team_req_data.get('access_status', None)
        if _access_status:
            if 'Y' != _access_status and 'N' != _access_status:
                self.bad_request_response['message'] = MSG.get('VALID_CHOICE')
                return self.bad_request_response
            self.team_req_data['access_status'] = (ACCESS_STATUS[0][0]
                                                   if _access_status == 'Y' else
                                                   ACCESS_STATUS[1][0])

    def update_member_remove_mapping(self, member_id):
        """this update_member_remove_mapping method used to update the member 
        removing object from backend
        """
        user_member_obj = UserMemberMapping.objects.filter(user=self.auth_instance.user_auth).first()
        user_member_obj.members.remove(member_id)


    def update_team_member(self):
        """this  update_team_member used to update the member user 
        using partial true serializers
        """
        user_instance = get_user_instance({'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        member_instance = get_user_instance(dict(id=self.team_req_data.get('member_id')))
        if not member_instance:
            self.bad_request_response['message'] = MSG['MEMBER_DOES_NOT_EXIST']
            return self.bad_request_response

        self._manage_related_fields_from_name()
        serializer_instance = SerializerManipulationService(
            model_instance=member_instance,
            serializer_class=MemberSerializer,
            request_data=self.team_req_data,
            type='__update__')
        serializer_data = serializer_instance()
        if not serializer_data:
            self.not_acceptable_response['message'] = MSG['No_ACTIVE_DATA']
            return self.not_acceptable_response

        if (self.team_req_data['access_status'] == 'N' 
                or self.team_req_data['access_status'] == 'self_only'):
            return UserMemberService(auth_instance=self.auth_instance).assign_user_mapping(serializer_data)

        try:
            self.update_member_remove_mapping(self.team_req_data.get('member_id'))
        except Exception as e:
            print('updateMemberMappingExpErr')
            print(e)

        return self.final_response

    def update_sticky_note(self):
        """this  update_sticky_notes used to update the sticky notes with the latest update text"""
        user_instance = get_user_instance(
            {'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        sticky_note_instance = get_user_sticky_notes_instance({'user': self.auth_instance.user_auth})
        if sticky_note_instance:
            sticky_note_serializer = UserStickyNotesSerializer(sticky_note_instance.last(),
                                                               data=self.team_req_data,
                                                               partial=True)
        else:
            self.team_req_data['user'] = self.auth_instance.user_auth.id
            sticky_note_serializer = UserStickyNotesSerializer(data=self.team_req_data)

        if sticky_note_serializer.is_valid():
            sticky_note_serializer.save()
            self.final_response['data'] = sticky_note_serializer.data
            return self.final_response
        else:
            self.not_acceptable_response['message'] = str(sticky_note_serializer.errors)
            return self.not_acceptable_response

    def get_sticky_note(self):
        """this get_sticky_note method used to get the sticky notes using serializer
        """
        user_instance = get_user_instance(
            {'is_active': True, 'auth_user': self.auth_instance})
        if not user_instance:
            self.bad_request_response['message'] = MSG['USER_NOT_FOUND']
            return self.bad_request_response

        sticky_note_instance = get_user_sticky_notes_instance(
            {'user': self.auth_instance.user_auth}).last()
        if sticky_note_instance:
            self.final_response['data'] = UserStickyNotesSerializer(sticky_note_instance).data
            return self.final_response
        else:
            self.not_acceptable_response['message'] = MSG.get('No_ACTIVE_DATA')
            return self.not_acceptable_response
