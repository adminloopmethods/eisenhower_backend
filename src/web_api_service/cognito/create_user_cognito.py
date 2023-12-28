"""
as said in previous email, i've prepared a AWS Cognito setup to use while developing.
I created a User Pool called "UtentiSviluppo1" with id : eu-west-1_Gn7D77zmw
Inside it you'll find two users collected into  "UtentiSviluppo" group. I've already set the
email service with the ufficiofacile.com domain and teamsviluppo@ufficiofacile.com as
sender email. The DKIM DNS records are already in place.
The autonomous sign up is also enabled.
Into the App integration section there are both a Cognito domain : https://gdrsviluppo2.auth.eu-west-1.amazoncognito.com
and a custom domain https://authx.ufficiofacile.com  paired with its SSL wildcard certificate
for ufficiofacile.com domain.
As App client i've created a test one called "Accesso3" and mapped to callback and sign-out URLs
that i used for testing.
You could create your applications clients as well and if you wish, i can either create  DNS record for them,
so all traffic could be shaped in https .
Please feel free to modify the setup as per your needs and let me know if there's something else i can do.
Have a nice day.

"""


import boto3
import datetime

# Amazon Cognito User Pool Configs
LIMIT = 60
REGION = 'us-east-1'
USER_POOL_ID = 'us-east-1_aaaaaaaaa'

# Create boto3 CognitoIdentityProvider client
client = boto3.client('cognito-idp', REGION)
pagination_token = ""

# Degfine function that utilize ListUsers AWS API call
def get_list_cognito_users(cognito_idp_client, next_pagination_token ='', Limit = LIMIT):  

    return cognito_idp_client.list_users(
        UserPoolId = USER_POOL_ID,
        #AttributesToGet = ['name'],
        Limit = Limit,
        PaginationToken = next_pagination_token
    ) if next_pagination_token else cognito_idp_client.list_users(
        UserPoolId = USER_POOL_ID,
        #AttributesToGet = ['name'],
        Limit = Limit
    )
  
# Pull Batch of Amazon Cognito User Pool records  
user_records = get_list_cognito_users(
    cognito_idp_cliend = client,
    next_pagination_token = pagination_token,
    Limit = LIMIT

# Print out result
def datetimeconverter(o):
    if isinstance(o, datetime.datetime):
        return str(o)
  
json_formatted_str = json.dumps(user_records, indent=4, default=datetimeconverter)
print(json_formatted_str)  