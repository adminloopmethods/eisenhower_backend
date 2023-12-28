"""
https://boto3.amazonaws.com/v1/documentation/api/
latest/reference/services/cognito-idp.html#
CognitoIdentityProvider.Client.admin_create_user
https://medium.com/@houzier.saurav/aws-cognito-with-python-6a2867dd02c6



Log in success
Access token: eyJraWQiOiJjVU1XWnIrakVBY1lwRUhlMnNVelpESmdEZFhQd2NzQ0pwVjM4NzBydnh3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9HbjdENzd6bXciLCJjbGllbnRfaWQiOiIya2NocW1wb3RvNmswNmFrOXY5MzY4ajQ4aiIsIm9yaWdpbl9qdGkiOiIwZDZkZTZkNS03Yjk5LTRhNjItYWYwZS0zMDY0NDY2MWI2ZTQiLCJldmVudF9pZCI6IjYyYjg1ODEzLWYyOWUtNDIwZC1hNDJhLWY0OTEzODIzYWFkYyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2NzA0ODI3MDIsImV4cCI6MTY3MDQ4NjMwMiwiaWF0IjoxNjcwNDgyNzAyLCJqdGkiOiI1MjE5ZDkxMi1iOWQ5LTRjODQtYTgxYi0xN2Y3MDVmMjIyMmMiLCJ1c2VybmFtZSI6IjA0YjU1Mzg3LTMyMzEtNDIyOC04NjM1LWM2MGJmMmVkYTg2NyJ9.X5g_3jEUgMyIi0iXNZMlkQgtljiAuuJAAQvYz9gXY-etNSu6P7Vl__0zQdHFVBbfKvSvoaPULl3d2huDFRgmnv4EScPdmqve_zQJa63CitPgTmFijb1tgw9IXzx7LpKyGLlNt9kW_4mXnoUp2NDfyq7HQT9kgF0BgxDVPShwvOg5o6ZtN9QPVKeNBeO0egGikE3Fzk6u7wmZAGDajrGFaO5RmhycADe44EqcIA468AwFyX6hCWmz98aes6iPAsO_HWc-ED1Eu2MxxT0B3m_lmAj7sOBw6IQhU5v5wOJugbnqY8D1dkMjeEzTv9U3xKU5f8V_cOURk4QPizFA1gppVg
ID token: eyJraWQiOiJQMDhLaENhRTlyOHU0MGVRc2RLOTNia0FLZ0xhZFhKREIyYThSdDBpbm1JPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS13ZXN0LTEuYW1hem9uYXdzLmNvbVwvZXUtd2VzdC0xX0duN0Q3N3ptdyIsInBob25lX251bWJlcl92ZXJpZmllZCI6ZmFsc2UsImNvZ25pdG86dXNlcm5hbWUiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJnaXZlbl9uYW1lIjoiQWRpbCBSYWphIiwib3JpZ2luX2p0aSI6IjBkNmRlNmQ1LTdiOTktNGE2Mi1hZjBlLTMwNjQ0NjYxYjZlNCIsImF1ZCI6IjJrY2hxbXBvdG82azA2YWs5djkzNjhqNDhqIiwiZXZlbnRfaWQiOiI2MmI4NTgxMy1mMjllLTQyMGQtYTQyYS1mNDkxMzgyM2FhZGMiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY3MDQ4MjcwMiwicGhvbmVfbnVtYmVyIjoiKzkxNjQ1NjQ1NjQ1NiIsImV4cCI6MTY3MDQ4NjMwMiwiaWF0IjoxNjcwNDgyNzAyLCJmYW1pbHlfbmFtZSI6IkR1bW15IGZhbWlseSBOYW1lIiwianRpIjoiMmYzMzdlZDItNDgyZS00YjhjLTgzMjctMzk0MmFkYmIzYzQ3IiwiZW1haWwiOiJyYWphQGdtYWlsLmNvbSJ9.cX_GTdIObjj87ue7vAlODBjcNjncL5R7kAvYUV2JRSLjsvv-QsShrEgPlKMk2D1nK_l2ocf5e-k6gGhbjK-8PRbc-qqUEjP5F7NDITOCaPX8u5reOfXQXtOD2_jpDymlSncPdYplmrQWrfOW1zWYnkApVyZzT3lQUgsmi4DC0zFCXofOzNAqu6RyJshNFmLvIiMmJIkR5CNYbUaRwVpBkgCHDg8bDOnHv_UiDCIiRzib6VYmtc_cnIbcLRDKGUu_fA9kuBSDzDiiqcswZZPORzjZtYWs_bqoUV1U7lo7LqPd9O3RcRFfCFlfJEUHnW3_7EkPbec6ATmmZPeWd9DaCA
########aws_cognito_response {'ChallengeParameters': {}, 'AuthenticationResult': {'AccessToken': 'eyJraWQiOiJjVU1XWnIrakVBY1lwRUhlMnNVelpESmdEZFhQd2NzQ0pwVjM4NzBydnh3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9HbjdENzd6bXciLCJjbGllbnRfaWQiOiIya2NocW1wb3RvNmswNmFrOXY5MzY4ajQ4aiIsIm9yaWdpbl9qdGkiOiIwZDZkZTZkNS03Yjk5LTRhNjItYWYwZS0zMDY0NDY2MWI2ZTQiLCJldmVudF9pZCI6IjYyYjg1ODEzLWYyOWUtNDIwZC1hNDJhLWY0OTEzODIzYWFkYyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2NzA0ODI3MDIsImV4cCI6MTY3MDQ4NjMwMiwiaWF0IjoxNjcwNDgyNzAyLCJqdGkiOiI1MjE5ZDkxMi1iOWQ5LTRjODQtYTgxYi0xN2Y3MDVmMjIyMmMiLCJ1c2VybmFtZSI6IjA0YjU1Mzg3LTMyMzEtNDIyOC04NjM1LWM2MGJmMmVkYTg2NyJ9.X5g_3jEUgMyIi0iXNZMlkQgtljiAuuJAAQvYz9gXY-etNSu6P7Vl__0zQdHFVBbfKvSvoaPULl3d2huDFRgmnv4EScPdmqve_zQJa63CitPgTmFijb1tgw9IXzx7LpKyGLlNt9kW_4mXnoUp2NDfyq7HQT9kgF0BgxDVPShwvOg5o6ZtN9QPVKeNBeO0egGikE3Fzk6u7wmZAGDajrGFaO5RmhycADe44EqcIA468AwFyX6hCWmz98aes6iPAsO_HWc-ED1Eu2MxxT0B3m_lmAj7sOBw6IQhU5v5wOJugbnqY8D1dkMjeEzTv9U3xKU5f8V_cOURk4QPizFA1gppVg', 'ExpiresIn': 3600, 'TokenType': 'Bearer', 'RefreshToken': 'eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.2OztUNNQnooBfsh5YECYYFLx9iGzct6ENWyzUFU9tjN2MaPWv_LkbvqGpGwDsiE6jXuJDTV3wEVfiDuFLt8fonhWhO7kJAE5_-VfaX2QTSoX4IOhqeHKvq0PN78UeI3Cjmqo9HgB3sWXTaxpZklS8Ynun_Xxi9_yt4yPww2VxmsaGgSUCc5Be7YuFK59ED_IVzKT2mfM1rwN7gNbt7M2V8h1RfqmpnKob6V-XmN06wCu5-J3S3Yt7SeIao7Gyy-1D7tCMzkZSPIfhURwi_hfqX6gYnhRjc68jAuTA6Le1lW9KQJCLxr1z_8lQRpsDZ1umwk_qCugplmar7buxasVnA.JxK4E3aIgqEpCg89.n5e66Q9BqKzq5-wlIo6Z_27f6QJvGYRpp2GJ3HGZIfW6_QT3OCcYGuqIdYmyIMaoKJnBgZnIf6GroRkR097buiX4BaCBnO7o1_iBFEDXVq3CP4fTQa5TD7kXXVvJSpyBAKruVv8-2l3cJ6KL9w6P7TunVC6D6iIZaZqw0piyxmWomdYRsIfPe18ewWuAPiwB2aHizjA5qBzupiaFy0MKsMpllNswmm2DQeqeZWC21R6luw0diODOnbvuGuZcp9UKfEjTp_6PH7Rjf8yGnj98koe0XTwSyA8l6emUoOdzHbYRQA2H9wxYm26yS_smN0uYhHuDgklbtjdoJUz3PBgMF_fZVMtXwBIpfbmBl8qSIFBJr6yoZQnfbMS5h5rUbEBTcHuFXE4FyXXM6_V5ikQdlKgpn3fXf2If-qB9WPpMeHVGe3U8wdNZzg6Wfv9_9LA851M1-U4tIsLV0Z2GxtiSDQBnAQKskbwcdpbcxClCfB9EmfEZj7qH_DkGhGIr03jEMVJbhE3aZo9iVRjDqs8kKT9XXMi9Zc2qmrrE5htWobBjD5r4_8Ma0G0A5VQuxSBiVP-oCRHMLyawyrAe9YR8KpifBAHC7lHf70Rli77CHsNemWxBqdeuUePHOOS10Mh1_inqu_b25PUZ6oMOV8qvg16GsyppZp2qSnjKSKTkZHYV6yWYh5JtkUwhDKWaSfdQuep7dmDZz4F8E2XgVuERYxqEvVqITmv2ku2cl9AJ7zjNpWylMOhIuoKJkE0-yaNwMLQTnpqDoJ42jlMsFKICwe0TulKTVF5NBZtGPkunBTZ4uADinZpt8TXWyogiuEEp7YwB_QGQg489wfSt_5v9qQM78EFjmRPxT8rc7Sz-bFK95vgOEf_RwJzq9hibqh4jVJb58fdxZSIF0vQrozPxNSDigJt-msF-NOrB79JDNs2uK3q1lGK_Nt8QuOavcIs4rWdvo3eEna5P5T96FguLUBIFDNOlEfgjCrAMUSY68OQyNhh1wRYrPEcAophxiZ41oMyvIgUNE8AMT_OkPoJ1L4zv20Kzm4LkKxzz4CZHtHANC-HtPCGJMTMgwEr7a7bJ-oVVKRGgQrNfD9JfUG8Xb-9g7h9wuMa-0GEI0rmWS5VsnPDkfLxOCdTVUn48dUaxkcfH4wyE6T5hTnexdqqIdY6vE-HoXoIRsh1GogvCIUfsytoCLdGTeVPCRlfMag5BKcRFBTEOJvYQ0Q9vNs6CIBkQtSLmZ8Skkekaf5koQLB8pMJ50W7kIx0PsABboI-TnGuiZMWjS5XvQD2OgRqJ_zzkns5C4HGMHjeWaejznqeoazpykkgdWo-QvhE.KTgNwzsuAI0NYGQ58QcOig', 'IdToken': 'eyJraWQiOiJQMDhLaENhRTlyOHU0MGVRc2RLOTNia0FLZ0xhZFhKREIyYThSdDBpbm1JPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS13ZXN0LTEuYW1hem9uYXdzLmNvbVwvZXUtd2VzdC0xX0duN0Q3N3ptdyIsInBob25lX251bWJlcl92ZXJpZmllZCI6ZmFsc2UsImNvZ25pdG86dXNlcm5hbWUiOiIwNGI1NTM4Ny0zMjMxLTQyMjgtODYzNS1jNjBiZjJlZGE4NjciLCJnaXZlbl9uYW1lIjoiQWRpbCBSYWphIiwib3JpZ2luX2p0aSI6IjBkNmRlNmQ1LTdiOTktNGE2Mi1hZjBlLTMwNjQ0NjYxYjZlNCIsImF1ZCI6IjJrY2hxbXBvdG82azA2YWs5djkzNjhqNDhqIiwiZXZlbnRfaWQiOiI2MmI4NTgxMy1mMjllLTQyMGQtYTQyYS1mNDkxMzgyM2FhZGMiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY3MDQ4MjcwMiwicGhvbmVfbnVtYmVyIjoiKzkxNjQ1NjQ1NjQ1NiIsImV4cCI6MTY3MDQ4NjMwMiwiaWF0IjoxNjcwNDgyNzAyLCJmYW1pbHlfbmFtZSI6IkR1bW15IGZhbWlseSBOYW1lIiwianRpIjoiMmYzMzdlZDItNDgyZS00YjhjLTgzMjctMzk0MmFkYmIzYzQ3IiwiZW1haWwiOiJyYWphQGdtYWlsLmNvbSJ9.cX_GTdIObjj87ue7vAlODBjcNjncL5R7kAvYUV2JRSLjsvv-QsShrEgPlKMk2D1nK_l2ocf5e-k6gGhbjK-8PRbc-qqUEjP5F7NDITOCaPX8u5reOfXQXtOD2_jpDymlSncPdYplmrQWrfOW1zWYnkApVyZzT3lQUgsmi4DC0zFCXofOzNAqu6RyJshNFmLvIiMmJIkR5CNYbUaRwVpBkgCHDg8bDOnHv_UiDCIiRzib6VYmtc_cnIbcLRDKGUu_fA9kuBSDzDiiqcswZZPORzjZtYWs_bqoUV1U7lo7LqPd9O3RcRFfCFlfJEUHnW3_7EkPbec6ATmmZPeWd9DaCA'}, 'ResponseMetadata': {'RequestId': '62b85813-f29e-420d-a42a-f4913823aadc', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Thu, 08 Dec 2022 06:58:22 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '4232', 'connection': 'keep-alive', 'x-amzn-requestid': '62b85813-f29e-420d-a42a-f4913823aadc'}, 'RetryAttempts': 0}}


"""

