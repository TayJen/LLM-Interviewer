import logging
import os

from telegram import Update
from telegram.ext import CallbackContext

from utils.question_loader import questionnaire_db
from utils.rag_pipeline import evaluate_answer
from utils.stages import SELECTING_TOPIC, ASKING_QUESTION


async def start_interview(update: Update, context: CallbackContext):
    """Begin the interview with generated questions."""
    if 'generated_questions' not in context.user_data:
        await update.message.reply_text("Пожалуйста сначала выбери тему: \n/select_topic <topic_number>")
        return

    context.user_data['current_question_idx'] = 0
    await ask_next_question(update, context)


async def ask_next_question(update: Update, context: CallbackContext):
    """Ask the next question in the interview."""
    questions = context.user_data['generated_questions']
    idx = context.user_data['current_question_idx']

    if idx >= len(questions):
        topics = questionnaire_db.get_rag_topics()
        topic_list = "\n".join([f"{i + 1}. {topic}" for i, topic in enumerate(topics)])
        await update.message.reply_text(f"Ты повторил все вопросы по этой теме, здорово! Ты можешь набрать \n/select_topic <topic_number> чтобы выбрать новую тему.\n\nНапоминаю список тем:\n{topic_list}")
        return SELECTING_TOPIC

    context.user_data['current_question'] = questions[idx]['question']
    context.user_data['current_answer'] = questions[idx]['answer']

    await update.message.reply_text(f"Question #{idx + 1}: {questions[idx]['question']}")


async def handle_answer(update: Update, context: CallbackContext):
    """Evaluate user's answer and provide feedback."""
    logging.info("In handle_answer now...")

    user_answer = update.message.text
    question = context.user_data['current_question']
    correct_answer = context.user_data['current_answer']

    # Evaluate the answer using LLM
    evaluation = evaluate_answer(question, correct_answer, user_answer)

    # Parse the evaluation response
    grade = evaluation.get('grade', 0.0)
    tips = evaluation.get('tips', "No tips available.")

    logging.info(f"Question: {question}")
    logging.info(f"Answer: {correct_answer}")
    logging.info(f"User Answer: {user_answer}")
    logging.info(f"Evaluation: grade - {grade}, tips: {tips}")

    great_grade_threshold = float(os.getenv('rag_great_grade_threshold', 0.8))
    good_grade_threshold = float(os.getenv('rag_good_grade_threshold', 0.5))

    if grade >= great_grade_threshold:
        await update.message.reply_text(f"Отличный ответ!\n\n{tips}")
    elif grade >= good_grade_threshold:
        await update.message.reply_text(f"Хороший ответ, но есть неточности!\n\n{tips}")
    else:
        await update.message.reply_text(f"Ответ в целом неправильный\n\n{tips}")

    # Move to the next question
    context.user_data['current_question_idx'] += 1
    return await ask_next_question(update, context)
