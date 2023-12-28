# import business card models


import requests

from cards.models import BusinessCardReaderManager


# import


#  import serializers


def cut_file(f):
    output = " "
    for chunk in f.chunks():
        output += chunk.decode("ascii")
    return output.replace("\n", "").replace("\r", "")


def handle_uploaded_file(f):
    for x in f:
        if x.startswith("newick;"):
            print("")
    return cut_file(x)


class BusinessCardUpload:
    """
    BusinessCardReader
    """

    def __init__(self, **kwargs):
        self.auth_user_instance = kwargs.get("auth_user_instance", None)
        self.business_card_data = kwargs.get("business_card_data", {})

        # for abby service attrs
        self.data_set_type = ""
        self.service_function = "recognition"
        self.application_type = "BCM"
        self._user_category_value_list = []

        # abby base url
        self.abby_base_url = "https://abbyyrest.gruppodr.it/api/ocr/"

        # sub url of api endpoints
        self.submit = "submit"

    def upload_business_card(self):
        """this upload_business_card method used to upload
        the business card image in bcr db
        """

        business_card_create = BusinessCardReaderManager.objects.create(
            business_image=self.business_card_data["business_image"],
            retrive_status="initiate",
            user_id=self.auth_user_instance.user_auth.id,
        )
        if not business_card_create:
            return None

        # third party api consume services
        _bearer_token_cognito = "".join(
            ["bearer ", str(self.auth_user_instance.user_auth.cognito_access_token)]
        )

        url = "".join([self.abby_base_url, self.submit])
        # print('business_card_data', self.business_card_data['business_image'].read())
        files = {"file": open(business_card_create.business_image.path, "rb")}
        # files = handle_uploaded_file(self.business_card_data['business_image'].read())
        print("filesss", files)

        abby_response = requests.post(
            url,
            files=files,
            headers={
                "Authorization": _bearer_token_cognito,
                "Content-Type": "multipart/form-data; boundary=<calculated when request is sent>",
            },
        )
        print("abby_response", abby_response)
        return None
