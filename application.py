from flask import Flask, Response, request
from flask_cors import CORS
from application_services.art_catalog_resource import ArtCatalogResource
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


@app.route("/api/orders", methods=["GET", "POST"]) # WORKS!
def orders():
    if request.method == "GET":
        res = ArtCatalogResource.retrieve_all_orders()
        return Response(
            form_response_json("success", res),
            status=HTTPStatus.OK,
            content_type="application/json"
        )
    elif request.method == "POST":
        order_base_info = request.get_json()
        res = ArtCatalogResource.add_new_order(order_base_info)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp


@app.route("/api/orders/<int:order_id>", methods=["GET", "DELETE"])
def selected_order(order_id): # TODO: DRY refactoring
    res = ArtCatalogResource.retrieve_single_order(order_id=order_id)
    if request.method == "GET":
        if res is not None:
            return Response(
                form_response_json("success", res),
                status=HTTPStatus.OK,
                content_type="application/json"
            )
        else:
            return Response(
                form_response_json("order not found", None),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json"
            )
    elif request.method == "DELETE":
        res = ArtCatalogResource.remove_order_by_id(order_id)
        if res is not None:
            return Response(
                form_response_json("success", {"order_id": order_id}),
                status=HTTPStatus.OK,
                content_type="application/json"
            )
        else:
            return Response(
                form_response_json("order not found", None),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json"
            )
    else: # TODO: Needed?
        return Response(
            form_response_json("unsupported method", None),
            status=HTTPStatus.METHOD_NOT_ALLOWED,
            content_type="application/json"
        )


@app.route("/api/orders/<int:order_id>/orderitems", methods=["GET"])
def all_items_for_order(order_id): # WORKS!
    res = ArtCatalogResource.retrieve_all_items_in_given_order(order_id=order_id)
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
def item_in_order(order_id, item_id): # TODO: DRY refactoring.
    if request.method == "GET":
        res = ArtCatalogResource.retrieve_single_item_in_given_order(order_id, item_id)
        if res is None or res is False:
            return Response(
                form_response_json("order not found" if res is None else "item not in specified order", None),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json"
            )
        else: # if valued
            return Response(
                form_response_json("success", res),
                status=HTTPStatus.OK,
                content_type="application/json"
            )
    elif request.method == "POST": # both to create an entry and to update it
        order_info = request.get_json() # item info in body
        order_info["order_id"] = order_id
        order_info["item_id"] = item_id
        res = ArtCatalogResource.add_item_to_order(order_info)
        if res is None:
            return Response(
                form_response_json("order not found", None),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json"
            )
        else:  # if valued
            return Response(
                form_response_json("success", res),
                status=HTTPStatus.OK,
                content_type="application/json"
            )
    elif request.method == "DELETE":
        res = ArtCatalogResource.remove_item_from_order(order_id, item_id)
        if res is None or res is False:
            return Response(
                form_response_json("order not found" if res is None else "item not in specified order", None),
                status=HTTPStatus.NOT_FOUND,
                content_type="application/json"
            )
        else:  # if valued
            return Response(
                form_response_json("success", {"order_id": order_id, "item_id": item_id}),
                status=HTTPStatus.OK,
                content_type="application/json"
            )


## OLD ROUTES (for reference, remove later)

@app.route("/api/catalog", methods=["GET"])
def get_full_catalog():
    res = ArtCatalogResource.retrieve_all_records()
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp


@app.route("/api/catalog/<int:item_id>", methods=["GET"])
def get_catalog_item(item_id):
    res = ArtCatalogResource.retrieve_single_record(item_id)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp


@app.route("/api/catalog", methods=["POST"])
def add_new_catalog_item():
    res = ArtCatalogResource.add_new_product(request.get_json())
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp


@app.route("/api/catalog/<int:item_id>", methods=["POST"])
def update_catalog_item(item_id):
    fields_to_update = request.get_json()
    res = ArtCatalogResource.update_item_by_id(item_id, fields_to_update)

    if res == 1:
        fields_to_update.update({"item_id": item_id, "status": "updated"})
        rsp = Response(
            json.dumps(fields_to_update), status=200, content_type="application/json"
        )
    else:
        rsp = Response(
            json.dumps({"item_id": item_id, "status": "error"}),
            status=500,
            content_type="application/json",
        )
    return rsp


@app.route("/api/catalog/<int:item_id>", methods=["DELETE"])
def delete_catalog_item(item_id):
    res = ArtCatalogResource.delete_item_by_id(item_id)

    if res == 1:
        rsp = Response(
            json.dumps({"item_id": item_id, "status": "deleted"}),
            status=200,
            content_type="application/json",
        )
    else:
        rsp = Response(
            json.dumps({"item_id": item_id, "status": "error"}),
            status=500,
            content_type="application/json",
        )
    return rsp


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
