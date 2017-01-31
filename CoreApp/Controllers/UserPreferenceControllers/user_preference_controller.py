import json
from CoreApp.Controllers.DatabaseObjects import userpreference_manage
from CoreApp.Controllers.DatabaseObjects.userprofile_manage import get_user_id

# ============FIX SPACE AFTER PREFERENCES=============================

def update_user_preference(request):
    print("Request for updating the preferences of user")
    update_user_preference_response = {}
    request_body = json.loads(request.body.decode("utf-8"))

    if 'USER_TOKEN' in request_body:
        user_id = get_user_id(request_body['USER_TOKEN'])
        if user_id == 0:
            print("Invalid user token while updating preferences")
            update_user_preference_response["STATUS"] = 302
            return update_user_preference_response
        else:
            if 'PREFERENCES' in request_body:  # XXXXX SPACE HERE
                user_preferences = request_body['PREFERENCES']     # XXXXX SPACE HERE
                update_status = userpreference_manage.update_preference(user_id, user_preferences)
                if update_status:
                    update_user_preference_response['STATUS'] = 301
                    return update_user_preference_response
                else:
                    update_user_preference_response['STATUS'] = 303
                    return update_user_preference_response
            else:
                update_user_preference_response['STATUS'] = 302
                return update_user_preference_response

    else:
        update_user_preference_response['STATUS'] = 302
        return update_user_preference_response

def pull_preferences(request):
    print("Request for pulling the preferences of user")
    user_preference_response = {}
    request_body = json.loads(request.body.decode("utf-8"))

    if "USER_TOKEN" in request_body:
        user_id = get_user_id(request_body['USER_TOKEN'])
        if user_id == 0:
            print("Invalid user token while updating preferences")
            user_preference_response["STATUS"] = 302
            return user_preference_response
        else:
            user_preferences = userpreference_manage.get_preferences(user_id)
            user_preference_response['STATUS'] = 301
            user_preference_response['PREFERENCES'] = user_preferences

            return user_preference_response
    else:
        user_preference_response["STATUS"] = 302
        return user_preference_response