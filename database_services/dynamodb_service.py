import json
import logging
import boto3
import time
import uuid
from pprint import pprint
from botocore.exceptions import ClientError

import middleware.context as context
import database_services.dynamodb_secrets as secrets
from database_services.dynamodb_errors import DynmamoDBErrors as e

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DynamoDBServiceException(Exception):
    def __init__(self, msg):
        self.msg = msg


dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=secrets.AWS_ACCESS_KEY,
                          aws_secret_access_key=secrets.AWS_SECRET_KEY,
                          region_name=secrets.AWS_REGION_NAME)


# other_client = boto3.client("dynamodb")

table = dynamodb.Table('comment-response')


# TODO: incoorporate offset, limit/pagination
def fetch_all_comments():
    """
    Retrieves all comments for all items
    Returns: A list of all comments in dynamoDB
    """
    response = table.scan()
    data = response['Items']
    return data

#pprint(fetch_all_comments())

# TODO: incoorporate offset, limit/pagination
def fetch_all_comments_by_template(template):
    """
    retrieves all comments that match template
    template: dict.  eg. {item_id: 1}
    Note: This template can only be for top level/ Comment attributes.
    DynamoDB doesn't have a feature to filter the data present in the Map inside the List data type,
    unless you know the entire value for the response which seems irrelevant
    """
    fe = ' AND '.join(['{0}=:{0}'.format(k) for k, v in template.items()])
    ea = {':{}'.format(k): v for k, v in template.items()}

    result = table.scan(
        FilterExpression=fe,
        ExpressionAttributeValues=ea
    )
    return result['Items']

#pprint(fetch_all_comments_by_template({"commenter_id": "talya"}))

def fetch_comment_by_id(comment_id_value):
    """
    retrieves the comment with comment_id=comment_id
    comment_id_value: string
    """
    rsp = table.get_item(Key={'comment_id': comment_id_value})
    response = rsp.get('Item', None)
    return response
pprint(fetch_comment_by_id('3e0ab1b0-df48-4c65-b238-e3b4ccd8ee76'))

def get_comments_by_item_id(item_id):
    """
    retrieves all comments under the given item id
    item_id: string
    """
    return fetch_all_comments_by_template({'item_id': item_id})


#pprint(fetch_comment_by_id('2'))

def add_response(comment_id, responder_id, response_text):
    """
    Posts a response under a comment id
    comment_id: the comment_id the response will be under
    responder_id: the user posting the response
    response_text: the response_text field in the response object
    (See add_response in ferguson code)
    """
    Key = {
        "comment_id": comment_id
    }
    dt = time.time()
    dts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt))

    full_rsp = {
        "responder_id": responder_id,
        "datetime": dts,
        "response_text": response_text,
        "response_id": str(uuid.uuid4()),
        "version_id": str(uuid.uuid4())
    }
    UpdateExpression = "SET responses = list_append(responses, :i)"
    ExpressionAttributeValues = {
        ':i': [full_rsp]
    }
    ReturnValues = "UPDATED_NEW"

    res = table.update_item(
        Key=Key,
        UpdateExpression=UpdateExpression,
        ExpressionAttributeValues=ExpressionAttributeValues,
        ReturnValues=ReturnValues
    )

    return None, res

#add_response('1', 'maya', 'adding a response!')
#pprint(fetch_all_comments())

def post_comment(item_id, commenter_id, comment_text):
    """
    Posts a new comment
    commenter_id: the user posting the comment
    commenter_text: the comment_text field in the comment object
    (See add_comment in ferguson code)
    """
    dt = time.time()
    dts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt))

    item = {
        "comment_id": str(uuid.uuid4()),
        "version_id": str(uuid.uuid4()),
        "commenter_id": commenter_id,
        "comment_text": comment_text,
        "datetime": dts,
        "item_id": item_id,
        "responses": []
    }
    res = table.put_item(Item=item)
    return None, res


# post_comment('4','jake', 'comment about item 4!')
# pprint(fetch_all_comments())


def update_comment(comment_id, old_version_id, commenter_id, new_comment_text):
    """
    updates a comment with id=comment_id only if old_version_id==version_id of the comment with comment_id
    comment_id: the id of the comment to update
    commenter_id: the id of the commenter updating the comment
    new_comment_text: the new text of the comment

    this function needs to:
    1. verify that commenter_id= commenter_id
    2. update conditionally based on the version number of the old comment.
    (see write_comment_if_not_changed in ferguson code)
    """
    comment_to_update = fetch_comment_by_id(comment_id)

    if comment_to_update['commenter_id'] != commenter_id:
        return e.WRONG_USER, "Users may not edit other users comments"

    dt = time.time()
    dts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt))
    new_version_id = str(uuid.uuid4())

    try:
        res = table.update_item(
            Key= {
                'comment_id': comment_id
            },
            UpdateExpression="SET version_id = :new_version_id, comment_text = :new_comment_text, #dts = :dts",
            ConditionExpression="version_id=:old_version_id",
            ExpressionAttributeValues={":old_version_id": old_version_id,":new_comment_text": new_comment_text,
                                       ":new_version_id": new_version_id, ":dts": dts},
            ExpressionAttributeNames= {"#dts": "datetime"}
        )
    except ClientError as err:
        if err.response['Error']['Code']=='ConditionalCheckFailedException':
            return e.WRITE_WRITE_CONFLICT, "VersionID incorrect- Write Write conflict"
        else:
            return e.COMMENT_NOT_FOUND, "Update failed"

    return None, res

