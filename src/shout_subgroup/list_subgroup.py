import logging

from sqlalchemy.orm import Session
from telegram import Update
from telegram.ext import ContextTypes

from shout_subgroup.database import session
from shout_subgroup.exceptions import NotGroupChatError
from shout_subgroup.repository import find_all_subgroups_in_group_chat
from shout_subgroup.utils import is_group_chat


async def list_subgroups(db: Session, telegram_group_chat_id: int) -> str:
    # Guard Clauses
    if not await is_group_chat(telegram_group_chat_id):
        msg = f"Can't list subgroups because telegram chat id {telegram_group_chat_id} is not a group chat."
        logging.info(msg)
        raise NotGroupChatError(msg)

    # Get all the subgroups for the group chat
    subgroups = await find_all_subgroups_in_group_chat(db, telegram_group_chat_id)

    # Transform into string
    subgroups_names = [sub.name for sub in subgroups]

    # "mock-subgroup-1, mock-subgroup-2, mock-subgroup-3"
    return ", ".join(subgroups_names)


async def list_subgroup_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the list subgroup command.
    This function should not handle business logic,
    or storing data. It will delegate that responsibility
    to other functions. Similar to controllers from the MVC pattern.
    :param update:
    :param context:
    :return:
    """

    try:
        subgroups = await list_subgroups(session, update.effective_chat.id)

        if not subgroups:
            await update.message.reply_text(f"There are no subgroups in this chat")
            return

        await update.message.reply_text(f"Here are the subgroups for this chat: {subgroups}")
        return

    except NotGroupChatError:
        await update.message.reply_text("Sorry, you can only list subgroups in group chats.")
        return
