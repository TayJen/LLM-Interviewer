from telegram import Update
from telegram.ext import CallbackContext

from utils.question_loader import load_question
from utils.hints import get_hint
from utils.progress_tracker import update_progress


async def start_interview(update: Update, context: CallbackContext):
    # In-memory for hints and resources
    context.user_data['current_question_idx'] = 1
    await ask_next_question(update, context)


async def ask_next_question(update: Update, context: CallbackContext):
    question = load_question(context.user_data['topic_idx'], context.user_data['current_question_idx'])
    # In-memory for hints and resources
    context.user_data['current_question'] = question
    await update.message.reply_text(f"Question {context.user_data['current_question_idx']}: {question}")


async def handle_answer(update: Update, context: CallbackContext):
    user_answer = update.message.text
    question_id = context.user_data['current_question_idx']
    correct_answer = load_question(context.user_data['topic'], question_id, answer=True)

    if user_answer.lower() == correct_answer.lower():
        await update.message.reply_text("Correct! Moving to the next question...")
        context.user_data['current_question_idx'] += 1
        update_progress(context.user_data)  # Track progress
        await ask_next_question(update, context)
    else:
        await update.message.reply_text("Incorrect! Type /hint or /answer for help.")


async def request_hint(update: Update, context: CallbackContext):
    hint = get_hint(context.user_data['topic_idx'], context.user_data['current_question_idx'])
    await update.message.reply_text(f"Hint: {hint}")


async def get_answer(update: Update, context: CallbackContext):
    correct_answer = load_question(
        context.user_data['topic_idx'], context.user_data['current_question_idx'],
        answer=True
    )
    await update.message.reply_text(f"The correct answer is: {correct_answer}")
    context.user_data['current_question_idx'] += 1
    await ask_next_question(update, context)
