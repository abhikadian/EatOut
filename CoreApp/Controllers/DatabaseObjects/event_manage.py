import uuid
import googlemaps
from decimal import *
from pyfcm import FCMNotification
from configparser import ConfigParser
from CoreApp.Controllers.DatabaseObjects.table_objects import event_table
from CoreApp.Controllers.DatabaseObjects.userprofile_manage import get_user_from_user_id
from CoreApp.Controllers.Recommendation.RecommendationParams import rest_get_preferences

secret = ConfigParser()
secret.read('config.ini')

push_service = FCMNotification(api_key="API KEY HERE")

def generate_event(user_id, event_details):
    # Generate unique event id
    event_id = "EI_" + str(uuid.uuid4())

    event_location = event_details['LOCATION']

    maps = googlemaps.Client(key = secret["GOOGLEAPI"]["key"])
    geocode_result = maps.geocode(event_location+', New York, NY')
    coordinates = [Decimal(str(geocode_result[0]['geometry']['location']['lat'])),
                   Decimal(str(geocode_result[0]['geometry']['location']['lng']))]

    # Get Name and Firebase Id of friends

    participant_names = ""
    participant_firebase = []

    all_participants = event_details["PARTICIPANTS"]

    for human in all_participants:
        human_profile = get_user_from_user_id(human)
        if human_profile is not None:
            participant_names += human_profile["USER_NAME"] + "\n"
            participant_firebase.append(human_profile["FIREBASE_ID"])

    # Add Owner Name in names
    owner_profile = get_user_from_user_id(user_id)
    participant_names += owner_profile["USER_NAME"]
    participant_firebase.append(owner_profile["FIREBASE_ID"])

    #-------------------------------------

    new_event_record = {
        "EVENT_ID" : event_id,
        "EVENT_OWNER" : user_id,
        "EVENT_NAME" : event_details["NAME"],
        "EVENT_TYPE" : event_details["TYPE"],
        "EVENT_DATETIME" : event_details["DATETIME"],
        "EVENT_PARTICIPANTS" : all_participants,
        "EVENT_PARTICIPANT_FIREBASE": participant_firebase,
        "EVENT_LOCATION_POINT" : coordinates,
        "EVENT_LOCATION_TEXT" : event_location,
        "EVENT_PREFERENCES" : event_details['PREFERENCES'],
        "EVENT_RESTAURENTSELECT" : "None",
        "EVENT_ISFINISHED" : "False"
    }

    # Changes Begin
    list_of_userids = event_details["PARTICIPANTS"]
    list_of_userids.append(user_id)

    event_recom = generate_recommendations(list_of_userids, new_event_record["EVENT_LOCATION_POINT"],
                                           new_event_record["EVENT_PREFERENCES"])
    new_event_record["RECOMMENDATIONS"] = event_recom

    # Changes End

    # Changes --> Commented Block
    # event_recom = generate_recommendations(new_event_record["EVENT_LOCATION_POINT"],new_event_record["EVENT_PREFERENCES"])
    # new_event_record["RECOMMENDATIONS"] = event_recom

    create_respose = event_table.put_item(
        Item = new_event_record
    )

    pref_string = ""
    for pref in event_details['PREFERENCES']:
        pref_string += pref + "\n"

    pref_string = pref_string[:-1]

    return_record = {
        "EVENT_ID": event_id,
        "EVENT_NAME": event_details["NAME"],
        "EVENT_TYPE": event_details["TYPE"],
        "EVENT_DATETIME": event_details["DATETIME"],
        "EVENT_PARTICIPANT_NAMES" : participant_names,
        "EVENT_LOCATION_TEXT" : event_location,
        "EVENT_PREFERENCES": pref_string,
        "EVENT_ISFINISHED" : "False"

    }

    # new_event_record["EVENT_LOCATION_POINT"][0] = float(new_event_record["EVENT_LOCATION_POINT"][0])
    # new_event_record["EVENT_LOCATION_POINT"][1] = float(new_event_record["EVENT_LOCATION_POINT"][1])

    # return new_event_record

    # =============NOTIFICATION=====================
    # api key in config file
    message_title = "A new EatOut Event"
    message_body = "Hi! "+owner_profile["USER_NAME"]+" has invited you to an event."
    result = push_service.notify_multiple_devices(registration_ids=participant_firebase, message_title=message_title,message_body=message_body)
    print(result)
    # ==============================================


    print("EVENT CREATION COMPLETE")
    return return_record

