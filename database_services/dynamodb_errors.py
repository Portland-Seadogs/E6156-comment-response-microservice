from enum import Enum
from http import HTTPStatus


class DynmamoDBErrors(Enum):
    WRONG_USER = 1
    COMMENT_NOT_FOUND = 2


error_status_mappings = {
    DynmamoDBErrors.WRONG_USER: HTTPStatus.FORBIDDEN,
    DynmamoDBErrors.COMMENT_NOT_FOUND: HTTPStatus.NOT_FOUND
}
