from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError


def check_mongo(MONGO_URL: str) -> bool:
    """
    Check connectivity to a MongoDB instance.

    This function attempts to connect to a MongoDB server using the provided URL.
    It sends a "ping" command to the admin database to verify that the server is responsive.

    Parameters:
        MONGO_URL (str): The connection string (URI) for the MongoDB server.

    Returns:
        bool: True if the MongoDB server is reachable and responds to the ping,
              False if there is a connection failure or configuration error.
    """
    try:
        # Create a MongoClient instance with a server selection timeout of 5000ms.
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)

        # Send a ping command to the admin database to verify connection.
        client.admin.command("ping")

        # If the ping is successful, return True.
        return True
    except (ConnectionFailure, ConfigurationError) as e:
        # If a connection failure or configuration error occurs, return False.
        return False
