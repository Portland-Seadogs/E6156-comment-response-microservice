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


def fetch_all_records(table_name, offset, limit):
    return None


def fetch_all_records_by_key(table_name, offset, limit, key):
    return None


def update_record(table_name, key, update_expression, attribute_names, attribute_values, return_values):
    return None


def create_record(table_name, item):
    return None


def delete_record(table_name, key, condition_expression, attribute_names, attribute_values):
    return None
