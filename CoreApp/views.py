import simplejson as json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from CoreApp.Controllers.LoginControllers import login_controller as login_controller
from CoreApp.Controllers.FriendsListControllers import modify_friends_list as modify_friends_list_controller
from CoreApp.Controllers.UserPreferenceControllers import user_preference_controller as user_preference_controller
from CoreApp.Controllers.UserReviewControllers import user_review_controller as user_review_controller
from CoreApp.Controllers.DatabaseObjects.userprofile_manage import get_user_id
from CoreApp.Controllers.DatabaseObjects.restaurantprofile_manage import retrieve_restaurant_profile
from CoreApp.Controllers.EventController import event_controller
from CoreApp.Controllers.NearbyEventController.nearby_events import get_nearby_events

#-------------------------- USER RELATED VIEWS --------------------------

@csrf_exempt
def test_login_user(request):
    resp = login_controller.test_login(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)


@csrf_exempt
def update_friends(request):
    resp = modify_friends_list_controller.modify_friends(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def get_friends(request):
    resp = modify_friends_list_controller.get_all_friends(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def update_preference(request):
    resp = user_preference_controller.update_user_preference(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def get_preference(request):
    resp = user_preference_controller.pull_preferences(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def update_reviews(request):
    resp = user_review_controller.update_review_for_user(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)


#------------------------ RESTAURANT RELATED VIEWS ----------------------

@csrf_exempt
def get_cuisines(request):
    print("request for cuisines list in views function")
    cuisine_list_response = {}
    request_body = json.loads(request.body.decode("utf-8"))
    if "USER_TOKEN" in request_body:
        user_id = get_user_id(request_body["USER_TOKEN"])
        if user_id == 0:
            print("invalid user token while updating preferences")
            cuisine_list_response["STATUS"] = 502
            return cuisine_list_response
        else:
            cuisines = [
                {'name':'American'},
                {'name':'Chinese'},
                {'name':'Italian'},
                {'name':'Mexican'},
                {'name':'Japanese'},
                {'name':'Caribbean'},
                {'name':'Spanish'},
                {'name':'Indian'},
                {'name':'Asian'},
                {'name':'Jewish'},
                {'name':'French'},
                {'name':'Thai'},
                {'name':'Korean'},
                {'name':'Mediterranean'},
                {'name':'Irish'},
                {'name':'Seafood'},
                {'name':'Middle Eastern'},
                {'name':'Greek'},
                {'name':'Vietnamese'},
                {'name':'Russian'},
                {'name':'Eastern European'},
                {'name':'African'},
                {'name':'Turkish'},
                {'name':'Soul Food'},
                {'name':'Continental'},
                {'name':'Pakistani'},
                {'name':'German'},
                {'name':'Fillipino'},
                {'name':'Polish'},
                {'name':'Brazilian'},
                {'name':'Ethiopian'},
                {'name':'Australian'},
                {'name':'English'},
                {'name':'Portugese'},
                {'name':'Egyptian'},
                {'name':'Indonesian'},
                {'name':'Chilean'},
                {'name':'Hawaiian'},
            ]
            cuisine_list_response["LIST_OF_CUISINES"] = cuisines


    else:
        cuisine_list_response["STATUS"] = 502

    return HttpResponse(json.dumps(cuisine_list_response), content_type="application/json", status=200)

@csrf_exempt
def get_restaurant_by_id(request):
    print("Request for Restaurant Profile")
    restaurant_response = {}
    request_body = json.loads(request.body.decode("utf-8"))
    if "USER_TOKEN" in request_body:
        user_id = get_user_id(request_body["USER_TOKEN"])
        if user_id == 0:
            print("invalid user token while updating preferences")
            restaurant_response["STATUS"] = 502

        else:
            if "RESTAURANT_ID" in request_body:
                restaurant_profile = retrieve_restaurant_profile(request_body["RESTAURANT_ID"])
                restaurant_response["STATUS"] = 501
                restaurant_response["PROFILE"] = restaurant_profile

            else:
                restaurant_response["STATUS"] = 502

    else:
        restaurant_response["STATUS"] = 502

    return HttpResponse(json.dumps(restaurant_response), content_type="application/json", status=200)

#-------------------------- EVENT RELATED VIEWS -------------------------

@csrf_exempt
def create_event(request):
    print(request)
    print(type(request))
    resp = event_controller.create_event_request(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def update_event(request):
    resp = event_controller.update_event(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def get_event_details(request):
    resp = event_controller.get_event_details_from_id(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def update_vote(request):
    print("Trying to update votes")
    resp = event_controller.update_event_vote(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def get_recommendations_event(request):
    resp = event_controller.get_event_recommendations(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)

@csrf_exempt
def get_neighborhoods(request):
    print("Request for Neighborhoods List")
    neighborhood_list = {}
    request_body = json.loads(request.body.decode("utf-8"))
    if "USER_TOKEN" in request_body:
        user_id = get_user_id(request_body["USER_TOKEN"])
        if user_id == 0:
            print("invalid user token while updating preferences")
            neighborhood_list["STATUS"] = 502

        else:
            neighborhoods = [
                {'name': 'Annandale'},
                {'name': 'Ardon Heights'},
                {'name': 'Astoria-Long Island City'},
                {'name': 'Auburndale'},
                {'name': 'Battery Park'},
                {'name': 'Bay Ridge'},
                {'name': 'Baychester'},
                {'name': 'Bayside'},
                {'name': 'Bedford Park'},
                {'name': 'Bedford-Stuyvesant'},
                {'name': 'Bensonhurst'},
                {'name': 'Bloomfield-Chelsea-Travis'},
                {'name': 'Boerum Hill'},
                {'name': 'Borough Park'},
                {'name': 'Brownsville'},
                {'name': 'Bushwick'},
                {'name': 'Canarsie'},
                {'name': 'Carnegie Hill'},
                {'name': 'Carroll Gardens'},
                {'name': 'Central Park'},
                {'name': 'Charlestown-Richmond Valley'},
                {'name': 'Chelsea'},
                {'name': 'Chinatown'},
                {'name': 'City Island'},
                {'name': 'Clearview'},
                {'name': 'Clifton'},
                {'name': 'Clinton'},
                {'name': 'Cobble Hill'},
                {'name': 'College Point'},
                {'name': 'Coney Island'},
                {'name': 'Corona'},
                {'name': 'Country Club'},
                {'name': 'Douglastown-Little Neck'},
                {'name': 'Downtown'},
                {'name': 'Dyker Heights'},
                {'name': 'East Brooklyn'},
                {'name': 'East Harlem'},
                {'name': 'East Village'},
                {'name': 'Eastchester'},
                {'name': 'Ettingville'},
                {'name': 'Financial District'},
                {'name': 'Flatbush'},
                {'name': 'Flushing'},
                {'name': 'Fordham'},
                {'name': 'Forest Hills'},
                {'name': 'Fort Green'},
                {'name': 'Fresh Kills'},
                {'name': 'Garment District'},
                {'name': 'Glendale'},
                {'name': 'Gramercy'},
                {'name': 'Gravesend-Sheepshead Bay'},
                {'name': 'Great Kills'},
                {'name': 'Greenwich Village'},
                {'name': 'Greenwood'},
                {'name': 'Hamilton Heights'},
                {'name': 'Harlem'},
                {'name': 'High Bridge'},
                {'name': 'Howard Beach'},
                {'name': 'Howland Hook'},
                {'name': 'Huguenot'},
                {'name': 'Hunts Point'},
                {'name': 'Inwood'},
                {'name': 'Jackson Heights'},
                {'name': 'Jamaica'},
                {'name': 'Kings Bridge'},
                {'name': 'Laurelton'},
                {'name': 'Little Italy'},
                {'name': 'Lower East Side'},
                {'name': 'Mapleton-Flatlands'},
                {'name': 'Mariners Harbor'},
                {'name': 'Maspeth'},
                {'name': 'Middle Village'},
                {'name': 'Midland Beach'},
                {'name': 'Midtown'},
                {'name': 'Morningside Heights'},
                {'name': 'Morris Heights'},
                {'name': 'Morris Park'},
                {'name': 'Mott Haven'},
                {'name': 'Murray Hill'},
                {'name': 'New Brighton'},
                {'name': 'Nkew Gardens'},
                {'name': 'North Sutton Area'},
                {'name': 'Oakwood'},
                {'name': 'Park Slope'},
                {'name': 'Parkchester'},
                {'name': 'Port Richmond'},
                {'name': 'Prince Bay'},
                {'name': 'Queens Village'},
                {'name': 'Queensboro Hill'},
                {'name': 'Red Hook'},
                {'name': 'Richmondtown'},
                {'name': 'Ridgewood'},
                {'name': 'Riverdale'},
                {'name': 'Rosebank'},
                {'name': 'Rosedale'},
                {'name': 'Rossville'},
                {'name': 'Saintalbans'},
                {'name': 'Soho'},
                {'name': 'Soundview'},
                {'name': 'South Beach'},
                {'name': 'South Bronx'},
                {'name': 'Springfield Gardens'},
                {'name': 'Spuyten Duyvil'},
                {'name': 'Steinway'},
                {'name': 'Sunny Side'},
                {'name': 'Sunset Park'},
                {'name': 'The Rockaways'},
                {'name': 'Throggs Neck'},
                {'name': 'Todt Hill'},
                {'name': 'Tottensville'},
                {'name': 'Tremont'},
                {'name': 'Tribeca'},
                {'name': 'Union Port'},
                {'name': 'University Heights'},
                {'name': 'Upper East Side'},
                {'name': 'Upper West Side'},
                {'name': 'Utopia'},
                {'name': 'Wakefield-Williamsbridge'},
                {'name': 'Washington Heights'},
                {'name': 'West Village'},
                {'name': 'Westerleigh-Castleton'},
                {'name': 'Whitestone'},
                {'name': 'Williams Bridge'},
                {'name': 'Williamsburg'},
                {'name': 'Woodhaven-Richmond Hill'},
                {'name': 'Woodlawn-Nordwood'},
                {'name': 'Woodrow'},
                {'name': 'Woodside'},
                {'name': 'Yorkville'}
            ]
            neighborhood_list["STATUS"] = 501
            neighborhood_list["NEIGHBORHOODS"] = neighborhoods

    else:
        neighborhood_list["STATUS"] = 502

    return HttpResponse(json.dumps(neighborhood_list), content_type="application/json", status=200)


@csrf_exempt
def get_allevents(request):
    resp = get_nearby_events(request)
    return HttpResponse(json.dumps(resp), content_type="application/json", status=200)


