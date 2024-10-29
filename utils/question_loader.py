import json


def load_questions() -> dict:
    with open('interview_questions.json', 'r') as file:
        return json.load(file)


def load_topics() -> list[str]:
    questions = load_questions()
    return [topic['name'] for topic in questions]


def load_question(topic_idx: int, question_idx: int, answer: bool = False) -> str:
    questions = load_questions()
    topic = questions[topic_idx]
    question_data = topic['questions'][question_idx]
    return question_data['answer'] if answer else question_data['question']
