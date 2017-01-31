import requests, json
from yelp.client import Client
from configparser import ConfigParser
from yelp.oauth1_authenticator import Oauth1Authenticator
from CoreApp.Controllers.DatabaseObjects.table_objects import user_preference_table
# from CoreApp.Controllers.DatabaseObjects.restaurantprofile_manage import retrieve_restaurant_profile

config_secrets = ConfigParser()
config_secrets.read('config.ini')

# API AUTHENTICATION
# Changes --> commented block
# auth = Oauth1Authenticator(
#    consumer_key = config_secrets["YELP"]["yelp_consumer_key"],
#    consumer_secret = config_secrets["YELP"]["yelp_consumer_secret"],
#    token = config_secrets["YELP"]["yelp_token"],
#    token_secret = config_secrets["YELP"]["yelp_token_secret"]
# )
# client = Client(auth)
# Changes End

data = {
    'grant_type':'client_credentials',
    'client_id': config_secrets["YELP"]["yelp_app_id"],
    'client_secret': config_secrets["YELP"]["yelp_app_secret"]
 }

token = requests.post('https://api.yelp.com/oauth2/token', data = data)
access_token = token.json()['access_token']
headers =  {'Authorization': 'bearer %s' % access_token}

def event_restsearch_avgprice(user_ids):
    count = 0
    sum = 0.0
    for i in user_ids:
       preferences = user_preference_table.get_item(
           Key = {
                 'USER_ID' : i
           }
       )
       sum += float(preferences['Item']['PREFERENCES']['PRICE_RANGE'])
       count+=1
    return int(sum//count)


def rest_get_preferences(user_ids, location, preferences):
    if len(preferences)==1:
        limitItems = 10
    elif len(preferences)==2:
        limitItems = 6
    elif len(preferences)==3:
        limitItems =4
    else:
        limitItems=3

    restaurant_result = []
    average_price = event_restsearch_avgprice(user_ids)
    for i in preferences:
        params = {
            'term': i,
            'latitude': location[0],
            'longitude': location[1],
            'sort_by': 'best_match',
            'limit': 5,
            'price': average_price,
            'radius': 3000
        }
        url = 'https://api.yelp.com/v3/businesses/search'
        resp = requests.get(url=url, params=params, headers=headers)
        data = json.loads(resp.text)

        for i in data['businesses']:
            restaurant = {
                "RESTAURANT_ID": i["id"],
                "RESTAURANT_NAME": i["name"]
            }
            restaurant_result.append(restaurant)

    return restaurant_result

# Changes --> Commented Block
# def rest_get_preferences(location, preferences):
#     if len(preferences)==1:
#         limitItems = 10
#     elif len(preferences)==2:
#         limitItems = 6
#     elif len(preferences)==3:
#         limitItems =4
#     else:
#         limitItems=3
#
#     restaurant_result = []
#
#     for i in preferences:
#         params = {
#             'term': i,
#             'lang': 'en',
#             'limit': limitItems,
#             'sort': 0,
#             'radius_filter': 3000
#         }
#         results = client.search_by_coordinates(location[0],location[1], **params)
#         for business in results.businesses:
#             restaurant = {
#                 "RESTAURANT_ID": business.id,
#                 "RESTAURANT_NAME": business.name
#             }
#             restaurant_result.append(restaurant)
#
#     return restaurant_result

# location = [40.694558, -73.986599]
# preferences = ['indian', 'chinese']
# restaurant_result = []
# rest_get_preferences(location,preferences)