from telegram import Update
from telegram.ext import CallbackContext

from utils.resources_loader import get_resources_for_question


async def get_resources(update: Update, context: CallbackContext):
    resources = get_resources_for_question(context.user_data['topic'], context.user_data['current_question'])
    await update.message.reply_text(f"Here are some resources:\n{resources}")
