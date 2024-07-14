from gptprocessor import GPTProcessor
from text import Text
from quiz import Quiz
from question import Question
import json
import random


#"You are QuizMasterGPT, you will be provided with a short text, your task is to create a quiz question concerning the text in the language of the text. Return the created question only."

question_only_postfix = " Return the created question only."
json_postfix = " Return the question and answer in json format {'question':...,'answer':...}."
multiple_choice =' Provide multiple choices and answer in the json format {"question":...,"answer":..., "choices":...}'

class QuizMaker(GPTProcessor):
    system_quiz_making_prompt = "You are QuizMasterGPT, you will be provided with a short text, your task is to create a hard quiz question concerning the text in the language of the text." + multiple_choice
    def __init__(self):
        super().__init__()
        self._quiz = None
        self._topic = None
        self._topic_snippets = None

    def get_quiz(self):
        return self._quiz
    
    def set_quiz(self, quiz):
        self._quiz = quiz
    
    def get_topic(self):
        return self._topic
    
    def set_topic(self, topic):
        if type(topic) == Text:
            self.set_topic_snippets(topic.split_into_snippets())
        else:    
            self._topic = topic
    
    def set_topic_snippets(self, topic_snippets):
        self._topic_snippets = topic_snippets

    def get_topic_snippets(self):
        return self._topic_snippets
    
    def create_question(self, topic=None):
        question = Question()
        if topic:
            self.set_topic(topic)
        question_wording = self.get_question_wording()
        if True:
            question_json = json.loads(question_wording)
            question_wording = question_json["question"]
            answer = question_json["answer"]
            choices = question_json["choices"]
            random.shuffle(choices)
            question.set_answer(answer)
            question.set_choices(choices)
        question.set_question_wording(question_wording)
        return question
    
    def create_questions(self):
        self.get_topic()
        return [self.create_question()]
    
    def create_snippet_questions(self):
        topic_snippets = self.get_topic_snippets()
        questions = [self.create_question(topic=str(topic)) for topic in topic_snippets]
        return questions 

    def get_question_wording(self):
        topic = self.get_topic()
        question_wording = ""
        if topic:
            self.set_prompt(topic)
            model = self.get_model()
            messages = self.create_messages(self.system_quiz_making_prompt)
            question_wording = self.get_response(model, messages)  
        return question_wording 
    
    def create_quiz(self, quiz_type="text"):
        quiz = Quiz()
        questions = self.create_questions() if quiz_type == "text" else self.create_snippet_questions()
        quiz.set_questions(questions)
        return quiz

    
    
        