#update_comment("3e0ab1b0-df48-4c65-b238-e3b4ccd8ee76", '1234', 'TK', 'new comment')
# pprint(fetch_all_comments())
# pprint(fetch_comment_by_id('d9d6b8ec-9a0a-49ce-a17e-de091b184fd8'))


def update_response(comment_id, response_id, new_response_text, responder_id, old_version_id):
    """
    same as update comment but for response
    This post shows how to update one map item in a list in dynamo
    https://stackoverflow.com/questions/36799604/update-list-element-in-dynamodb
    I think flow will have to be: iterate through the list to find the index where response_id=response_id,
    then follow the stackoverflow format
    """
    comment_to_update = fetch_comment_by_id(comment_id)

    if comment_to_update is None:
        return e.COMMENT_NOT_FOUND, "Parent comment could not be found!"

    comment_responses = comment_to_update["responses"]
    index_of_response_to_update = -1

    for idx, resp in enumerate(comment_responses):
        if resp["response_id"] == response_id:
            index_of_response_to_update = idx
            break

    if index_of_response_to_update == -1:
        return e.COMMENT_NOT_FOUND, "The requested response could not be found."

    if comment_responses[index_of_response_to_update]['responder_id'] != responder_id:
        return e.WRONG_USER, "Users may not edit other users comments"

    dt = time.time()
    dts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt))
    new_version_id = str(uuid.uuid4())
    try:
        res = table.update_item(
            Key={
                'comment_id': comment_id
            },
            UpdateExpression=f"SET responses[{index_of_response_to_update}].response_text = :new_response_text, " +
                                 f"responses[{index_of_response_to_update}].version_id = :new_version_id, " +
                                 f"responses[{index_of_response_to_update}].#dts = :dts",
            ConditionExpression=f"responses[{index_of_response_to_update}].version_id=:old_version_id",
            ExpressionAttributeValues={":new_response_text": new_response_text,
                                       ":new_version_id": new_version_id,
                                       ":dts": dts,
                                       ":old_version_id": old_version_id},
            ExpressionAttributeNames={"#dts": "datetime"}
        )
    except ClientError as err:
        if err.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return e.WRITE_WRITE_CONFLICT, "VersionID incorrect- Write Write conflict"
        else:
            print(err)
            return e.COMMENT_NOT_FOUND, "Update failed"
    return None, res


def delete_comment(comment_id, commenter_id):
    """
    deletes a comment with comment_id=comment_id
    deleting a comment deletes all the responses to the comment
    needs to verify that the user deleting the comment is same as user who created the comment
    """
    comment_to_update = fetch_comment_by_id(comment_id)

    if comment_to_update is None:
        return e.COMMENT_NOT_FOUND, "Parent comment could not be found!"

    if comment_to_update['commenter_id'] != commenter_id:
        return e.WRONG_USER, "Users may not delete other users comments"

    res = table.delete_item(
        Key={
            'comment_id': comment_id
        }
    )

    return None, res


def delete_response(comment_id, response_id, responder_id):
    """
    deletes a response with response_id = responder_id
    needs to verify that the user deleting the response is the same as the user who created the response
    """
    comment_to_update = fetch_comment_by_id(comment_id)

    if comment_to_update is None:
        return e.COMMENT_NOT_FOUND, "Parent comment could not be found!"

    comment_responses = comment_to_update["responses"]
    index_of_response_to_update = -1

    for idx, resp in enumerate(comment_responses):
        if resp["response_id"] == response_id:
            index_of_response_to_update = idx
            break

    if index_of_response_to_update == -1:
        return e.COMMENT_NOT_FOUND, "The requested response could not be found."

    if comment_responses[index_of_response_to_update]['responder_id'] != responder_id:
        return e.WRONG_USER, "Users may not delete other users responses"

    res = table.update_item(
        Key={
            'comment_id': comment_id
        },
        UpdateExpression=f"REMOVE responses[{index_of_response_to_update}]"
    )

    return None, res


def fetch_single_response(comment_id, response_id):
    """
    fetches a response with response_id = responder_id
    """
    comment_to_look_in = fetch_comment_by_id(comment_id)

    if comment_to_look_in is None:
        return e.COMMENT_NOT_FOUND, "Parent comment could not be found!"

    comment_responses = comment_to_look_in["responses"]
    index_of_response_to_fetch = -1

    for idx, resp in enumerate(comment_responses):
        if resp["response_id"] == response_id:
            index_of_response_to_fetch = idx
            break

    if index_of_response_to_fetch == -1:
        return e.COMMENT_NOT_FOUND, "The requested response could not be found."
    else:
        return None, comment_responses[index_of_response_to_fetch]