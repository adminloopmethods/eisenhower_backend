import requests

# import business card models
from cards.models import BusinessCardReaderManager, BusinessExpenseManager
from core.third_party_consume_service import TPAPIService


#  import serializers


class AbbyOcrReader:
    """
    AbbyOcrReader
    """

    def __init__(self, **kwargs):
        self.auth_user_instance = kwargs.get("auth_user_instance", None)
        self.abby_base_url = "https://abbyyrest.gruppodr.it/api/ocr/"
        self.business_image = kwargs.get("business_image")
        self.application_type = kwargs.get("application_type", None)
        self.service_function = kwargs.get("service_function", None)
        self.data_set_type = kwargs.get("data_set_type", None)
        self.business_image_name = kwargs.get("business_image_name", None)
        self.abby_response_msg = dict(
            success="OK",
            internal_server_error="Corrupted file / file with viruses.",
            processable_entity="Missing file.",
            unauthorized="Invalid/expired bearer token.",
        )
        self.content_type_dict = {"Content-Type": "image/png"}
        self.abby_response_id = kwargs.get("abby_response_id", None)
        self.business_card_id = kwargs.get("business_card_id", None)
        self.abby_response = None
        self.business_expense_id = kwargs.get("business_expense_id", None)

    def handle_uploaded_file(self, f):
        for x in f:
            if x.startswith("newick;"):
                print("")
        return cutFile(x)

    def upload_business_card(self):
        """this upload_business_card method used to upload
        the business card img from abby to detect the text processing service

        expected str, bytes or os.PathLike object, not InMemoryUploadedFile
        expected str, bytes or os.PathLike object, not InMemoryUploadedFile

        """
        # third party api consume services
        _bearer_token_cognito = "".join(
            [
                "Bearer ",
                str(self.auth_user_instance.user_auth.cognito_access_token)
            ]
        )

        url = "https://abbyyrest.gruppodr.it/api/ocr/submit"
        file_obj = open(self.business_image, "rb")
        files = {"file": file_obj}
        form_data = {
            "application": "BCM",
            "function": "recognition",
            "dataSetType": "",
            # "file": file_obj,
        }
        headers = {"Authorization": _bearer_token_cognito}
        response = requests.post(
            url,
            files=files, data=form_data, headers=headers,
            verify=False
        )
        print("#############", response.status_code)

        # for success response
        if response.status_code == 200:
            print(response.json())
            self.abby_response = response.json()
            try:
                BusinessCardReaderManager.objects.filter(
                    id=self.business_card_id
                ).update(
                    abby_response_id=self.abby_response["id"],
                    retrive_status="initiate"
                )
            except Exception as e:
                print("UpdateAbbyIdExceptionErr")
                print(e)
            return self.abby_response, self.abby_response_msg["success"]
        # for un authorized if token not passed or token expired issue
        if response.status_code == 401:
            try:
                BusinessCardReaderManager.objects.filter(
                    id=self.business_card_id
                ).update(
                    retrive_status="failed",
                    reason_for_failed=self.abby_response_msg["unauthorized"]
                )
            except Exception as e:
                print("unauthorizedExceptionErr")
                print(e)
            return None, self.abby_response_msg["unauthorized"]
        # for image not processing image or media file not found in request
        if response.status_code == 422:
            try:
                BusinessCardReaderManager.objects.filter(
                    id=self.business_card_id
                ).update(
                    retrive_status="failed",
                    reason_for_failed=self.abby_response_msg[
                        "processable_entity"
                    ]
                )
            except Exception as e:
                print("processableEntityExceptionErr")
                print(e)
            return None, self.abby_response_msg["processable_entity"]
        #  som issue from server side
        if response.status_code == 500:
            try:
                BusinessCardReaderManager.objects.filter(
                    id=self.business_card_id
                ).update(
                    retrive_status="failed",
                    reason_for_failed=self.abby_response_msg[
                        "internal_server_error"
                    ]
                )
            except Exception as e:
                print("internalServerErrorExceptionErr")
                print(e)
            return None, self.abby_response_msg["internal_server_error"]

    def upload_business_expense(self):
        """this upload_business_card method used to upload
        the business card img from abby to detect the text processing service

        expected str, bytes or os.PathLike object, not InMemoryUploadedFile
        expected str, bytes or os.PathLike object, not InMemoryUploadedFile

        """
        # third party api consume services
        _bearer_token_cognito = "".join(
            [
                "Bearer ", 
                str(self.auth_user_instance.user_auth.cognito_access_token)
            ]
        )

        url = "https://abbyyrest.gruppodr.it/api/ocr/submit"
        file_obj = open(self.business_image, "rb")

        print("file:     ", file_obj)
        print("fileType:   ", type(file_obj))

        files = {"file": file_obj}
        form_data = {
            "application": "BEM",
            "function": "recognition",
            "dataSetType": "",
            # "file": file_obj,
        }
        headers = {"Authorization": _bearer_token_cognito}
        response = requests.post(
            url,
            files=files, data=form_data, headers=headers,
            verify=False
        )
        print("#############", response.status_code)
        # for success response
        if response.status_code == 200:
            print(response.json(), 'uuuuuuuuuuuuuuuuuuuuuuuuuuuu')
            self.abby_response = response.json()
            try:
                BusinessExpenseManager.objects.filter(
                    id=self.business_expense_id
                ).update(
                    abby_response_id=self.abby_response["id"],
                    retrive_status="initiate"
                )
            except Exception as e:
                print("UpdateAbbyIdExceptionErr")
                print(e)
            return response.json(), self.abby_response_msg["success"]
        # for un authorized if token not passed or token expired issue
        if response.status_code == 401:
            try:
                BusinessExpenseManager.objects.filter(
                    id=self.business_expense_id
                ).update(
                    retrive_status="failed",
                    reason_for_failed=self.abby_response_msg["unauthorized"]
                )
            except Exception as e:
                print("UpdateAbbyIdExceptionErr")
                print(e)
            return None, self.abby_response_msg["unauthorized"]
        # for image not Processing image or media file not found in request
        if response.status_code == 422:
            try:
                BusinessExpenseManager.objects.filter(
                    id=self.business_expense_id
                ).update(
                    retrive_status="failed",
                    reason_for_failed=self.abby_response_msg[
                        "processable_entity"
                    ]
                )
            except Exception as e:
                print("UpdateAbbyIdExceptionErr")
                print(e)
            return None, self.abby_response_msg["processable_entity"]
        #  som issue from server side
        if response.status_code == 500:
            try:
                BusinessExpenseManager.objects.filter(
                    id=self.business_expense_id
                ).update(
                    retrive_status="failed",
                    reason_for_failed=self.abby_response_msg[
                        "internal_server_error"
                    ]
                )
            except Exception as e:
                print("UpdateAbbyIdExceptionErr")
                print(e)
            return None, self.abby_response_msg["internal_server_error"]

    def test_upload_file_local(self, test_upload_data):
        """in this method test_upload_file_local call the media file
        for testing purpose
        /api/v1/user/detail/update/
        """
        print("!!!!!!!!!test_upload_data", test_upload_data["business_image"])

        file = test_upload_data["business_image"]
        print("filepathsssssss", dir(file))
        # print('fileFile', open(file, 'rb'))

        # load_file = FileSystemStorage()
        # filename = load_file.save(file.name, file)  # saving in local directory and getting filename
        # data = {}
        # fr_data = None
        # with open(filepath ,'rb') as fr:
        #     fr_data += fr.read()
        # url = 'http://127.0.0.1:8000/api/'
        # response = requests.post(url=url, data=data, files= {
        #                           'filefiledname': fr_data
        #                           }
        #                          )
        print(open(file, "rb"))

        third_party_request_params = dict(
            base_url="http://192.168.1.23:7777",
            api_url_path="/api/v1/business/card/test/upload/",
            api_method="__MULTIPART__",
            headers={
                # 'Authorization': _bearer_token_cognito,
                "Content-Type": "multipart/form-data; boundary=<calculated when request is sent>",
            },
            files={"file": open(file, "rb")},
            api_form_data={
                "test_file": open(file, "rb")
            },
            # payload=payload
        )
        third_party_api_instance = TPAPIService(**third_party_request_params)
        test_multipart_response = third_party_api_instance()

        print("test_multipart_response", test_multipart_response)
        print("test_multipart_json_response", test_multipart_response.json())

    @staticmethod
    def firebase_configuration():
        """in this firebase_configuration method used to setup
        configure the abby ocr service
        """
        try:
            import firebase_admin
            from firebase_admin import credentials
        except ImportError:
            print('ImportError')

        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

    def abby_retrieve_call(self):
        """
        this abby_retrieve_call method used to call the abby retrive function
        bcm_abby_response_data: {
            "lastName": null,
            "country": null,
            "city": null,
            "telephoneMobile": null,
            "companyName": null,
            "postalCode": null,
            "facebook": null,
            "title": null,
            "telephoneOffice": null,
            "eMail": null,
            "firstName": null,
            "province": null,
            "web": null,
            "street": null,
            "nomeBatch": "e99b5f96-de02-4bbe-971d-7fe1d43bf61f",
            "fax": null
        }
        """
        # third party api consume services
        _bearer_token_cognito = "".join(
            [
                "Bearer ",
                str(self.auth_user_instance.user_auth.cognito_access_token)
            ]
        )

        url = "".join(
            [
                "https://abbyyrest.gruppodr.it/api/ocr/retrieve?id=",
                self.abby_response_id,
            ]
        )

        headers = {"Authorization": _bearer_token_cognito}
        response = requests.get(url, headers=headers, verify=False)
        print("############# success_code", response.status_code)

        if response.status_code == 200:
            print('$$$$$$$$$$$$$$$$$$$$$$$$$ ABBY RESPONSE JSON', response.json())
            print(response.json())
            return response.json(), self.abby_response_msg["success"]
        if response.status_code == 401:
            return None, self.abby_response_msg["unauthorized"]
        if response.status_code == 422:
            return None, self.abby_response_msg["processable_entity"]
        if response.status_code == 500:
            return None, self.abby_response_msg["internal_server_error"]
        if response.status_code == 425:
            return response.status_code, None
