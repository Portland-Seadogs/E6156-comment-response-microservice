from flask import Flask, Response, request
from flask_cors import CORS
from middleware.security.security import Security
from application_services.art_catalog_comment_response_resource import ArtCatalogOrdersResource
from http import HTTPStatus
import json
import logging

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


@app.route("/api/comments/<int:item_id>", methods=["GET", "POST"], strict_slashes=False)
def get_post_comments(item_id):
    return None


@app.route("/api/comments/<int:item_id>/<int:comment_id>", methods=["PUT", "DELETE"], strict_slashes=False)
def update_delete_comments(item_id, comment_id):
    return None


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
