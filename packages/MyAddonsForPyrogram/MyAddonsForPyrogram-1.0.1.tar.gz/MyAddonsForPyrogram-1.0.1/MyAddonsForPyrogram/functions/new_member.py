from MyAddonsForPyrogram.enums import IMAGES, TEXTS
from MyAddonsForPyrogram.database import NewMembersManager
from pyrogram import Client
from pyrogram.types import ChatMemberUpdated


def handle_member_update(
    client: Client,
    update: ChatMemberUpdated,
    channel_link: str,
    new_members_manager: NewMembersManager,  # Instance of NewMembersManager (configured with MONGO_DB_URL)
) -> None:
    """
    Args:
            client (Client): The Pyrogram client instance used for API calls.
            update (ChatMemberUpdated): An object containing information about the member update.
            channel_link (str): A string URL representing the channel link, used in the welcome message.
            new_members_manager: An instance of NewMembersManager, instantiated with MONGO_DB_URL,
                                 responsible for handling the removal of members.

        This function handles updates regarding a member's status in a chat.
        It checks if the update indicates that a new member has joined and, if so,
        sends them a thank-you photo along with a caption. Immediately after,
        it removes the member using the provided NewMembersManager instance.
    """

    # Check if the update has a new chat member and that there wasn't a previous member state.
    # This condition typically implies that the user has just joined the chat.
    if update.new_chat_member and not update.old_chat_member:
        try:
            new_members_manager.remove_member(update.from_user.id)
        except:
            pass
        client.send_photo(
            chat_id=update.from_user.id,  # Send the photo directly to the user via private chat.
            photo=IMAGES.THANKS_FOR_JOINING.value,  # Retrieve the thank-you image.
            caption=TEXTS.THANKS_FOR_JOINING.value(
                channel_link
            ),  # Create the caption text with the channel link.
        )
