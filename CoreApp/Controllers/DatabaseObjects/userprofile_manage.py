import uuid
from configparser import ConfigParser
from boto3.dynamodb.conditions import Key
from itsdangerous import URLSafeSerializer
from CoreApp.Controllers.DatabaseObjects.table_objects import user_profile_table

config_secrets = ConfigParser()
config_secrets.read('config.ini')

def check_if_user_exists(user_profile):
    facebook_id = user_profile['FACEBOOK_ID']
    email_id = user_profile['EMAIL_ID']
    query_response = user_profile_table.get_item(
        Key={
            'FACEBOOK_ID': facebook_id,
            'EMAIL_ID': email_id
        }
    )

    result = {
        'status': '',
        'user_token': ''
    }
    if 'Item' not in query_response:
        print("User does not exist!")
        token = create_new_profile(user_profile)
        result['status'] = 101
        result['user_token'] = token
    else:
        print("User Exists")
        result['status'] = 102
        result['user_token'] = query_response['Item']['USER_TOKEN']

    return result


def create_new_profile(user_profile):
    token_signer = URLSafeSerializer(config_secrets["UUIDSECRET"]["secret_key"],
                                     salt=config_secrets["UUIDSECRET"]["secret_salt"])

    print("Creating a new entry for user!")

    # Generate New User ID --> Random and unique
    user_id = 'UI_' + str(uuid.uuid4())

    # Generate New User Token
    user_token = token_signer.dumps(user_id)

    # New User Record Structure
    new_user_profile = {
        'FACEBOOK_ID': user_profile['FACEBOOK_ID'],
        'USER_ID': user_id,
        'USER_NAME': user_profile['USER_NAME'],
        'EMAIL_ID': user_profile['EMAIL_ID'],
        'GENDER': user_profile['GENDER'],
        'USER_TOKEN': user_token,
        'FIREBASE_ID' : user_profile['FIREBASE_ID']
    }

    user_profile_table.put_item(
        Item=new_user_profile
    )

    print("New entry created!")

    # ADD CODE TO CREATE RECORDS FOR FRIENDLIST, PREFERENCE, AND FEEDBACK
    # -------------------------------------------------------------------

    return user_token


def get_user_id(user_token):
    user_id = 0
    projection_expression = "USER_ID"
    filter_expression = Key('USER_TOKEN').eq(user_token)
    response = user_profile_table.scan(
        ProjectionExpression=projection_expression,
        FilterExpression=filter_expression
    )
    for i in response['Items']:
        user_id = i["USER_ID"]

    return user_id


def get_user_id_given_facebook_id(facebook_id):
    print("testing the query")
    projection_expression = "USER_ID"
    filter_expression = Key('FACEBOOK_ID').eq(facebook_id)
    response = user_profile_table.scan(
        ProjectionExpression=projection_expression,
        FilterExpression=filter_expression
    )
    user_id = ""
    for i in response['Items']:
        user_id = i["USER_ID"]

    return user_id

def get_user_from_user_id(user_id):
    filter_exp = Key('USER_ID').eq(user_id)
    query_response = user_profile_table.scan(
        FilterExpression= filter_exp
    )
    if query_response['Items'][0] is not None:
        return query_response['Items'][0]
    return None

def get_firebase_from_userid(user_id):
    filter_exp = Key('USER_ID').eq(user_id)

    query_response = user_profile_table.scan(
        FilterExpression = filter_exp
    )

    if query_response['Items'][0] is not None:
        return query_response['Items'][0]['FIREBASE_ID']
    return None

