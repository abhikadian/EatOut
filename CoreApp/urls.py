from django.conf.urls import url
from . import views

urlpatterns = [
    # ------------------------------------------
    # User Login
    # ------------------------------------------

    # Input:
    # {FACEBOOK_ID, EMAIL_ID, USER_NAME, GENDER}
    # Output: { status: 101/102/103, user_token: }
    #    Status code 101 : New User.
    #    Status code 102 : Existing User
    #    Status code 103 : Bad Request / Missing Data

    url(r'user/test_login$', views.test_login_user, name='test_login_user'),

    # ------------------------------------------
    # Update Friends List
    # ------------------------------------------
    # Input:
    # {USER_TOKEN, [LIST_OF_FRIENDS_FACEBOOK_IDS]}
    # Output: { status: 201/202}

    url(r'user/update_friends$', views.update_friends, name='update_friends'),

    # ------------------------------------------
    # Get Friends List
    # ------------------------------------------
    # Input:
    # {USER_TOKEN}
    # Output: { STATUS: 201/202,
    #           FRIENDS: [
    #               {USER RECORD}, {USER RECORD}, ..
    #           ]
    # }

    url(r'user/get_friends$', views.get_friends, name='get_friends'),

    # ----------------------------------------------
    # Update Preferences
    # ----------------------------------------------
    # Input:
    # {USER_TOKEN, [PREFERENCES]}
    # Output: { status: 301/302/303}
    # 301 : successfully updated the preferences
    # 302 : incorrect user_token
    # 303 : something wrong with the database, try again/incorrect sub-keys in the preference key
    # PREFERENCES : {LIST_OF_PRIMARY_CUISINES:[STRINGS],
    #                PRICE_RANGE : INTEGER,
    #                LIST_OF_FAVOURITE_ITEMS : [STRINGS],
    #                LIST_OF_SECONDARY_CUISINES:[STRINGS],
    #                MINIMUM_RATING : FLOAT,
    #                DISTANCE_RADIUS : FLOAT
    # }

    url(r'user/update_preference$', views.update_preference, name='update_preference'),

    # ----------------------------------------------
    # Update Preferences
    # ----------------------------------------------
    # Input:
    # {USER_TOKEN}
    url(r'user/get_preference$', views.get_preference, name='get_preference'),

    # ----------------------------------------------
    # Update Reviews
    # ----------------------------------------------
    # Input:
    # {USER_TOKEN, [REVIEWS]}
    # Output: { status: 401/402/403}
    # 401 : successfully updated the reviews
    # 402 : incorrect user_token
    # 403 : something wrong with the database, try again/incorrect sub-keys in the reviews key
    # REVIEWS : { RESTAURANT_ID (you get it from the event creation API),
    #                RATING : 1,2 or 3 (like, dislike or neutral),
    #                OVERALL_RESTAURANT_REVIEW : STRING,  {REMOVE FOR NOW}
    #                ITEMS : (list of items)[
    #                      { NAME : STRING,
    #                      LIKED : STRING "TRUE"  or "FALSE",
    #                      },
    #
    #                      { NAME : STRING,
    #                      LIKED : STRING "TRUE"  or "FALSE",
    #                      },
    #                ]
    # }
    url(r'user/update_reviews$', views.update_reviews, name='update_reviews'),

    # ----------------------------------------------
    # get cuisines
    # ----------------------------------------------
    # Input:
    # {USER_TOKEN}
    # Output: { STATUS: 501/502 (success/ incorrect user token),
    #  LIST_OF_CUISINES : [list of cuisines]
    # }

    url(r'restaurant/get_cuisines$', views.get_cuisines, name='get_cuisines'),

    url(r'restaurant/get_restaurant_details$', views.get_restaurant_by_id, name='get_restaurant'),

    # ----------------------------------------------
    # Create Event
    # ----------------------------------------------
    # Input:
    # {
    #   USER_TOKEN,
    #   EVENT_DETAILS : {
    #       NAME : String
    #       Type: String    (Private/Checkin)
    #       PARTICIPANTS: [] Array of user ids
    #       PREFERENCES: []  Array of cuisines
    #       LOCATION: String E.g. East Village
    #   }
    # }
    # Output: { STATUS: 501/502 (success/ incorrect user token),
    #  LIST_OF_CUISINES : [list of cuisines]
    # }

    url(r'event/create$', views.create_event, name='create_event'),

    url(r'event/update$', views.update_event, name='update_event'),

    url(r'event/getevent$', views.get_event_details, name='get_event'),

    # ----------------------------------------------
    # Get all events to display on map
    # ----------------------------------------------
    # Input:
    # { USER_TOKEN }
    # Output: {
    #   STATUS : 501/502 (success/ incorrect user token),
    #   PERSONAL_EVENTS : []    Every Event --> {"EVENT_ID": "", "EVENT_LOCATION": [lat, lon], "EVENT_PARTICIPANTS": ["lsit of user ids"]}
    #   FRIENDS_EVENTS : []
    # }
    url(r'event/getall$', views.get_allevents, name='get_allevents'),

    # ----------------------------------------------
    # get neighborhoods
    # ----------------------------------------------
    # Input:
    # {USER_TOKEN}
    # Output: { STATUS: 501/502 (success/ incorrect user token),
    #  NEIGHBORHOODS : [list of neighborhoods]
    # }

    url(r'event/get_neighborhoods$', views.get_neighborhoods, name='get_neighborhoods'),

    # ----------------------------------------------
    # Update vote of restaurants
    # ----------------------------------------------
    # Input:
    # {USER_TOKEN, VOTES : ["RESTAURANT1", "RESTAURANT2", ..]}
    # Output: { STATUS: 601/602 (success/ incorrect user token),
    #  VOTE_COUNT: []
    # }

    url(r'event/update_vote$', views.update_vote, name='update_vote'),

    # Get recommendations for
    url(r'event/get_recommendation_list$', views.get_recommendations_event, name='get_recommendations'),
]
