"""
API RESPONSE PARSER
"""
from core.messages import API_RESPONSE_MSG, MSG

from rest_framework import status
from rest_framework.response import Response


class APIResponseParser:
    """
    ApiResponseParser
    Common api Response Parser for all API Response.
    """

    def __init__(self):
        pass

    @staticmethod
    def response(**_api_resp_data):
        """
        kwargs: all Kwargs Parameter comes from to APIView Class.
        return: Response
        """
        try:
            if not _api_resp_data['success']:
                return Response(
                    {
                        'message': _api_resp_data['message'], 'success': False,
                        'data': [], 'errors': _api_resp_data.get('errors', [])
                    },
                    status=_api_resp_data.get(
                        'status_code', status.HTTP_302_FOUND)
                )
            if _api_resp_data['success']:
                return Response(
                    {
                        _api_resp_data['keyname']: _api_resp_data['data'],
                        'success': _api_resp_data['success'],
                        'message': _api_resp_data.get('message', 'DONE')
                    },
                    status=_api_resp_data.get('status_code')
                )
        except Exception as msg:
            return Response(
                {
                    'message': "APIResponseParser.response.errors", 'errors': [str(msg)], 'success': False
                },
                status=_api_resp_data.get('status_code', status.HTTP_302_FOUND)
            )

    @staticmethod
    def responses(**_api_resp_data):
        """
        responses: response_with_status
        This response_with_status() methods used to get and create the response with status
        code api structure data
        kwargs: all Kwargs Parameter comes from to APIView Class.
        return: Response
        """
        response = {}
        try:
            if _api_resp_data.get('success', True):
                for key, values in _api_resp_data['data'].items():
                    response[key] = values
                response['message'] = _api_resp_data.get('message', 'DONE')
                response['success'] = _api_resp_data.get('success', True)
                response['errors'] = _api_resp_data.get('errors', [])
                return Response(
                    response,
                    status=_api_resp_data.get('status_code')
                )
            if not _api_resp_data['success']:
                return Response(
                    {
                        'success': False,
                        'message': _api_resp_data.get('message', 'ERRORs'),
                        'errors': _api_resp_data.get('errors', []),
                        'data': _api_resp_data.get('data', {})
                    },
                    status=_api_resp_data.get(
                        'status_code', status.HTTP_302_FOUND)
                )
        except Exception as msg:
            return Response(
                {
                    'message': "APIResponseParser.response.errors",
                    'errors': [str(msg)],
                    'success': False
                },
                status=_api_resp_data.get('status_code', status.HTTP_302_FOUND)
            )


# as a response templates
def final_response():
    """this final_response function used to return final response 
    for reuse code and avoid for duplicate code 
    """
    return {
        'success': True,
        'message': MSG['DONE'],
        'keyname': 'data',
        'data': [],
        'status_code': status.HTTP_201_CREATED
    }


def final_response_ok():
    """this final_response function used to return final response
    for reuse code and avoid for duplicate code
    """
    return {
        'success': True,
        'message': MSG['DONE'],
        'keyname': 'data',
        'data': [],
        'status_code': status.HTTP_200_OK
    }


def not_acceptable_response():
    """this not_acceptable_response function used to return not accetable 
    alert response for reuse code and avoid for duplicate code 
    """
    return {
        'success': False,
        'message': MSG['No_ACTIVE_DATA'],
        'status_code': status.HTTP_406_NOT_ACCEPTABLE
    }


def bad_request_response():
    """this bad_request_response function used to return not accetable 
    alert response for reuse code and avoid for duplicate code 
    """
    return {
        'success': False,
        'message': MSG['ERRORS'],
        'errors': [],
        'status_code': status.HTTP_400_BAD_REQUEST
    }


def request_not_found():
    """request not found message data for common request errors codes"""
    return dict(success=False,
                message=API_RESPONSE_MSG['REQUEST_NOT_FOUND'],
                status_code=status.HTTP_400_BAD_REQUEST)
