import json
from collections import Counter
from CoreApp.Controllers.DatabaseObjects.table_objects import event_table, votebank_table, votecount_table
from CoreApp.Controllers.DatabaseObjects.userprofile_manage import get_user_id
from CoreApp.Controllers.DatabaseObjects.event_manage import generate_event, update_event_record, get_event, get_event_ui
from CoreApp.Controllers.DatabaseObjects.restaurantprofile_manage import retrieve_restaurant_profile
from boto3.dynamodb.conditions import Key
from operator import itemgetter
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="API KEYS HERE")

def create_event_request(request):
    request_body = json.loads(request.body.decode("utf-8"))

    response = {}
    if 'USER_TOKEN' in request_body:
        user_token = request_body['USER_TOKEN']
        user_id = get_user_id(user_token)

        if user_id != 0:
            if 'EVENT_DETAILS' in request_body:
                event_details = request_body['EVENT_DETAILS']
                generate_response = generate_event(user_id, event_details)
                response['STATUS'] = 601
                response['EVENT'] = generate_response
                return response
            else:
                response['STATUS'] = 602
                return response
        else:
            response['STATUS'] = 602
            return response
    else:
        response['STATUS'] = 602
        return response


def update_event(request):
    request_body = json.loads(request.body.decode("utf-8"))

    response = {}
    if 'USER_TOKEN' in request_body:
        user_token = request_body['USER_TOKEN']
        user_id = get_user_id(user_token)

        if user_id != 0:
            if 'EVENT_DETAILS' in request_body:
                event_details = request_body['EVENT_DETAILS']
                update_response = update_event_record(event_details)
                response['STATUS'] = 601
                response['EVENT'] = update_response
                return response
            else:
                response['STATUS'] = 602
                return response
        else:
            response['STATUS'] = 602
            return response
    else:
        response['STATUS'] = 602
        return response


def update_event_vote(request):
    print("In function body")
    request_body = json.loads(request.body.decode("utf-8"))

    response = {}
    if 'USER_TOKEN' in request_body:
        print("After user token")
        user_token = request_body['USER_TOKEN']
        user_id = get_user_id(user_token)

        if user_id != 0:
            print("Found user id")
            if 'VOTES' in request_body and 'EVENT_ID' in request_body:

                print("Votes and Event Id ok")

                event_id = request_body['EVENT_ID']
                event_details = get_event(event_id)
                rest_votes = request_body['VOTES']

                vote_count = votecount_table.query(
                    KeyConditionExpression=Key('EVENT_ID').eq(event_id)
                )

                max_count = 0
                rest_id = ""

                print(vote_count)
                for item in vote_count['Items']:
                    if item['VOTE_COUNT'] > max_count:
                        max_count = item['VOTE_COUNT']
                        rest_id = item['RESTAURANT_ID']

                # ------------------

                update_query_response = votebank_table.update_item(
                    Key = {
                        "EVENT_ID" : event_id,
                        "ENTITY_ID" : user_id
                    },
                    UpdateExpression="set VOTES = :v",
                    ExpressionAttributeValues = {
                        ":v" : rest_votes
                    }
                )

                print("Table updated")

                # Update Scores

                event_query_response = votebank_table.query(
                    KeyConditionExpression = Key('EVENT_ID').eq(event_id)
                )

                all_votes = []

                for vote in event_query_response['Items']:
                    all_votes += vote['VOTES']

                vote_count = Counter(all_votes)

                for restaurant in vote_count.keys():
                    update_count_response = votecount_table.update_item(
                        Key = {
                            "EVENT_ID" : event_id,
                            "RESTAURANT_ID" : restaurant
                        },
                        UpdateExpression = "set VOTE_COUNT = :v",
                        ExpressionAttributeValues = {
                            ":v" : vote_count[restaurant]
                        }
                    )

                vote_count = votecount_table.query(
                    KeyConditionExpression=Key('EVENT_ID').eq(event_id)
                )

                new_max_count = 0
                new_rest_id = ""

                print(vote_count)
                for item in vote_count['Items']:
                    if item['VOTE_COUNT'] > new_max_count:
                        new_max_count = item['VOTE_COUNT']
                        new_rest_id = item['RESTAURANT_ID']

                if new_rest_id != rest_id:
                    highest_rest = retrieve_restaurant_profile(new_rest_id)
                    event_details["EVENT_RESTAURENTSELECT"] = highest_rest["RESTAURANT_NAME"]
                    event_details["EVENT_LOCATION_POINT"] = highest_rest["RESTAURANT_LOCATION"]

                    update_event_response = event_table.put_item(
                        Item = event_details
                    )

                    participant_firebase = event_details["EVENT_PARTICIPANT_FIREBASE"]
                    message_title = "New Top Voted Restaurant"
                    message_body = "Hi! " + highest_rest["RESTAURANT_NAME"] + " is the new top voted restaurant for " + \
                                   event_details["EVENT_NAME"] + " event."
                    result = push_service.notify_multiple_devices(registration_ids=participant_firebase,
                                                                  message_title=message_title,
                                                                  message_body=message_body)
                    print(result)


                response['STATUS'] = 601
                response['VOTE_COUNT'] = vote_count
                return response
            else:
                response['STATUS'] = 602
                return response
        else:
            response['STATUS'] = 602
            return response
    else:
        response['STATUS'] = 602
        return response


