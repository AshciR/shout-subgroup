import logging
import os
from dataclasses import dataclass, field

from dotenv import load_dotenv
from telegram import Update, User as TelegramUser
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Your bot's token
load_dotenv()
TOKEN = os.getenv('TELEGRAM_API_KEY')

# TODO: Determine how to persist the data in the long run
group_chats = {}
subgroups = {}
users = {}


@dataclass
class User:
    user_id: int
    username: str
    first_name: str
    last_name: str
    link: str
    subgroups: list[str] = field(default_factory=list)


async def add_user_to_collection(user: TelegramUser, users_collection: dict[int, User]) -> User:
    """
       Add a new user to the storage if not already present.

       Args:
           user (TelegramUser): The telegram user object.
           users_collection (dict): the database/dictionary with the users

       Returns:
           User: The added or existing user.
   """
    user_id = user.id
    if user_id not in users_collection:
        added_user = User(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            link=user.link
        )

        logging.info(f"Adding User with id {user_id}.")
        users_collection[user_id] = added_user

        return added_user
    else:
        logging.info(f"User with id {user_id} already exists.")
        return users_collection[user_id]


async def add_user_to_subgroup(
        user_id,
        subgroup_id,
        users_collection: dict[int, User],
        subgroup_collection: dict[int, dict]
) -> bool:
    if user_id not in users_collection:
        logging.info(f"User with id {user_id} does not exist.")
        return False

    if subgroup_id not in subgroup_collection:
        logging.info(f"Subgroup with id {subgroup_id} does not exist.")
        return False

    user = users_collection[user_id]
    if subgroup_id not in user.subgroups:
        user.subgroups.append(subgroup_id)
    else:
        logging.info(f"User with id {user_id} is already in subgroup {subgroup_id}.")
        return False

    if user_id not in subgroup_collection[subgroup_id]["user_ids"]:
        subgroup_collection[subgroup_id]["user_ids"].append(user_id)
    else:
        logging.info(f"User with id {user_id} is already in subgroup {subgroup_id}.")
        return False

    return True


async def create_subgroup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # # Temporary hack to save users
    # added_user = add_user_to_collection(
    #     update.effective_user,
    #     users
    # )
    #
    # # Extract arguments from the command
    # args = context.args
    # if len(args) < 2:
    #     await update.message.reply_text("Usage: /group <group_name> @alice @bob ... @zack")
    #     return
    #
    # subgroup_name = args[0]
    #
    # usernames = set(args[1:])   # We parse this into a set to prevent duplicate entries
    #
    # if subgroup_name not in subgroups:
    #     subgroups[subgroup_name] = {usernames}
    #     await update.message.reply_text(f'Storage: {subgroups}')
    # else:
    #     await update.message.reply_text(
    #         f'"{subgroup_name}" group already exists. Remove the group if you want to recreate it'
    #     )
    #
    # return


    if context.args:
        subgroup_name = context.args[0]

        # TODO: Map the member names to their user ids

        # TODO: Figure out how to add yourself to the group. Telegram doesn't allow you to @ yourself
        usernames = context.args[1]

        await update.message.reply_text(f'Subgroup Name: {subgroup_name}')
        await update.message.reply_text(f'Members: {usernames}')

        if subgroup_name not in subgroups:
            subgroups[subgroup_name] = {usernames}
            await update.message.reply_text(f'Storage: {subgroups}')
        else:
            await update.message.reply_text(
                f'"{subgroup_name}" group already exists. Remove the group if you want to recreate it'
            )

        return

    await update.message.reply_text("You need to provide the group name and members")


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("group", create_subgroup))
    app.run_polling()


if __name__ == '__main__':
    main()
