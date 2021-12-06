from flask import Flask, Response, request
from flask_cors import CORS
from middleware.security.security import Security
from http import HTTPStatus
import json
import logging

from database_services import dynamodb_service as db
from database_services import dynamodb_errors as e

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

application = app = Flask(__name__)
CORS(app)


def form_response_json(status, result):
    return json.dumps({"status": status, "result": result}, default=str)


@application.before_request
def verify_oauth_token():
    """
    Method to run before all requests; determines if a user has a valid
    Google OAuth2 token and uses the token to discover who the user making the request is.
    The google user and auth token loaded into special flask object called 'g'.
    While g is not appropriate for storing data across requests, it provides a global namespace
    for holding any data you want during a single request.
    """
    return Security.verify_token(request)


@app.route("/")
def health_check():
    return "Hello World"


@app.route("/api/comments/<string:item_id>", methods=["GET", "POST"], strict_slashes=False)
def get_post_item_comments(item_id):
    """
    Main query param: item_id
    GET -- gets all comments under a given item ID
        * Does not expect any other params.
    POST -- adds a new comment under a given item ID.
        * Expects a JSON body in the request, consisting of the following keys: user_id, comment_text
        * POST issues a 400 error if these keys are missing from the body.
    """
    if request.method == "GET":
        result = db.get_comments_by_item_id(item_id)
        return Response(
            form_response_json("done", result),
            status=HTTPStatus.OK,
            content_type="application/json",
        )
    elif request.method == "POST":
        request_base_info = request.get_json()
        user_id = request_base_info.get("user_id", None)
        comment_text = request_base_info.get("comment_text", None)

        if user_id is None or comment_text is None:
            return Response(
                form_response_json("bad request - user/comment", None),
                status=HTTPStatus.BAD_REQUEST,
                content_type="application/json",
            )

        result = db.post_comment(item_id, user_id, comment_text)
        return Response(
            form_response_json("success", None), # TODO: What to return here?
            status=HTTPStatus.OK,
            content_type="application/json",
        )


@app.route("/api/comments/<string:item_id>/<string:comment_id>", methods=["GET", "POST", "PUT", "DELETE"], strict_slashes=False)
def get_update_delete_single_comments(item_id, comment_id):
    """
    TODO: Should probably use item ID somehow.
    All methods require the item ID and the comment ID in the query params.
    GET -- gets a comment with a given comment ID.
        * 404 if the given comment ID does not exist.
    POST -- posts a response under the given comment ID.
        * Expects a JSON body in the request, consisting of the following keys: user_id, response_text
        * 400 if the necessary JSON body params are not provided.
        * 404 for other errors
    PUT -- updates a comment with the given comment ID.
        * Expects a JSON body in the request, consisting of the following keys: user_id, old_version_id, new_comment_text.
        * 400 if the necessary JSON body params are not provided.
        * 409 for a Write-Write conflict
        * 403/404 for other errors.
    DELETE -- deletes a comment with the given ID
        * Expects a JSON body in the request, consisting of the following keys: user_id
        * 400 if the necessary JSON body params are not provided.
        * 403/404 for other errors
    """
    if request.method == "GET":
        result = db.fetch_comment_by_id(comment_id)
        return Response(
            form_response_json("success" if result is not None else "not found", result),
            status=HTTPStatus.OK if result is not None else HTTPStatus.NOT_FOUND,
            content_type="application/json",
        )
    elif request.method == "POST":
        request_base_info = request.get_json()
        user_id = request_base_info.get("user_id", None)
        response_text = request_base_info.get("response_text", None)

        if user_id is None or response_text is None:
            return Response(
                form_response_json("bad request - user/comment", None),
                status=HTTPStatus.BAD_REQUEST,
                content_type="application/json",
            )

        result = db.add_response(comment_id, user_id, response_text)
        return Response(
            form_response_json("success", None),  # TODO: What to return here?
            status=HTTPStatus.OK,
            content_type="application/json",
        )

    elif request.method == "PUT":
        request_base_info = request.get_json()
        user_id = request_base_info.get("user_id", None)
        old_version_id = request_base_info.get("old_version_id", None)
        new_comment_text = request_base_info.get("new_comment_text", None)

        if user_id is None or old_version_id is None or new_comment_text is None:
            return Response(
                form_response_json("bad request - user/version/comment", None),
                status=HTTPStatus.BAD_REQUEST,
                content_type="application/json",
            )

        result = db.update_comment(comment_id, old_version_id, user_id, new_comment_text)
        if result[0] is not None:
            return Response(
                form_response_json(f"invalid request - {result[1]}", None),
                status=e.error_status_mappings[result[0]],
                content_type="application/json",
            )
        else:
            return Response(
                form_response_json("success", None), # TODO: What to return here?
                status=HTTPStatus.OK,
                content_type="application/json",
            )

    elif request.method == "DELETE":
        request_base_info = request.get_json()
        user_id = request_base_info.get("user_id", None)

        if user_id is None:
            return Response(
                form_response_json("bad request - user", None),
                status=HTTPStatus.BAD_REQUEST,
                content_type="application/json",
            )

        result = db.delete_comment(comment_id, user_id)
        if result[0] is not None:
            return Response(
                form_response_json(f"invalid request - {result[1]}", None),
                status=e.error_status_mappings[result[0]],
                content_type="application/json",
            )
        else:
            return Response(
                form_response_json("success", None), # TODO: What to return here?
                status=HTTPStatus.OK,
                content_type="application/json",
            )


