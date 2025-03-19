from pyrogram.types import Message
import json, requests


def send_reaction(message: Message, emoji: str, BOT_TOKEN: str):
    """
    Send a reaction (emoji) to a Telegram message using the Telegram Bot API.

    Parameters:
        message (Message): A Pyrogram Message object representing the target message.
        emoji (str): The emoji to send as a reaction.
        BOT_TOKEN (str): The token of the Telegram bot.

    Returns:
        The result of the reaction operation, as provided by the Telegram API response.
    """
    # Define the reaction payload as a list with a dictionary containing the type and emoji.
    reaction = [{"type": "emoji", "emoji": emoji}]

    # Prepare the data payload with the required parameters for the Telegram API.
    data = {
        "chat_id": message.chat.id,  # ID of the chat where the message is located.
        "message_id": message.id,  # ID of the message to add the reaction.
        "reaction": json.dumps(
            reaction
        ),  # Serialize the reaction list to a JSON string.
        "is_big": False,  # Flag indicating if the reaction should be displayed as big.
    }

    # Construct the API URL using the provided bot token.
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMessageReaction"

    # Send a POST request to the Telegram API with the data payload and parse the response as JSON.
    response = requests.post(url, data=data).json()

    # Return the 'result' field from the API response, which contains the outcome of the operation.
    return response["result"]
