from CoreApp.Controllers.DatabaseObjects.table_objects import user_preference_table

def check_if_preference_user_exists(user_id):
    query_response = user_preference_table.get_item(
        Key={
            'USER_ID': user_id,
        }
    )

    if 'Item' not in query_response:
        return False
    else:
        return True

def update_preference(user_id, preferences):
    if check_if_preference_user_exists(user_id):
        update_response = user_preference_table.update_item(
            Key={
                'USER_ID': user_id
            },
            UpdateExpression="set PREFERENCES = :l",
            ExpressionAttributeValues={
                ':l': preferences
            }
        )

        print("UpdatePreference succeeded:")
        print("update preferences list response ", update_response)
        code = update_response["ResponseMetadata"]["HTTPStatusCode"]
        print("update preferenes list response ", code)
        if code == 200:
            return True
        else:
            return False

    else:
        create_user_record(user_id, preferences)
        return True


def create_user_record(user_id, preferences):
    new_record = {
        'USER_ID' : user_id,
        'PREFERENCES' : preferences
    }

    response = user_preference_table.put_item(
        Item = new_record
    )

    return new_record

def get_preferences(user_id):
    preferences = user_preference_table.get_item(
        Key = {
            'USER_ID' : user_id
        }
    )

    preferences['Item']['PREFERENCES']['PRICE_RANGE'] = float(preferences['Item']['PREFERENCES']['PRICE_RANGE'])
    preferences['Item']['PREFERENCES']['MINIMUM_RATING'] = float(preferences['Item']['PREFERENCES']['MINIMUM_RATING'])

    # print(preferences['Item'])
    # print(type(preferences['Item']['PREFERENCES']['PRICE_RANGE']))
    # print(type(preferences['Item']['PREFERENCES']['MINIMUM_RATING']))

    return preferences['Item']['PREFERENCES']