import logging

from telegram import Update
from telegram.ext import CallbackContext

from utils.question_loader import questionnaire_db
from utils.rag_pipeline import generate_rag_questions
from utils.stages import SELECTING_TOPIC, ASKING_QUESTION

logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    logger.info("In start now")
    topics = questionnaire_db.get_rag_topics()
    topic_list = "\n".join([f"{i + 1}. {topic}" for i, topic in enumerate(topics)])
    await update.message.reply_text(
        f"Привет! Я твой LLM-Interview бот. Пожалуйста выбери тему собеседования, набрав \n/select_topic <topic_number>:\n{topic_list}"
    )
    return SELECTING_TOPIC


async def select_topic(update: Update, context: CallbackContext):
    logger.info("In select_topic now")
    try:
        topic_num = int(context.args[0]) - 1
        context.user_data['topic_idx'] = topic_num
        logger.info(f"Selected topic number {topic_num}")

        topic_name = questionnaire_db.get_rag_topic_by_idx(topic_num)
        await update.message.reply_text(f"Хорошо, ты выбрал {topic_name}. Пожалуйста подожди, загружаю вопросы...")

        rag_questions = generate_rag_questions(topic_name)
        context.user_data['generated_questions'] = rag_questions
        context.user_data['current_question_idx'] = 0

        await update.message.reply_text(f"Тема выбрана. Набери /start_interview чтобы начать.")
        return ASKING_QUESTION

    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйста выбери корректный номер темы.")
        return SELECTING_TOPIC
