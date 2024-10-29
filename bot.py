import os
import logging

import yaml
from dotenv import load_dotenv

from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from utils.question_loader import initialize_questionnaire


# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load config
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
    print(config)

# Initialize questions and answers database
initialize_questionnaire(config)


from handlers.start import start, select_topic
from handlers.interview import start_interview, handle_answer, request_hint, get_answer
from handlers.progress import check_progress
from handlers.resources import get_resources

# Conversation states
SELECTING_TOPIC, ASKING_QUESTION, PROVIDING_HINT, CHECKING_PROGRESS, FETCHING_RESOURCES = range(5)


def build_application():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("Telegram Bot Token not found.")
        return

    # Initialize the bot application
    application = ApplicationBuilder().token(token).build()

    # Conversation for topic selection and interview
    interview_convo = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_TOPIC: [CommandHandler('select_topic', select_topic)],
            ASKING_QUESTION: [
                CommandHandler('start_interview', start_interview),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer),  # Capture user answers
                CommandHandler('hint', request_hint),
                CommandHandler('answer', get_answer),
                CommandHandler('progress', check_progress),
                CommandHandler('resources', get_resources),
            ]
        },
        fallbacks=[]  # Add fallback handling if needed
    )

    application.add_handler(interview_convo)

    return application


def main():
    app = build_application()

    # If something goes wrong
    if app is None:
        return

    if app:
        app.run_polling()


if __name__ == '__main__':
    main()
