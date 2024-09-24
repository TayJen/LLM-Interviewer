import asyncio
import os
import json
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, \
    filters

# Load environment variables from.env file
load_dotenv()

# Enable logging to help debug
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# The logger we use for this bot
logger = logging.getLogger(__name__)

# Define states for conversation
ASKING_QUESTION, RECEIVING_ANSWER = range(2)


# Load questions from JSON file
def load_questions():
    with open('interview_questions.json', 'r') as file:
        return json.load(file)


questions = load_questions()


# Start Command - Triggered when user starts the bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Hello! I'm your LLM-Interview bot. \
        I will ask you machine learning interview questions. \
        Type /start_interview to begin."
    )


# Start Interview Command
async def start_interview(update: Update, context: CallbackContext):
    # Store current question index in user data
    context.user_data['current_question'] = 0

    # Ask the first question
    first_question = questions[context.user_data['current_question']]['question']
    await update.message.reply_text(f"Question 1: {first_question}")

    # Move to the next state (ASKING_QUESTION)
    return ASKING_QUESTION


# Handle User's Response to Questions
async def handle_answer(update: Update, context: CallbackContext):
    user_answer = update.message.text
    current_question = context.user_data['current_question']

    # Retrieve correct answer from questions file
    correct_answer = questions[current_question]['answer']

    # Simple comparison to check if answer is correct (can be expanded)
    if user_answer.lower() == correct_answer.lower():
        await update.message.reply_text("Correct! Moving to the next question...")
    else:
        await update.message.reply_text(f"Incorrect! The correct answer was: {correct_answer}")

    # Move to the next question
    context.user_data['current_question'] += 1

    if context.user_data['current_question'] < len(questions):
        next_question = questions[context.user_data['current_question']]['question']
        await update.message.reply_text(f"Question {context.user_data['current_question'] + 1}: {next_question}")
        return ASKING_QUESTION
    else:
        await update.message.reply_text("Interview complete! Thanks for answering the questions.")
        return ConversationHandler.END


# Handle Unknown Commands
async def unknown_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Sorry, I didn't understand that command.")


# Cancel Interview Command
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Interview canceled.")
    return ConversationHandler.END


# Main Function to Start the Bot
def build_application():
    # Initialize the bot with your token
    application = ApplicationBuilder().token(
        # TODO: fix and add the error message if no token is provided
        os.getenv("TELEGRAM_BOT_TOKEN", None)
    ).concurrent_updates(True).build()

    # Command handler for /start
    start_handler = CommandHandler('start', start)

    # Command handler for /start_interview
    interview_handler = ConversationHandler(
        entry_points=[CommandHandler('start_interview', start_interview)],
        states={
            ASKING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Fallback handler for unknown commands
    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)

    # Add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(interview_handler)
    application.add_handler(unknown_handler)

    return application


def main():
    app = build_application()
    app.run_polling()


if __name__ == '__main__':
    main()
