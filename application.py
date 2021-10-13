from flask import Flask, Response, request
from flask_cors import CORS
from application_services.art_catalog_orders_resource import ArtCatalogOrdersResource
from http import HTTPStatus
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

application = app = Flask(__name__)
CORS(app)


def form_response_json(status, result):
    return json.dumps({
        "status": status,
        "result": result
    }, default=str)


@app.route("/")
def health_check():
    return "<u>Hello World</u>"


@app.route("/api/orders", methods=["GET", "POST"])
@app.route("/api/orders/", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        res = ArtCatalogOrdersResource.retrieve_all_orders()
        return Response(
            form_response_json("success", res),
            status=HTTPStatus.OK,
            content_type="application/json"
        )
    elif request.method == "POST":
        order_base_info = request.get_json()
        res = ArtCatalogOrdersResource.add_new_order(order_base_info)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp


@app.route("/api/orders/<int:order_id>", methods=["GET", "DELETE"])
@app.route("/api/orders/<int:order_id>/", methods=["GET", "DELETE"])
def selected_order(order_id): # TODO: DRY refactoring
    if request.method == "GET":
        res = ArtCatalogOrdersResource.retrieve_single_order(order_id=order_id)
        retval = res
    else: # request.method == "DELETE":
        res = ArtCatalogOrdersResource.remove_order_by_id(order_id)
        retval = {"order_id": order_id}

    if res is not None:
        return Response(
            form_response_json("success", retval),
            status=HTTPStatus.OK,
            content_type="application/json"
        )
    else:
        return Response(
            form_response_json("order not found", None),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json"
        )


@app.route("/api/orders/<int:order_id>/orderitems", methods=["GET"])
@app.route("/api/orders/<int:order_id>/orderitems/", methods=["GET"])
def all_items_for_order(order_id): # WORKS!
    res = ArtCatalogOrdersResource.retrieve_all_items_in_given_order(order_id=order_id)
    if res is None:
        return Response(
            form_response_json("order not found", None),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json"
        )
    else:
        return Response(
            form_response_json("success", res),
            status=HTTPStatus.OK,
            content_type="application/json"
        )


@app.route("/api/orders/<int:order_id>/orderitems/<int:item_id>", methods=["GET", "POST", "DELETE"])
@app.route("/api/orders/<int:order_id>/orderitems/<int:item_id>/", methods=["GET", "POST", "DELETE"])
def item_in_order(order_id, item_id):
    if request.method == "GET":
        res = ArtCatalogOrdersResource.retrieve_single_item_in_given_order(order_id, item_id)
        retval = res
    elif request.method == "POST": # both to create an entry and to update it
        order_info = request.get_json() # item info in body
        order_info["order_id"] = order_id
        order_info["item_id"] = item_id
        res = ArtCatalogOrdersResource.add_item_to_order(order_info)
        retval = res
    else: # request.method == "DELETE":
        res = ArtCatalogOrdersResource.remove_item_from_order(order_id, item_id)
        retval = {"order_id": order_id, "item_id": item_id}

    if res is None or res is False:
        return Response(
            form_response_json("order not found" if res is None else "item not in specified order", None),
            status=HTTPStatus.NOT_FOUND,
            content_type="application/json"
        )
    else:  # if valued
        return Response(
            form_response_json("success", res),
            status=HTTPStatus.OK,
            content_type="application/json"
        )


if __name__ == "__main__":
    application.run()
