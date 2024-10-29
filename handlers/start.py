import logging

from telegram import Update
from telegram.ext import CallbackContext

from utils.question_loader import questionnaire_db


logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    topics = questionnaire_db.get_topics()
    topic_list = "\n".join([f"{i + 1}. {topic}" for i, topic in enumerate(topics)])
    await update.message.reply_text(
        f"Hello! I'm your LLM-Interview bot. Please select a topic by typing /select_topic <topic_number>:\n {topic_list}"
    )


async def select_topic(update: Update, context: CallbackContext):
    try:
        topic_num = int(context.args[0])
        context.user_data['topic_idx'] = topic_num
        logger.info(f"Selected topic number {topic_num}")
        await update.message.reply_text(f"Topic selected. Type /start_interview to begin.")
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a valid topic number.")
