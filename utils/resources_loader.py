def get_resources_for_question(topic_idx: int = 0, question_idx: int = 0) -> str:
    resources = {
        (1, 1): "Resource link for topic 1, question 1",
        (1, 2): "Resource link for topic 1, question 2",
        (2, 1): "Resource link for topic 2, question 1",
        (2, 2): "Resource link for topic 2, question 2"
    }

    answer = resources.get(
        (topic_idx, question_idx),
        f"No resources available for question #{question_idx} in topic #{topic_idx}"
    )

    return answer