# def get_preferences_from_eventid(request):
#     request_body = json.loads(request.body.decode("utf-8"))
#
#     response = {}
#     if 'USER_TOKEN' in request_body:
#         user_token = request_body['USER_TOKEN']
#         user_id = get_user_id(user_token)
#
#         if user_id != 0:
#             if 'EVENT_DETAILS' in request_body:
#                 event_details = request_body['EVENT_DETAILS']
#                 update_response = update_event_record(event_details)
#                 response['STATUS'] = 601
#                 response['EVENT'] = update_response
#                 return response
#             else:
#                 response['STATUS'] = 602
#                 return response
#         else:
#             response['STATUS'] = 602
#             return response
#     else:
#         response['STATUS'] = 602
#         return response

def get_event_recommendations(request):
    print("Computing recommendations!")
    request_body = json.loads(request.body.decode("utf-8"))

    response = {}
    if 'USER_TOKEN' in request_body:
        print("Got token")
        user_token = request_body['USER_TOKEN']
        print(user_token)
        user_id = get_user_id(user_token)

        if user_id != 0 and "EVENT_ID" in request_body:
            print("Got id and event id")

            event_id = request_body["EVENT_ID"]
            # Get current top

            vote_count = votecount_table.query(
                KeyConditionExpression=Key('EVENT_ID').eq(event_id)
            )

            # max_count = 0
            # rest_id = ""
            #
            # print(vote_count)
            # for item in vote_count['Items']:
            #     if item['VOTE_COUNT'] > max_count:
            #         max_count = item['VOTE_COUNT']
            #         rest_id = item['RESTAURANT_ID']
            #
            #         # ------------------
            event_details = get_event(event_id)

            if event_details is not None:
                print("Got event details")
                prefs = []
                for item in event_details["RECOMMENDATIONS"]:
                    votes_query = votecount_table.get_item(
                        Key = {
                            "EVENT_ID": event_id,
                            "RESTAURANT_ID": item["RESTAURANT_ID"]
                        }
                    )

                    if 'Item' in votes_query:
                        record = {
                            "RESTAURANT_ID": item["RESTAURANT_ID"],
                            "RESTAURANT_NAME": item["RESTAURANT_NAME"],
                            "VOTE_COUNT": votes_query['Item']["VOTE_COUNT"]
                        }

                    else:
                        record = {
                            "RESTAURANT_ID": item["RESTAURANT_ID"],
                            "RESTAURANT_NAME": item["RESTAURANT_NAME"],
                            "VOTE_COUNT": 0
                        }

                    prefs.append(record)

                prefs = sorted(prefs, key=itemgetter('VOTE_COUNT'), reverse=True)


                # event_details["EVENT_RESTAURENTSELECT"] = prefs[0]["RESTAURANT_NAME"]
                # event_details["EVENT_LOCATION_POINT"] = retrieve_restaurant_profile(prefs[0]["RESTAURANT_ID"])["RESTAURANT_LOCATION"]
                #
                # update_event_response = event_table.put_item(
                #     Item = event_details
                # )
                #
                # participant_firebase = event_details["EVENT_PARTICIPANT_FIREBASE"]
                # message_title = "New Top Voted Restaurant"
                # message_body = "Hi! " + prefs[0]["RESTAURANT_NAME"] + " is the new top voted restaurant for " + \
                #                event_details["EVENT_NAME"] + " event."
                # result = push_service.notify_multiple_devices(registration_ids=participant_firebase,
                #                                               message_title=message_title,
                #                                               message_body=message_body)
                # print(result)

                #------------------
                response["STATUS"] = 601
                response["RECOMMENDATIONS"] = prefs

            else:
                response["STATUS"] = 602
        else:
            response["STATUS"] = 602
    else:
        response["STATUS"] = 602

    print("Returning reco list")
    print(response["STATUS"])
    print(response["RECOMMENDATIONS"])
    return response


def get_event_details_from_id(request):
    request_body = json.loads(request.body.decode("utf-8"))

    response = {}
    if 'USER_TOKEN' in request_body:
        user_token = request_body['USER_TOKEN']
        user_id = get_user_id(user_token)

        if user_id != 0 and "EVENT_ID" in request_body:
            event_id = request_body["EVENT_ID"]
            event_result = get_event_ui(event_id)

            if event_result is not None:
                response["STATUS"] = 601
                response["EVENT_DETAILS"] = event_result
            else:
                response["STATUS"] = 602
        else:
            response["STATUS"] = 602

    else:
        response["STATUS"] = 602

    return response

