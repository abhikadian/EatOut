import json


def generate_token():
    return "abcdefgh"


def make_new_user(facebook_id, gender, name, age, email_id):
    # should make a new user from the input params and return the generate user_token
    user_token = generate_token()
    return user_token


def signup_user(request):
    signup_response = {}
    if request.body:
        received_json_data = json.loads(request.body.decode("utf-8"))
        if "FACEBOOK_ID" in received_json_data and "GENDER" in received_json_data \
                and "AGE" in received_json_data and "EMAIL_ID" in received_json_data and "NAME" in received_json_data:
            facebook_id = received_json_data["FACEBOOK_ID"]
            gender = received_json_data["GENDER"]
            age = received_json_data["AGE"]
            email_id = received_json_data["EMAIL_ID"]
            name = received_json_data["NAME"]
            user_token = make_new_user(facebook_id, gender, name, age, email_id)
            if user_token is not None:  # no account yet
                signup_response["STATUS"] = 1
                signup_response["USER_TOKEN"] = user_token
            else:  # something went wrong with the signup
                signup_response["STATUS"] = 3
        else:
            signup_response["STATUS"] = 2

    else:
        signup_response["STATUS"] = 2
    return signup_response
