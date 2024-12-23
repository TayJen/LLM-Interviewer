import os
import logging
import yaml
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from utils.question_loader import initialize_questionnaire
from utils.stages import SELECTING_TOPIC, ASKING_QUESTION

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load config
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
    logger.info("Config loaded successfully.")
    for key, value in config.items():
        os.environ[key] = str(value)

# Initialize questions and answers database
initialize_questionnaire(config)

from handlers.start import start, select_topic
from handlers.interview import start_interview, handle_answer


def build_application():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("Telegram Bot Token not found.")
        return

    application = ApplicationBuilder().token(token).build()

    # Conversation for topic selection and interview
    interview_convo = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_TOPIC: [
                CommandHandler('select_topic', select_topic)
            ],
            ASKING_QUESTION: [
                CommandHandler('start_interview', start_interview),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer),
            ]
        },
        fallbacks=[]
    )

    application.add_handler(interview_convo)
    return application


def main():
    app = build_application()
    if app is None:
        return
    app.run_polling()


if __name__ == '__main__':
    main()
