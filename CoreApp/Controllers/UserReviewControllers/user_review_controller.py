import json
from CoreApp.Controllers.DatabaseObjects.table_objects import user_review_table
from CoreApp.Controllers.DatabaseObjects.userprofile_manage import get_user_id
from CoreApp.Controllers.DatabaseObjects.restaurantprofile_manage import update_restaurant_review

def update_review_for_this_user(user_id, reviews):
    # review is already a json
    print("trying to open the review data")
    if "RESTAURANT_ID" in reviews:
        restaurant_id = reviews["RESTAURANT_ID"]
    else:
        return False

    if "RATING" in reviews:
        overall_rating = reviews["RATING"]
    else:
        overall_rating = None

    # if "OVERALL_RESTAURANT_REVIEW" in reviews:
    #     overall_review = reviews["OVERALL_RESTAURANT_REVIEW"]
    # else:
    #     overall_review = None

    if "ITEMS" in reviews:
        items = reviews["ITEMS"]
    else:
        items = None

    update_response = user_review_table.put_item(
        Item={
            'USER_ID': user_id,
            'RESTAURANT_ID': str(restaurant_id),
            'RATING': overall_rating,
            # 'OVERALL_RESTAURANT_REVIEW': overall_review,
            'ITEMS': items,
        },
    )

    print("UpdateReviews succeeded:")
    print("update reviews response ", update_response)
    code = update_response["ResponseMetadata"]["HTTPStatusCode"]
    print("update reviews list response ", code)
    if code == 200:
        return True
    else:
        return False


def update_review_for_user(request):
    print("Request for updating user review")
    update_user_review_response = {}
    request_body = json.loads(request.body.decode("utf-8"))
    if "USER_TOKEN" in request_body:
        user_id = get_user_id(request_body["USER_TOKEN"])
        if user_id == 0:
            print("invalid user token while updating preferences")
            update_user_review_response["STATUS"] = 402
            return update_user_review_response
        else:
            # The user_token exists and is correct
            if "REVIEWS" in request_body:
                reviews = request_body["REVIEWS"]
                update_status = update_review_for_this_user(user_id, reviews)
                if update_status:
                    # Update review for the restaurant in here
                    update_restaurant_review(reviews)
                    update_user_review_response["STATUS"] = 401
                    return update_user_review_response
                else:
                    update_user_review_response["STATUS"] = 403
                    return update_user_review_response
            else:
                update_user_review_response["STATUS"] = 402
                return update_user_review_response

    else:
        update_user_review_response["STATUS"] = 402
        return update_user_review_response
