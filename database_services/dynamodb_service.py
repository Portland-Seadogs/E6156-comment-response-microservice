import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DynamoDBServiceException(Exception):
    def __init__(self, msg):
        self.msg = msg


def _get_db_connection():
    return None


def fetch_all_comments(table_name, offset, limit):
    """
    Retrieves all comments for all items
    """
    return None


def fetch_all_comments_by_template(table_name, offset, limit, template):
    """
    retrieves all comments that match template
    template: dict.  eg. {item_id: 1}
    """
    return None


def fetch_comment_by_id(comment_id):
    """
    retrieves the comment with comment_id=comment_id
    """
    return None


def add_response(table_name, comment_id, responder_id, response_text):
    """
    Posts a response under a comment id
    comment_id: the comment_id the response will be under
    responder_id: the user posting the response
    response_text: the response_text field in the response object
    (See add_response in ferguson code)
    """
    return None


def post_comment(commenter_id, comment_text):
    """
    Posts a new comment
    commenter_id: the user posting the comment
    commenter_text: the comment_text field in the comment object
    (See add_comment in ferguson code)
    """
    return None


def update_comment(comment_id, commenter_id, new_comment_text):
    """
    updates a comment with id=comment_id
    comment_id: the id of the comment to update
    commenter_id: the id of the commenter updating the comment
    new_comment_text: the new text of the comment

    this function needs to:
    1. fetch the old comment and verify that commenter_id= commenter_id
    2. update conditionally based on the version number of the old comment.
    (see write_comment_if_not_changed in ferguson code)
    """
    return None


def update_response(comment_id, response_id, new_response_text, responder_id):
    """
    same as update comment but for response
    """
    return None


def delete_comment(comment_id, commenter_id):
    """
    deletes a comment with comment_id=comment_id
    deleting a comment deletes all the responses to the comment
    needs to verify that the user deleting the comment is same as user who created the comment
    """


def delete_response(comment_id, response_id, responder_id):
    """
    deletes a response with response_id = responder_id
    needs to verify that the user deleting the response is the same as the user who created the response
    """
    return None
