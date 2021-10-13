from application_services.base_application_resource import BaseApplicationResource
import database_services.rdb_service as d_service


class ArtCatalogOrdersResource(BaseApplicationResource):
    db_schema = "art_catalog"
    order_record_table = "orders"
    order_contents_table = "order_items"

    def __init__(self):
        super().__init__()

    @classmethod
    def _order_exists(cls, order_id):
        # check if order exists
        found_orders = d_service.find_by_template(
            cls.db_schema, cls.order_record_table, {"order_id": order_id}
        )

        # if order does not exist, return None
        return len(found_orders) > 0

    ## ORDERS #

    @classmethod # DONE, WORKS!
    def retrieve_all_orders(cls):
        found_orders = d_service.fetch_all_records(cls.db_schema, cls.order_record_table)
        for order in found_orders:
            order["links"] = cls.retrieve_all_items_in_given_order(order["order_id"], href=True)
        return found_orders

    @classmethod # DONE, WORKS!
    def retrieve_single_order(cls, order_id):
        found_orders = d_service.find_by_template(
            cls.db_schema, cls.order_record_table, {"order_id": order_id}
        )
        if len(found_orders) > 0:
            found_order = found_orders[0]
            found_order["links"] = cls.retrieve_all_items_in_given_order(found_order["order_id"], href=True)
            return found_order
        else:
            return None

    @classmethod # DONE, WORKS!
    def add_new_order(cls, order_information): ## TODO: Create order info beforehand.
        new_record_id = d_service.create_new_record(
            cls.db_schema, cls.order_record_table, **order_information
        )
        return {"order_id": new_record_id}

    @classmethod # DONE
    def remove_order_by_id(cls, order_id):
        order_exists = cls._order_exists(order_id)

        # if order does not exist, return None
        if not order_exists:
            return None

        all_items_in_order = cls.retrieve_all_items_in_given_order(order_id, href=False)

        # delete all items in order before deleting order itself
        for i in all_items_in_order:
            cls.remove_item_from_order(i["order_id"], i["item_id"])

        return d_service.delete_record_by_multikey(
            cls.db_schema, cls.order_record_table, order_id=order_id
        )

    # TODO: Need to update order record itself in any way? (probably not)

    ## ORDER CONTENTS ##

    @classmethod # DONE
    def add_item_to_order(cls, item_order_information):
        # TODO: Check data validity?

        removal_result = cls.remove_item_from_order(
            item_order_information["order_id"],
            item_order_information["item_id"]
        )

        # order does not exist
        if removal_result is None:
            return None

        # create new order_item entry, using provided data.
        new_record_id = d_service.create_new_record(
            cls.db_schema, cls.order_contents_table, **item_order_information
        )

        return {
            "order_id": item_order_information["order_id"],
            "item_id": item_order_information["item_id"],
            "record_id": new_record_id
        }

    @classmethod # DONE, WORKS!
    def retrieve_all_items_in_given_order(cls, order_id, href=False):
        if href:
            all_items_in_order = d_service.find_by_template(
                cls.db_schema, cls.order_contents_table, {"order_id": order_id}
            )

            retval = []
            for i in all_items_in_order:
                retval.append({
                    "href": f'/orders/{order_id}/orderitems/{i["item_id"]}',
                    "rel": "order_item"
                })
            return retval
        else:
            order_exists = cls._order_exists(order_id)

            # if order does not exist, return None
            if not order_exists:
                return None

            # else return the items in this order. could be an empty array if the order does not yet have any entries
            return d_service.find_by_template(
                cls.db_schema, cls.order_contents_table, {"order_id": order_id}
            )


    @classmethod  # DONE, WORKS!
    def retrieve_single_item_in_given_order(cls, order_id, item_id):
        order_exists = cls._order_exists(order_id)

        # if order does not exist, return None
        if not order_exists:
            return None

        # get item with ID in order with ID
        item_in_order = d_service.find_by_template(
            cls.db_schema, cls.order_contents_table, {"order_id": order_id, "item_id": item_id}
        )

        if item_in_order is None or len(item_in_order) == 0:
            return False
        else:
            return item_in_order[0]


    @classmethod # DONE
    def remove_item_from_order(cls, order_id, item_id):
        order_exists = cls._order_exists(order_id)

        # if order does not exist, return None
        if not order_exists:
            return None

        # check if item already exists in order
        given_item = cls.retrieve_single_item_in_given_order(
            order_id, item_id
        )

        # if an item entry exists, delete it
        if given_item is not None and given_item is not False:
            d_service.delete_record_by_multikey(
                cls.db_schema, cls.order_contents_table, order_id=order_id, item_id=item_id
            )
            return True
        else:
            return False
