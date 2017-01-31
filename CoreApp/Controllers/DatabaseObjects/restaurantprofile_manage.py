import json
from decimal import *
from CoreApp.Controllers.DatabaseObjects.table_objects import restaurant_table
from CoreApp.Controllers.RestaurantProfileController import restaurantprofile_controller

# Check if restaurant exists. If yes return result, if no return None
def get_restaurant_fron_id(restaurant_id):
    query_response = restaurant_table.get_item(
        Key = {
            'RESTAURANT_ID': restaurant_id,
        }
    )

    if 'Item' not in query_response:
        return None
    else:
        return query_response



def retrieve_restaurant_profile(restaurant_id):
    query_response = restaurant_table.get_item(
        Key={
            'RESTAURANT_ID': restaurant_id,
        }
    )

    if 'Item' not in query_response:
        print("Not Existing. Creating restaurant profile")
        yelp_restaurant_profile = restaurantprofile_controller.get_restaurant_profile(restaurant_id)
        result = create_new_restaurant_profile(yelp_restaurant_profile)
    else:
        print("Existing")
        result = query_response['Item']

    result["RESTAURANT_RATING"] = result["RESTAURANT_RATING"]
    result["RESTAURANT_LOCATION"][0] = result["RESTAURANT_LOCATION"][0]
    result["RESTAURANT_LOCATION"][1] = result["RESTAURANT_LOCATION"][1]

    return result


# Create new Restaurant Record
def create_new_restaurant_profile(restaurant_profile):
    cuisines = []

    for category in restaurant_profile['categories']:
        cuisines.append(category['title'])

    address = restaurant_profile['location']['display_address'][0]+', '+restaurant_profile['location']['display_address'][1]

    if 'hours' in restaurant_profile:
        timings = restaurant_profile['hours'][0]['open']
    else:
        timings = []

    new_restaurant_profile = {
        'RESTAURANT_ID' : restaurant_profile['id'],
        'RESTAURANT_NAME' : restaurant_profile['name'],
        'RESTAURANT_LOCATION' : [
                            Decimal(str(restaurant_profile['coordinates']['latitude'])),
                            Decimal(str(restaurant_profile['coordinates']['longitude']))
                ],
        'RESTAURANT_ADDRESS' : address,
        'RESTAURANT_PHONE' : restaurant_profile['phone'],
        'RESTAURANT_CUISINES' : cuisines,
        'RESTAURANT_PRICE' : len(restaurant_profile['price']),
        'RESTAURANT_PHOTO' : restaurant_profile['image_url'],
        'RESTAURANT_RATING' : Decimal(str(restaurant_profile['rating'])),
        'RESTAURANT_REVIEWCOUNT' : restaurant_profile['review_count'],
        'RESTAURANT_HOURS' : timings,
        'ITEMS_REVIEW': []
    }

    restaurant_table.put_item(
        Item = new_restaurant_profile
    )

    return new_restaurant_profile

# RESTAURANT_ID is same as the one given by YELP. Input is response object obtained after calling the api using business id
def check_if_restaurant_exists(restaurant_profile):
    print("In check rest exist")
    restaurant_id = restaurant_profile['id']
    print("Checking for id ", restaurant_id)
    query_response = get_restaurant_fron_id(restaurant_id)
    response = {
        'status' : "",
        'result' : ""
    }

    if query_response is None:
        print("Restaurant does not exist! Creating a record")
        return_profile = create_new_restaurant_profile(restaurant_profile)
        response['status'] = "New"
        response['result'] = return_profile

    else:
        print("Restaurant Exists")
        return_profile = query_response['Item']
        response['status'] = "Existing"
        response['result'] = return_profile

    return response


def update_restaurant_review(user_review):
    print("Incoming review: ", user_review)
    restaurant_id = user_review['RESTAURANT_ID']
    review_rating = user_review['RATING']
    review_items = user_review['ITEMS']

    restaurant_record = get_restaurant_fron_id(restaurant_id)

    if restaurant_record is not None:
        print("Found restaurant record ", restaurant_record['RESTAURANT_NAME'])

        print("Changing Rating")
        existing_rating = restaurant_record['RESTAURANT_RATING']
        existing_count = restaurant_record['RESTAURANT_REVIEWCOUNT']

        print("Existing Rating %r with count %r" %(existing_rating, existing_count))

        if review_rating is not None or review_rating != 0:
            total = (existing_rating * existing_count) + review_rating
            existing_count += 1
            new_rating = total / existing_count
            print("New rating is %r with review count %r" %(new_rating, existing_count))

            restaurant_record['RESTAURANT_RATING'] = Decimal(str(new_rating))
            restaurant_record['RESTAURANT_REVIEWCOUNT'] = existing_count

        restaurant_existing_items = restaurant_record['ITEMS_REVIEW']
        new_review_items = []
        for rev_item in review_items:
            print("Updating review of item ", rev_item['NAME'])
            item_exists = False
            for item in restaurant_existing_items:
                if rev_item['NAME'] in item['ITEM_NAME'] or item['ITEM_NAME'] in rev_item['NAME']:
                    item_exists = True
                    print("Item match found. Updating count")
                    if rev_item['LIKED'] == 'true':
                        item['ITEM_LIKE_COUNT'] += 1
                    else:
                        item['ITEM_DISLIKE_COUNT'] += 1

                    print(item)

            if not item_exists:
                print("Review item record does not exist. Creating record now.")
                new_item_record = {
                    'ITEM_NAME' : rev_item['NAME'],
                }
                if rev_item['LIKED'] == 'true':
                    new_item_record['ITEM_LIKE_COUNT'] = 1
                    new_item_record['ITEM_DISLIKE_COUNT'] = 0
                else:
                    new_item_record['ITEM_LIKE_COUNT'] = 0
                    new_item_record['ITEM_DISLIKE_COUNT'] = 1

                print(new_item_record)

                new_review_items.append(new_item_record)

        print("All reviews modified. Now updating table")

        for new_item in new_review_items:
            restaurant_existing_items.append(new_item)

        restaurant_record['ITEMS_REVIEW'] = restaurant_existing_items
        print(restaurant_record['ITEMS_REVIEW'])
        update_response = restaurant_table.put_item(
            Item = restaurant_record
        )

        print("Table updated ", update_response)

# Format of review
# sample_review = {
#     'RESTAURANT_ID' : 'malai-marke-indian-cuisine-new-york',
#     'RATING' : 4,
#     'ITEMS' : [
#         { 'NAME' : 'Paneer Makhni', 'LIKED' : 'true' },
#         { 'NAME' : 'Butter Chicken', 'LIKED' : 'true' }
#     ]
# }
#
#
#
# update_restaurant_review(sample_review)
