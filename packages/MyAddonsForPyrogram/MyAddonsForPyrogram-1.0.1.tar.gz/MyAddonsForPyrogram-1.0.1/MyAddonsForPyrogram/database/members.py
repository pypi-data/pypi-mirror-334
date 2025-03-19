from pymongo.collection import Collection
from pymongo.results import UpdateResult
from typing import Union


class NewMembersManager:
    """
    A class to manage new member IDs in the 'user_list' document of a MongoDB collection.
    """

    def __init__(self, collection: Collection):
        """
        Initialize with a MongoDB collection instance.

        Parameters:
            collection (Collection): The MongoDB collection instance.
        """
        self.collection = collection

    def add_member(self, user_id: int) -> Union[UpdateResult, bool]:
        """
        Add a user ID to the 'user_ids' array within the document identified by '_id': 'user_list'.
        If the document does not exist, it will be created (upsert=True). The $addToSet operator ensures that
        the user_id is added only if it is not already present in the array, preventing duplicates.

        Parameters:
            user_id (int): The user ID to add.

        Returns:
            UpdateResult: The result of the update operation if the collection is valid.
            bool: False if the collection is invalid.
        """
        if self.collection:
            return self.collection.update_one(
                {"_id": "user_list"}, {"$addToSet": {"user_ids": user_id}}, upsert=True
            )
        return False

    def remove_member(self, user_id: int) -> Union[UpdateResult, bool]:
        """
        Remove a user ID from the 'user_ids' array within the document identified by '_id': 'user_list'.
        The $pull operator removes all instances of the specified value from the array.

        Parameters:
            user_id (int): The user ID to remove.

        Returns:
            UpdateResult: The result of the update operation if the collection is valid.
            bool: False if the collection is invalid.
        """
        if self.collection:
            return self.collection.update_one(
                {"_id": "user_list"}, {"$pull": {"user_ids": user_id}}
            )
        return False

    def get_all_members(self) -> list:
        """
        Retrieve all user IDs from the 'user_ids' array within the document identified by '_id': 'user_list'.

        Returns:
            list: A list of user IDs if the document exists and contains the 'user_ids' field.
                  An empty list if the document does not exist, the 'user_ids' field is absent,
                  or if the collection is invalid.
        """
        if self.collection:
            doc = self.collection.find_one({"_id": "user_list"})
            if doc:
                return doc.get("user_ids", [])
        return []
