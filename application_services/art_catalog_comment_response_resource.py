from application_services.base_application_resource import BaseApplicationResource
import database_services.dynamodb_service as d_service


class ArtCatalogCommentResponseResource(BaseApplicationResource):
    table_name = "comments-responses"
    order_record_table = "orders"
    order_contents_table = "order_items"

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def retrieve_all_comments_for_item(cls, item_id):
        """
        Retrieves all comments for an item given an item_id.
        """
        return None

    @classmethod
    def post_comment(cls, item_id, poster_id, comment_text, in_response_to_comment_id=None):
        """
        Posts a comment under an item (with a given ID).
        Takes in the poster's ID, the text of the comment, and the comment that this was in response to (if applicable)
        """
        return None

    @classmethod
    def edit_comment(cls, item_id, poster_id, comment_id, updated_comment_text):
        """
        Edits an already-posted comment.
        Takes in the item's ID, the existing comment's ID, the poster's ID (to verify they have permissions to edit),
        and the updated comment text.
        """
        return None

    @classmethod
    def delete_comment(cls, item_id, poster_id, comment_id):
        """
        Deletes an already-posted comment.
        Takes in the item's ID, the existing comment's ID, the poster's ID (to verify they have permissions to delete).
        """
        return None
