import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Your bot's token
load_dotenv()
TOKEN = os.getenv('TELEGRAM_API_KEY')


async def create_subgroup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if context.args:
        subgroup_name = context.args[0]
        members = context.args[1]

        await update.message.reply_text(f'Subgroup Name: {subgroup_name}')
        await update.message.reply_text(f'Members: {members}')

        return

    await update.message.reply_text("You need to provide the group name and members")


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("group", create_subgroup))
    app.run_polling()


if __name__ == '__main__':
    main()
