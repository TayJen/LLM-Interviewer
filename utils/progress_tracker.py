def update_progress(user_data: dict):
    user_data['correct'] = user_data.get('correct', 0) + 1


def get_progress(user_data: dict):
    return f"{user_data.get('correct', 0)} correct out of {user_data['current_question']} questions."
