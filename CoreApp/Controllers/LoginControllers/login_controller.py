import json
from django.shortcuts import render
from CoreApp.Controllers.DatabaseObjects import userprofile_manage

def test_login(request):
    login_response = {}

    if request.body:
        print("Incoming Login Request")
        user_profile = json.loads(request.body.decode("utf-8"))

        if "FACEBOOK_ID" in user_profile:
            login_response = userprofile_manage.check_if_user_exists(user_profile)

        else:
            login_response["STATUS"] = 103
            print("Incomplete Data in POST request")

    else:
        login_response["STATUS"] = 103
        print("Incomplete Data in POST request")

    return login_response
