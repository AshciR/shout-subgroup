import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Your bot's token
load_dotenv()
TOKEN = os.getenv('TELEGRAM_API_KEY')

# TODO: Determine how to persist the data in the long run
subgroups = {}  # {subgroup_name: user_id}


async def create_subgroup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        subgroup_name = context.args[0]

        # TODO: Add method that will parse members into a set
        # TODO: Map the member names to their user ids
        # TODO: Figure out how to add yourself to the group. Telegram doesn't allow you to @ yourself
        members = context.args[1]

        await update.message.reply_text(f'Subgroup Name: {subgroup_name}')
        await update.message.reply_text(f'Members: {members}')

        if subgroup_name not in subgroups:
            subgroups[subgroup_name] = {members}
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
