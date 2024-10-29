import json
import os
import logging

from tqdm import tqdm

logger = logging.getLogger(__name__)
questionnaire_db = None


class Questionnaire:
    def __init__(self, config: dict):
        self.questions_path = config.get('questions_data_path', None)
        self.topics_list: list[str] = []
        self.all_questions_and_answers_dict: dict[str, dict[str, str]] = {}
        self.all_questions_list: dict[str: list[str]] = {}

        self._setup_and_load()
        logging.info("Initialized Questionnaire")

    def _setup_and_load(self):
        if self.questions_path is None:
            raise ValueError('No questions data path specified in the configuration')
        self.topics_list = os.listdir(self.questions_path)

        for topic_name in tqdm(self.topics_list):
            topic_path = os.path.join(self.questions_path, topic_name)

            if not os.path.isdir(topic_path):
                continue

            topic_questions_files = os.listdir(topic_path)

            for question_file in topic_questions_files:
                if not question_file.endswith(".json"):
                    continue

                self.all_questions_and_answers_dict[topic_name] = {}
                self.all_questions_list[topic_name] = []
                subtopic_path = os.path.join(topic_path, question_file)

                with open(subtopic_path, "r") as f_question:
                    questions_answers_list = json.load(f_question)
                    self.all_questions_list[topic_name] = self.all_questions_list[topic_name] + questions_answers_list

                    self.all_questions_and_answers_dict[topic_name].update(
                        {
                            question_dict['question']: question_dict['answer']
                            for question_dict in questions_answers_list
                        }
                    )

        logger.info(
            f"Loaded {len(self.all_questions_and_answers_dict)} topics with {sum(len(q) for q in self.all_questions_list.values())} questions"
        )

    def get_topics(self) -> list:
        return self.topics_list

    def get_topic_by_idx(self, topic_idx: int) -> str:
        if topic_idx >= len(self.topics_list):
            logger.info(f"{topic_idx} is not in the list of topics")
            return ""

        topic_name = self.topics_list[topic_idx]
        logger.info(f"Got topic {topic_name} with idx {topic_idx}")
        return topic_name

    def get_questions_by_topic(self, topic_name: str) -> dict:
        logger.info(f"Getting questions for {topic_name}")
        return self.all_questions_and_answers_dict.get(topic_name, {})

    def get_question_by_idx(self, topic_idx: int, question_idx: int) -> str:
        topic_name = self.get_topic_by_idx(topic_idx)
        question_name = self.all_questions_list[topic_name][question_idx]["question"]
        logger.info(f"Got question {question_name} with idx {question_idx} in {topic_name}")
        return question_name

    def get_question_answer(self, topic_idx: int, question_idx: int) -> str:
        topic_name = self.get_topic_by_idx(topic_idx)
        answer = self.all_questions_list[topic_name][question_idx]["answer"]
        logger.info(f"Got answer for {question_idx} in {topic_name}: {answer}")
        return answer


def initialize_questionnaire(config: dict):
    global questionnaire_db
    if questionnaire_db is None:
        questionnaire_db = Questionnaire(config)