import base64
import datetime
# has code desc
import hashlib
import hmac
import json

# projects conf settings
import boto3
from botocore.config import Config
from django.conf import settings

LIMIT = 60

_mY_cOnFiG = Config(
    region_name=settings.COGNITO_REGION,
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)


class AWSCognito:
    """this AWSCognitoAuthentication is used to manage the authentication
    process using aws cognito service
    """

    def __init__(self, **kwargs):

        # all secrect aws keys
        self.confirm_cognito_resp = None
        self.app_client_secret = settings.COGNITO_APP_CLIENT_SECRET
        self.region = settings.COGNITO_REGION
        self.app_client_id = settings.COGNITO_APP_CLIENT
        self.cognito_pool_id = settings.COGNITO_POOL_ID
        # all request parameters
        self.auth_user_instance = kwargs.get('auth_user_instance', None)
        self.data = kwargs.get('data', {})
        self._latin_key = 'latin-1'
        self.secret_hash = None
        self.token_key = ''
        self.access_token_dict = {}
        # boto3 client instance 
        self.cognito = boto3.client(
            'cognito-idp',
            config=_mY_cOnFiG,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        # constants instance variables
        self.cognito_resp = None
        self.update_cognito_resp = None
        self.format_phone_number = None
        self._username = kwargs.get('username', None)
        self.confirm_code = kwargs.get('confirm_code', None)
        self._family_name = 'Dummy family Name'
        self.given_name = None
        self._limit = 60
        self._pagination_token = ""

    def create_secret_hash(self):
        """this create_secret_hash method used to convert
        secret to hash secret values
        :return:
        """
        # b'u8f323eb3itbr3731014d25spqtv5r6pu01olpp5tm8ebicb8qa'
        key = bytes(self.app_client_secret, self._latin_key)
        # b'wasdkiller396u9ekukfo77nhcfbmqnrec8p'
        msg = bytes(''.join([self._username + self.app_client_id]), self._latin_key)
        # b'P$#\xd6\xc1\xc0U\xce\xc1$\x17\xa1=\x18L\xc5\x1b\xa4\xc8\xea,\x92\xf5\xb9\xcdM\xe4\x084\xf5\x03~'
        new_digest = hmac.new(key, msg, hashlib.sha256).digest()
        # UCQj1sHAVc7BJBehPRhMxRukyOoskvW5zU3kCDT1A34=
        self.secret_hash = base64.b64encode(new_digest).decode()

    def cognito_format_number(self):
        """this cognito_format_number method used to manage the
        format phone number according to cognito user
        :return:
        """
        self.format_phone_number = ''.join(['+', str(self.data['isd']), self.data['mobile']])

    def cognito_given_name(self):
        """
        this cognito_given_name method used to create join name for two string
        """
        self.given_name = ''.join([self.data.get('first_name'), ' ',
                                   self.data.get('last_name')])

    def cognito_registration(self):
        """
        DRF with Cognito cognito_registration
        Sample DRF App with Cognito to authenticate the APIs
        :return:{
            'UserConfirmed': False,
            'CodeDeliveryDetails': {
                'Destination': '+*********9009',
                'DeliveryMedium': 'SMS',
                'AttributeName': 'phone_number'
            },
            'UserSub': '6b7a02c2-9bd6-40e1-a23d-9a9db5b3a562',
            'ResponseMetadata': {
                'RequestId': '4bec2788-1366-4fd2-a7ec-021b3d1118b4',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'date': 'Thu, 20 Oct 2022 12:33:16 GMT',
                    'content-type': 'application/x-amz-json-1.1',
                    'content-length': '181',
                    'connection': 'keep-alive',
                    'x-amzn-requestid': '4bec2788-1366-4fd2-a7ec-021b3d1118b4'},
                    'RetryAttempts': 0
                }
        }
        """
        self.cognito_format_number()
        try:
            self.cognito_resp = self.cognito.sign_up(
                SecretHash=self.secret_hash,
                ClientId=self.app_client_id,
                Username=self._username,
                Password=self.data['password'],
                UserAttributes=[
                    {
                        'Name': 'phone_number',
                        'Value': self.format_phone_number
                    },
                    {
                        'Name': 'family_name',
                        'Value': self._family_name
                    },
                    {
                        'Name': 'given_name',
                        'Value': ''.join([self.data.get('first_name'), ' ',
                                          self.data.get('last_name')])
                    }

                ]
            )
            # Use AdminAddUserToGroup to add the user to the group
            self.cognito.admin_add_user_to_group(
                UserPoolId=self.cognito_pool_id,
                Username=self._username,
                GroupName='EMM'
            )
            return self.cognito_resp if self.cognito_resp else None
        except Exception as e:
            print('CognitoSignUpErr')
            print(e)
            return None

    def admin_cognito_registration(self):
        """
        DRF with Cognito cognito_registration
        Sample DRF App with Cognito to authenticate the APIs
        :return:{
            'UserConfirmed': False,
            'CodeDeliveryDetails': {
                'Destination': '+*********9009',
                'DeliveryMedium': 'SMS',
                'AttributeName': 'phone_number'
            },
            'UserSub': '6b7a02c2-9bd6-40e1-a23d-9a9db5b3a562',
            'ResponseMetadata': {
                'RequestId': '4bec2788-1366-4fd2-a7ec-021b3d1118b4',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'date': 'Thu, 20 Oct 2022 12:33:16 GMT',
                    'content-type': 'application/x-amz-json-1.1',
                    'content-length': '181',
                    'connection': 'keep-alive',
                    'x-amzn-requestid': '4bec2788-1366-4fd2-a7ec-021b3d1118b4'},
                    'RetryAttempts': 0
                }
        }
        """
        self.cognito_format_number()
        try:
            self.cognito_resp = self.cognito.admin_create_user(
                # SecretHash=self.secret_hash,
                # ClientId=self.app_client_id,
                UserPoolId=self.cognito_pool_id,
                Username=self._username,
                TemporaryPassword=self.data['password'],
                UserAttributes=[
                    {
                        'Name': 'phone_number',
                        'Value': self.format_phone_number
                    },
                    {
                        'Name': 'family_name',
                        'Value': self._family_name
                    },
                    {
                        'Name': 'given_name',
                        'Value': ''.join([self.data.get('first_name'), ' ',
                                          self.data.get('last_name')])
                    }

                ],
                ForceAliasCreation=True,
                MessageAction='SUPPRESS',
                DesiredDeliveryMediums=['EMAIL'],
                # ClientMetadata={
                #     'string': 'string'
                # }
            )
            return self.cognito_resp if self.cognito_resp else None
        except Exception as e:
            print('CognitoSignUpErr')
            print(e)
            return None

    def cognito_confirm_admin(self):
        """This cognito_confirm_admin method is used to manage the
        confirmation using cognito admin
        """
        try:
            self.confirm_cognito_resp = self.cognito.admin_confirm_sign_up(
                Username=self._username,
                UserPoolId=self.cognito_pool_id,
            )
            if self.confirm_cognito_resp:
                return self.confirm_cognito_resp
            else:
                return None
        except Exception as e:
            print('CognitoResendConfirmationErr')
            print(e)
            return None

    def confirm_sign_up(self):
        """this confirm_sign_up method used to manage and register a new user
        with the cognito pool database
        """
        self._username = self.data['email']
        self.create_secret_hash()
        self.cognito_resp = self.cognito_registration()
        return self.cognito_confirm_admin()

    def update_cognito_user_by_admin(self):
        """this update_cognito_user_by_admin method used to update the cognito 
        user using cognito boto services
        """
        self.cognito_format_number()
        self.cognito_given_name()

        if self.data.get('mobile') and self.data.get('first_name'):
            _update_user_attributes = [
                {'Name': 'phone_number', 'Value': self.format_phone_number},
                {'Name': 'given_name', 'Value': self.given_name}
            ]
        if not self.data.get('mobile') and self.data.get('first_name'):
            _update_user_attributes = [
                {'Name': 'given_name', 'Value': self.given_name}
            ]
        if self.data.get('mobile') and not self.data.get('first_name'):
            _update_user_attributes = [
                {'Name': 'phone_number', 'Value': self.format_phone_number}
            ]

        self.update_cognito_resp = self.cognito.admin_update_user_attributes(
            UserPoolId=self.cognito_pool_id,
            Username=self._username,
            UserAttributes=_update_user_attributes,
            ClientMetadata={
                'string': 'string'
            }
        )

    # @staticmethod
    def get_list_cognito_users(
            self,
            cognito_idp_client,
            next_pagination_token='', Limit=LIMIT):
        """
        # Degfine function that utilize ListUsers AWS API call
        """
        return cognito_idp_client.list_users(
            UserPoolId=self.cognito_pool_id,
            # AttributesToGet=['name'],
            Limit=Limit,
            PaginationToken=next_pagination_token
        ) if next_pagination_token else cognito_idp_client.list_users(
            UserPoolId=self.cognito_pool_id,
            # AttributesToGet=['name'],
            Limit=Limit
        )

    def get_cognito_user_list(self):
        """this get_cognito_user_listing method used to get the 
        all verified cognito user from cognito as per required cognito pool id
        """
        # Pull Batch of Amazon Cognito User Pool records

        user_records = self.get_list_cognito_users(
            cognito_idp_client=self.cognito,
            next_pagination_token=self._pagination_token,
            Limit=self._limit)

        # Print out result
        def datetime_converter(o):
            if isinstance(o, datetime.datetime):
                return str(o)

        json_formatted_users = json.dumps(user_records, indent=4, default=datetime_converter)
        json_to_dict = json.loads(json_formatted_users)
        # print('resultdata: ', json_to_dict['Users'])
        return json_to_dict['Users']


    def authenticate_and_get_token(self, password: str):
        """this authenticate_and_get_token method used to get the authenticate 
        the cognito pool access
        """
        print('self._username', self._username)
        print('password', password)
        self.create_secret_hash()
        resp = self.cognito.admin_initiate_auth(
            UserPoolId=self.cognito_pool_id,
            ClientId=self.app_client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                "USERNAME": self._username,
                "PASSWORD": password,
                "SECRET_HASH": self.secret_hash
            }
        )
        return resp

    def get_cognito_authentication(self, password):
        """this authenticate_and_get_token method used to get the authenticate 
        the cognito pool access.
        """
        try:
            self.create_secret_hash()
            self.cognito_response = self.cognito.initiate_auth(
                # SecretHash=self.secret_hash,
                ClientId=self.app_client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    "USERNAME": self._username,
                    "PASSWORD": password,
                    "SECRET_HASH": self.secret_hash
                }
            )
            print('self.cognito_response', self.cognito_response)
            if self.cognito_response:
                return self.cognito_response
            else:
                return None
        except Exception as e:
            print('cognitoResponseErr')
            print(e)
            return None

    def list_groups_for_user(self):
        """list_groups_for_user
        """
        response = self.cognito.admin_list_groups_for_user(
            Username=self._username,
            UserPoolId=self.cognito_pool_id,
            # Limit=3,
            # NextToken='next'
        )
        return response




