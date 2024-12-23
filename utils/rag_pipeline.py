import logging
import os
import re

from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Initialize
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=os.getenv("OPENAI_API_KEY"),
    chunk_size=1,
    dimensions=1024,
    show_progress_bar=False
)

vector_store_yandex = Chroma(
    collection_name="ml_yandex_handbook",
    embedding_function=embeddings,
    persist_directory="notebooks/chroma_yandex_db"
)

logging.info(
    f"Initialized Chroma vector_store_yandex, total num of documents: {len(vector_store_yandex.get()['documents'])}"
)

# Prompt
prompt = ChatPromptTemplate.from_template(
    """Generate the questions for the interviewee based on the selected topic of the interview:
{input}
And provided context (it's text of the book):

<context>
{context}
</context>

Генерировать надо на русском. Нужно сгенерировать как вопрос, так и ответ на этот вопрос, используя лишь приведенную информацию. В формате

Q: ...
A: ...

Всего нужно сгенерировать 10 вопросов.
"""
)

retriever_yandex = vector_store_yandex.as_retriever()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create a retrieval chain to answer questions
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever_yandex, document_chain)

# Create answer LLM
answer_llm = ChatOpenAI(model="gpt-4o-mini")


def generate_rag_questions(topic_name: str) -> list[dict]:
    """Generate questions using RAG pipeline."""
    logging.info("Generating questions...")

    response = retrieval_chain.invoke({"input": topic_name})
    generated_questions = response["answer"]

    # Parse questions and answers
    questions = re.findall(r'Q: (.*?)\n', generated_questions, re.DOTALL)
    answers = re.findall(r'A: (.*?)(?:\nQ:|\n?$)', generated_questions, re.DOTALL)

    logging.info(f"{generated_questions}")
    logging.info(f"Generated: {len(questions)} questions and {len(answers)} answers for topic {topic_name}")

    return [{"question": q, "answer": a} for q, a in zip(questions, answers)]


def evaluate_answer(input_question: str, input_answer: str, user_answer: str) -> dict:
    """Evaluate user answers using the evaluation chain."""
    prompt_answer_eval = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Ты помогающий интервьюеру ассистент, который оценивает ответ собеседующего от 0 до 1 (вещественным числом) " + \
                "Дан следующий вопрос: {input_question} и вот его истинный ответ: {input_answer}. " + \
                "Если что можешь использовать свой предобученный контекст чтобы узнать дополнительные детали для ответа на вопрос." + \
                "Помимо этого нужно помочь собеседуемому понять, почему его оценка справедлива и какие детали еще необходимо упомянуть для полноценного ответа" + \
                "Необходимо дать ответ в формате: \n\n Grade: ... \n Tips: ...",
            ),
            ("human", "Вот ответ собеседуемого: {input}"),
        ]
    )

    chain = prompt_answer_eval | answer_llm
    ai_response = chain.invoke(
        {"input_question": input_question, "input_answer": input_answer, "input": user_answer}
    )

    # Parse response for grade and tips
    grade_match = re.search(r'Grade:\s([\d.]+)', ai_response.content)
    tips_match = re.search(r'Tips:\s(.+)', ai_response.content, re.DOTALL)

    # Extracting and converting the grade
    grade = float(grade_match.group(1)) if grade_match else 0.0

    # Extracting the tips
    tips = tips_match.group(1).strip() if tips_match else "Нет деталей. Что-то сломалось."

    return {"grade": grade, "tips": tips}
