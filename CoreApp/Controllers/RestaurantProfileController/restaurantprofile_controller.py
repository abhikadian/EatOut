import pprint, requests, json
from yelp.client import Client
from configparser import ConfigParser
from yelp.oauth1_authenticator import Oauth1Authenticator
from CoreApp.Controllers.DatabaseObjects import restaurantprofile_manage as restaurant

config_secrets = ConfigParser()
config_secrets.read('config.ini')

# API AUTHENTICATION

auth = Oauth1Authenticator(
   consumer_key = config_secrets["YELP"]["yelp_consumer_key"],
   consumer_secret = config_secrets["YELP"]["yelp_consumer_secret"],
   token = config_secrets["YELP"]["yelp_token"],
   token_secret = config_secrets["YELP"]["yelp_token_secret"]
)

client = Client(auth)

data = {
   'grant_type' : 'client_credentials',
   'client_id' : config_secrets['YELP']['yelp_app_id'],
   'client_secret' : config_secrets['YELP']['yelp_app_secret']
}

token = requests.post('https://api.yelp.com/oauth2/token', data=data)
access_token = token.json()['access_token']
headers =  {'Authorization': 'bearer %s' % access_token}
getparams = {
   'lang':'en'
}

# SEARCH PARAMETERS

# params = {
#    'term': 'Indian',
#    'lang': 'en',
#    'limit': 15,
#    'sort': 0,
#    'radius_filter': 10000,
# }
#
# search_location = {
#     'lat' : 40.694558,
#     'long' : -73.986599,
# }


# Makes YELP call to search based on search parameters. Returns a list of restaurants.
# def update_restaurants_from_list_ids(list_of_rest):
#
#     restaurant_results = []
#
#     for rest in list_of_rest:
#         url = 'https://api.yelp.com/v3/businesses/' + rest["RESTAURANT_ID"]
#         print(rest["RESTAURANT_ID"])
#         yelp_restaurant_profile = requests.get(url = url, params = getparams, headers = headers).json()
#         print(yelp_restaurant_profile)
#         result = restaurant.check_if_restaurant_exists(yelp_restaurant_profile)
#         restaurant_results.append(result)
#
#     return restaurant_results

def get_restaurant_profile(restaurant_id):
    url = 'https://api.yelp.com/v3/businesses/' + restaurant_id
    yelp_restaurant_profile = requests.get(url=url, params=getparams, headers=headers).json()
    print(yelp_restaurant_profile)
    return yelp_restaurant_profile
