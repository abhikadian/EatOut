import simplejson as json
from math import radians, cos, sin, asin, sqrt
from CoreApp.Controllers.DatabaseObjects.userprofile_manage import get_user_id
from CoreApp.Controllers.DatabaseObjects.userfriends_manage import get_all_friends_of_user, get_user_from_user_id
from CoreApp.Controllers.DatabaseObjects.table_objects import event_table

# Find distance between coordinates

# def haversine(lon1, lat1, lon2, lat2):
#
#     # convert decimal degrees to radians
#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
#     # haversine formula
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * asin(sqrt(a))
#     miles = 6367 * c * 0.62137     # Multiply by 0.62137 to find distance in miles.
#     return miles

# distance = haversine(-74.010097, 40.640142, -74.012103, 40.636118)
# print(distance)


def get_nearby_events(request):
    request_body = json.loads(request.body.decode("utf-8"))

    events_response = {}

    if "USER_TOKEN" in request_body:

        user_id = get_user_id(request_body["USER_TOKEN"])
        if user_id != 0:
            all_events = event_table.scan()
            event_checker = []
            personal_events = []
            friends_events = []

            user_friends = get_all_friends_of_user(user_id)
            print("FriendList ", user_friends)
            for event in all_events["Items"]:

                # Check if personal events
                if user_id == event["EVENT_OWNER"] or user_id in event["EVENT_PARTICIPANTS"]:
                    if event["EVENT_ID"] not in event_checker:

                        all_participants = event["EVENT_PARTICIPANTS"]
                        participant_names = ""

                        for human in all_participants:
                            human_profile = get_user_from_user_id(human)
                            if human_profile is not None:
                                participant_names += human_profile["USER_NAME"] + "\n"

                        # Add Owner Name in names
                        owner_profile = get_user_from_user_id(user_id)
                        participant_names += owner_profile["USER_NAME"]

                        new_entry = {
                            "EVENT_ID": event["EVENT_ID"],
                            "EVENT_NAME": event["EVENT_NAME"],
                            "EVENT_LOCATION": event["EVENT_LOCATION_POINT"],
                            "EVENT_PARTICIPANT_NAMES": participant_names,
                            "EVENT_DATETIME": event["EVENT_DATETIME"],
                            "EVENT_LOCATION_TEXT": event["EVENT_LOCATION_TEXT"]
                        }
                        # new_entry["EVENT_PARTICIPANTS"].append(event["EVENT_OWNER"])
                        personal_events.append(new_entry)
                        print("Yes. Found a personal event")

                else:
                    if event["EVENT_TYPE"] == "CHECKIN":
                        # for friend in user_friends:
                        #     if friend["USER_ID"] == event["EVENT_OWNER"] or friend in event["EVENT_PARTICIPANTS"]:
                        all_participants = event["EVENT_PARTICIPANTS"]
                        participant_names = ""

                        for human in all_participants:
                            human_profile = get_user_from_user_id(human)
                            if human_profile is not None:
                                participant_names += human_profile["USER_NAME"] + "\n"

                        # Add Owner Name in names
                        owner_profile = get_user_from_user_id(user_id)
                        # participant_names += owner_profile["USER_NAME"]

                        new_entry = {
                            "EVENT_ID": event["EVENT_ID"],
                            "EVENT_NAME": event["EVENT_NAME"],
                            "EVENT_LOCATION": event["EVENT_LOCATION_POINT"],
                            "EVENT_PARTICIPANT_NAMES": participant_names,
                            "EVENT_DATETIME": event["EVENT_DATETIME"],
                            "EVENT_LOCATION_TEXT": event["EVENT_LOCATION_TEXT"]
                        }
                        # new_entry["EVENT_PARTICIPANTS"].append(event["EVENT_OWNER"])

                        friends_events.append(new_entry)
                        print("Yes. Found an event")

            events_response["STATUS"] = 501
            events_response["PERSONAL_EVENTS"] = personal_events
            events_response["FRIENDS_EVENTS"] = friends_events

        else:
            events_response["STATUS"] = 502

    else:
        events_response["STATUS"] = 502


    return events_response
