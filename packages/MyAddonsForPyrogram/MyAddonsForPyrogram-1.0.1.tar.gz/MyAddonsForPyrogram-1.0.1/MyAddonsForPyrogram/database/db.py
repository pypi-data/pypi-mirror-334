from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from typing import Union


class UserManager:
    """
    A class to manage served users in a MongoDB collection.
    """

    def __init__(self, usersdb: Collection):
        """
        Initialize with a MongoDB collection instance.

        Parameters:
            usersdb (Collection): The MongoDB collection instance.
                                  (e.g., MongoClient()[database][collection])
        """
        self.usersdb = usersdb

    def is_served_user(self, user_id: int) -> bool:
        """
        Check if a user is already served (exists in the collection).

        Parameters:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user exists in the collection, False otherwise.
        """
        if self.usersdb:
            user = self.usersdb.find_one({"user_id": user_id})
            return bool(user)
        return False

    def get_served_users(self) -> list:
        """
        Retrieve all served users from the collection.

        Returns:
            list: A list of user documents with user_id greater than 0.
                  Returns an empty list if the collection is not valid.
        """
        if self.usersdb:
            # Using list() to return all found documents as a list
            return list(self.usersdb.find({"user_id": {"$gt": 0}}))
        return []

    def add_served_user(self, user_id: int) -> Union[InsertOneResult, bool, None]:
        """
        Add a new served user to the collection if not already present.

        Parameters:
            user_id (int): The ID of the user to add.

        Returns:
            InsertOneResult: The result of the insert_one operation if the user is added.
            bool: False if the collection is invalid.
            None: If the user is already served.
        """
        if self.usersdb:
            if self.is_served_user(user_id):
                return None
            return self.usersdb.insert_one({"user_id": user_id})
        return False
