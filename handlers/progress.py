from telegram import Update
from telegram.ext import CallbackContext

from utils.progress_tracker import get_progress


async def check_progress(update: Update, context: CallbackContext):
    progress = get_progress(context.user_data)
    await update.message.reply_text(f"Progress: {progress}")
