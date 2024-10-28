def get_hint(question: str, topic_idx: int = 0, question_idx: int = 0) -> str:
    topic_hints = {
        (1, 1): "Hint for Topic 1, Question 1",
        (1, 2): "Hint for Topic 1, Question 2",
        (2, 1): "Hint for Topic 2, Question 1",
        (2, 2): "Hint for Topic 2, Question 2",
    }

    question_hints = topic_hints.get((topic_idx, question_idx), None)
    if question_hints is None and question == "":
        return f"No hint available for question #{question_idx+1} in topic #{topic_idx+1}."
    elif question_hints is None and question:
        return f"Hint for question: ```{question.split(' ')[-1]}```"

    return question_hints