def update_event_record(event_details):
    event_id = event_details["EVENT_ID"]

    event_record = get_event(event_id)

    if event_record is not None:
        event_location = event_details["LOCATION"]

        if event_details["LOCATION"] == "":
            maps = googlemaps.Client(key = secret["GOOGLEAPI"]["key"])
            geocode_result = maps.geocode(event_location + ', New York, NY')
            coordinates = [Decimal(str(geocode_result[0]['geometry']['location']['lat'])),
                           Decimal(str(geocode_result[0]['geometry']['location']['lng']))]
        else:
            coordinates = event_details["EVENT_LOCATION_POINT"]

        # Get Name and Firebase Id of friends

        participant_names = ""
        participant_firebase = []

        all_participants = event_details["PARTICIPANTS"]

        for human in all_participants:
            human_profile = get_user_from_user_id(human)
            if human_profile is not None:
                participant_names += human_profile["USER_NAME"] + "\n"
                participant_firebase.append(human_profile["FIREBASE_ID"])

        # Add Owner Name in names
        owner_profile = get_user_from_user_id(event_details['EVENT_OWNER'])
        participant_names += owner_profile["USER_NAME"]
        participant_firebase.append(owner_profile["FIREBASE_ID"])

        # -------------------------------------

        update_event = {
            "EVENT_ID": event_id,
            "EVENT_OWNER": event_details['EVENT_OWNER'],
            "EVENT_NAME": event_details["NAME"],
            "EVENT_TYPE": event_details["TYPE"],
            "EVENT_DATETIME": event_details["DATETIME"],
            "EVENT_PARTICIPANTS": all_participants,
            "EVENT_PARTICIPANT_FIREBASE": participant_firebase,
            "EVENT_LOCATION_POINT": coordinates,
            "EVENT_LOCATION_TEXT": event_location,
            "EVENT_PREFERENCES": event_details["PREFERENCES"],
            "EVENT_RESTAURENTSELECT": event_details["EVENT_RESTAURENTSELECT"],
            "EVENT_ISFINISHED": event_details["EVENT_ISFINISHED"]
        }

        # Changes --> Commented Block
        # event_recom = generate_recommendations(update_event["EVENT_LOCATION_POINT"], update_event["EVENT_PREFERENCES"])
        # update_event["RECOMMENDATIONS"] = event_recom

        # Changes Begin
        list_of_userids = event_details["PARTICIPANTS"]
        list_of_userids.append(event_details["EVENT_OWNER"])
        event_recom = generate_recommendations(list_of_userids, update_event["EVENT_LOCATION_POINT"],
                                               update_event["EVENT_PREFERENCES"])
        update_event["RECOMMENDATIONS"] = event_recom
        # Changes End

        create_respose = event_table.put_item(
            Item = update_event
        )

        pref_string = ""
        for pref in event_details['PREFERENCES']:
            pref_string += pref + "\n"

        pref_string = pref_string[:-1]

        return_record = {
            "EVENT_ID": event_id,
            "EVENT_NAME": event_details["NAME"],
            "EVENT_TYPE": event_details["TYPE"],
            "EVENT_DATETIME": event_details["DATETIME"],
            "EVENT_PARTICIPANT_NAMES": participant_names,
            "EVENT_LOCATION_TEXT": event_location,
            "EVENT_PREFERENCES": pref_string,
            "EVENT_RESTAURENTSELECT": event_details["EVENT_RESTAURENTSELECT"],
            "EVENT_ISFINISHED": event_details["EVENT_ISFINISHED"]
        }

        # update_event["EVENT_LOCATION_POINT"][0] = float(update_event["EVENT_LOCATION_POINT"][0])
        # update_event["EVENT_LOCATION_POINT"][1] = float(update_event["EVENT_LOCATION_POINT"][1])

        # =============NOTIFICATION=====================
        # ==============================================

        return return_record
    else:
        return None


def get_event(event_id):
    event_details = event_table.get_item(
        Key = {
            'EVENT_ID' : event_id
        }
    )

    if event_details['Item'] is not None:
        return event_details['Item']
    else:
        return None

def get_event_ui(event_id):
    event_record = event_table.get_item(
        Key={
            'EVENT_ID': event_id
        }
    )

    event_details = event_record['Item']

    if event_details is not None:

        pref_string = ""
        for pref in event_details['EVENT_PREFERENCES']:
            pref_string += pref + "\n"

        pref_string = pref_string[:-1]

        all_participants = event_details["EVENT_PARTICIPANTS"]
        participant_names = ""

        for human in all_participants:
            human_profile = get_user_from_user_id(human)
            if human_profile is not None:
                participant_names += human_profile["USER_NAME"] + "\n"

        # Add Owner Name in names
        owner_profile = get_user_from_user_id(event_details['EVENT_OWNER'])
        # participant_names += owner_profile["USER_NAME"]
        owner_token = owner_profile["USER_TOKEN"]

        return_record = {
            "EVENT_ID": event_id,
            "EVENT_NAME": event_details["EVENT_NAME"],
            "EVENT_TYPE": event_details["EVENT_TYPE"],
            "EVENT_DATETIME": event_details["EVENT_DATETIME"],
            "EVENT_PARTICIPANT_NAMES": participant_names,
            "EVENT_LOCATION_TEXT": event_details["EVENT_LOCATION_TEXT"],
            "EVENT_PREFERENCES": pref_string,
            "EVENT_RESTAURENTSELECT": event_details["EVENT_RESTAURENTSELECT"],
            "EVENT_ISFINISHED": event_details["EVENT_ISFINISHED"],
            "EVENT_OWNER_TOKEN": owner_token
        }

        print(return_record)

        return return_record
    else:
        print("Returning none!!!")
        return None

def generate_recommendations(list_of_userids, location, preferences):
    list_of_ids = rest_get_preferences(list_of_userids, location, preferences)
    # update_restaurants_from_list_ids(list_of_ids)
    return list_of_ids
