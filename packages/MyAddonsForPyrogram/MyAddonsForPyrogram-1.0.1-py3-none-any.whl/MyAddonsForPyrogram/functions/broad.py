from pyrogram.types import Message


def broadcast(user_list: list, message: Message, msg: str) -> tuple[int, int]:
    """
    Broadcasts a message to a list of users.

    Parameters:
        user_list (list): A list of dictionaries, each containing a "user_id" key.
        message (Message): The Pyrogram message object to be broadcasted.
        msg (str): A string that may contain the '--f' flag to determine the broadcast method.
                   If '--f' is found, the message is forwarded; otherwise, it is copied.

    Returns:
        tuple: A tuple containing:
            - no_sent (int): The number of messages sent successfully.
            - no_failed (int): The number of messages that failed to send.
    """
    no_sent = 0  # Counter for messages sent successfully.
    no_failed = 0  # Counter for messages that failed to send.

    # Loop through each user in the user list.
    for i in user_list:
        try:
            # Attempt to extract the user_id from the user dictionary.
            y = i["user_id"]
            # Check if the '--f' flag is present in the msg string.
            if "--f" in msg:
                try:
                    # Try to forward the message to the user with user_id 'y'.
                    message.forward(y)
                    no_sent += (
                        1  # Increment success counter if forwarding is successful.
                    )
                except Exception:
                    # If an exception occurs while forwarding, count it as a failure.
                    no_failed += 1
                    continue  # Skip to the next user.
            else:
                try:
                    # If '--f' flag is not present, try to copy the message to the user.
                    message.copy(y)
                    no_sent += 1  # Increment success counter if copying is successful.
                except Exception:
                    # If an exception occurs while copying, count it as a failure.
                    no_failed += 1
                    continue  # Skip to the next user.
        except Exception:
            # If there's an error (e.g., missing "user_id" in the dictionary), count it as a failure.
            no_failed += 1
            continue  # Continue with the next user in the list.

    # Return the counts of successful and failed message deliveries.
    return no_sent, no_failed
