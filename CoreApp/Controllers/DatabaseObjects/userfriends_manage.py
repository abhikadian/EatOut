from boto3.dynamodb.conditions import Key
from CoreApp.Controllers.DatabaseObjects.table_objects import user_friend_table as friend_table
from CoreApp.Controllers.DatabaseObjects.userprofile_manage import get_user_id_given_facebook_id, get_user_from_user_id


def manage_friends_list(user_id, list_of_friends):
    print("Calling manage friend list")
    # list is a list of facebook ids, should map them to app_ids and store them in the database
    list_of_friends_user_ids = []
    update_response = {}

    for facebook_id in list_of_friends:
        user_id_of_friend = get_user_id_given_facebook_id(facebook_id)
        if user_id_of_friend != '':
            list_of_friends_user_ids.append(user_id_of_friend)

    print(list_of_friends_user_ids)

    if len(list_of_friends_user_ids) != 0:
        update_response = friend_table.update_item(
            Key={
                'USER_ID': user_id
            },
            UpdateExpression="set FRIENDS_LIST = :l",
            ExpressionAttributeValues={
                ":l": list_of_friends_user_ids
            }
        )

        print("UpdateItem succeeded:")
        print("update friends list response ", update_response)
    else:
        print("No Friends")
        update_response["ResponseMetadata"]["HTTPStatusCode"] = 200

    return update_response

def get_all_friends_of_user(user_id):
    query_response = friend_table.get_item(
        Key = {
            "USER_ID" : user_id
        }
    )

    friends = query_response['Item']['FRIENDS_LIST']

    all_friends = []

    for user in friends:
        user_record = get_user_from_user_id(user)
        if user_record is not None:
            record_to_send = {}         # NOT SENDING ALL USER DATA
            record_to_send['USER_ID'] = user_record['USER_ID']
            record_to_send['USER_NAME'] = user_record['USER_NAME']
            record_to_send['EMAIL_ID'] = user_record['EMAIL_ID']
            all_friends.append(record_to_send)
            print("Added record for ", user_record['USER_NAME'])

    return all_friends

