import json

import requests

from duende.settings.development import PROJECT_BASE_URL


class TPAPIService:
    """
    APIConsumeService
    this class module used to call apis using request and get the response
    """

    def __init__(self, **kwargs):
        self.project_base_url = kwargs.get('base_url', PROJECT_BASE_URL)
        self.final_url_path = ''  # API Full path with base url
        self.api_url_path = kwargs.get('api_url_path', None)  # API Core Path
        # API method (GET/POST/PUT)
        self.api_method = kwargs.get('api_method', None)
        self.api_post_data = kwargs.get('api_post_data', None)  #
        self.api_form_data = kwargs.get('api_form_data', None)  # for multipart
        self.files = kwargs.get('files', None)  # for media file
        self.query_param_or_id = kwargs.get('query_param_or_id', None)  # check query parameter or id
        # header value (content-type and token)
        self.headers = kwargs.get('headers', None)
        self.payload = kwargs.get('payload', None)

    def generate_api_url_path(self):
        """
        generate_api_url_path
        this methods used to manage and create full api url path for consuming the api
        """
        self.final_url_path = ''.join([self.project_base_url, self.api_url_path])

    def __call__(self):
        self.generate_api_url_path()  # Generate the api url Path
        return self.call_all_api()  # all api response call

    def get_method_call(self):
        """
        api_get_method_call
        in this methods we used to 3 parameter for get the every api response
        param: used for query params like search value and data visibility
        id: used for passing a id in url for get the particular id or data records
        simple_else: direct hit simple url for get the json data
        """
        # for query params (search & filter)
        if self.query_param_or_id == 'param':
            _response = requests.get(
                self.final_url_path, params=self.api_post_data
            )
            if _response.status_code == 200:
                return _response.json()
            return None
        # for add id and single value
        elif self.query_param_or_id == 'id':
            _response = requests.get(
                self.final_url_path + self.api_post_data['id'] + '/', headers=self.headers
            )
            if _response.status_code == 200:
                return _response.json()
            return None
        # simple_else for normal url hit
        else:
            _response = requests.get(
                self.final_url_path, headers=self.headers
            )
            if _response.status_code == 200:
                return _response.json()
            return None

    def post_method_call(self):
        """
        api_post_method_call
        this methods used to call post request api for request user
        """
        _response = requests.post(
            self.final_url_path,
            data=json.dumps(self.api_post_data),
            headers=self.headers
        )
        if _response.status_code == 200:
            return _response.json()
        return None

    def multipart_post_method_call(self):
        """
        api_post_method_call
        this methods used to call post request api for request user
        """
        _response = requests.post(
            self.final_url_path,
            headers=self.headers,
            files=self.files,
            data=self.api_form_data,
            # data=self.payload
        )
        return _response

    def put_method_call(self):
        """
        api_put_method_call
        this methods used to call put request api for request user
        """
        _response = requests.put(
            self.final_url_path,
            data=json.dumps(self.api_post_data),
            headers=self.headers
        )
        if _response.status_code == 200:
            return _response.json()
        return None

    def call_all_api(self):
        """
        call_all_api
        this methods call all types of apis for get the api response data
        GET, POST, PUT
        """
        if self.api_method == "__GET__":
            return self.get_method_call()
        if self.api_method == "__POST__":
            return self.post_method_call()
        if self.api_method == "__PUT__":
            return self.put_method_call()
        if self.api_method == "__MULTIPART__":
            return self.multipart_post_method_call()