@app.route("/api/comments/<string:item_id>/<string:comment_id>/<string:response_id>", methods=["GET", "PUT", "DELETE"],
           strict_slashes=False)
def update_delete_single_responses(item_id, comment_id, response_id):
    """
    All methods require the item ID, response ID, and comment_ID as query params.
    Both methods also require user_id as a JSON body param.
    All methods may return:
        * 400 if the request is bad
        * 403 if the user is invalid
        * 404 if the given comment/response cannot be found.
    GET -- Retrieve a single response.
    PUT -- Updates a response.
        * Requires additional JSON body params: new_response_text and old_version_id
    DELETE -- Deletes a response.
    """
    if request.method == "GET":
        result = db.fetch_single_response(comment_id, response_id)

        if result[0] is not None:
            return Response(
                form_response_json(f"invalid request - {result[1]}", None),
                status=e.error_status_mappings[result[0]],
                content_type="application/json",
            )
        else:
            return Response(
                form_response_json("success", result),
                status=HTTPStatus.OK,
                content_type="application/json",
            )
    elif request.method == "PUT":
        request_base_info = request.get_json()
        user_id = request_base_info.get("user_id", None)
        new_response_text = request_base_info.get("new_response_text", None)
        old_version_id = request_base_info.get("old_version_id", None)

        if user_id is None or new_response_text is None or old_version_id is None:
            return Response(
                form_response_json("bad request - user/response_text", None),
                status=HTTPStatus.BAD_REQUEST,
                content_type="application/json",
            )

        result = db.update_response(comment_id, response_id, new_response_text, user_id, old_version_id)

    else:  # elif request.method == "DELETE":
        request_base_info = request.get_json()
        user_id = request_base_info.get("user_id", None)

        if user_id is None:
            return Response(
                form_response_json("bad request - user", None),
                status=HTTPStatus.BAD_REQUEST,
                content_type="application/json",
            )

        result = db.delete_response(comment_id, response_id, user_id)

    if result[0] is not None:
        return Response(
            form_response_json(f"invalid request - {result[1]}", None),
            status=e.error_status_mappings[result[0]],
            content_type="application/json",
        )
    else:
        return Response(
            form_response_json("success", None),  # TODO: What to return here?
            status=HTTPStatus.OK,
            content_type="application/json",
        )


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
