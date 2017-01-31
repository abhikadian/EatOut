import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamo_db = boto3.resource('dynamodb')
print("DynamoDB Connection Successful")

#-------------------- USER TABLES --------------------#

user_profile_table = dynamo_db.Table('UserProfileTable')
user_friend_table = dynamo_db.Table('UserFriendTable')
user_preference_table = dynamo_db.Table('UserPreferenceTable')
user_review_table = dynamo_db.Table('UserReviewTable')

#----------------- RESTAURANT TABLES -----------------#

restaurant_table = dynamo_db.Table('RestaurantTable')

#------------------- EVENT TABLES -------------------#

event_table = dynamo_db.Table('EventTable')

votebank_table = dynamo_db.Table('VoteBankTable')

votecount_table = dynamo_db.Table('VoteCountTable')

test = dynamo_db.Table('Test')
#
#
# resp = test.update_item(
#     Key={
#         "EVENT": "EVENT1",
#         "USER": "USER1"
#     },
#     UpdateExpression = "set VOTES = :v",
#     ExpressionAttributeValues = {
#         ":v" : ["REST1","REST3"]
#     }
# )
#
# print(resp)
#
# resp = test.query(
#     KeyConditionExpression = Key('EVENT').eq("EVENT1")
# )
# print(resp['Items'])
