import json

class Quiz:
    def __init__(self):
        self._questions = []
        
    def add_question(self, question):
        self._questions.append(question)
    
    def add_questions(self, questions):
        self._questions.extend(questions)
    
    def set_questions(self, questions):
        self._questions = questions
    
    def get_questions(self):
        return self._questions

    def pop_question(self):
        self._questions.pop()
    
    def clear_questions(self):
        self._questions = []
    
    def parse_questions(self):
        questions = self.get_questions()
        serializable_questions = [question.to_dict() for question in questions]
        return json.dumps(serializable_questions)
    
    def __repr__(self):
        questions = self.get_questions()
        questions_string = [str(question) for question in questions]
        return " ".join(questions_string)

    def parse_questions_to_str(self):
        questions = self.get_questions()
        serializable_questions = [question.to_dict() for question in questions]
        quiz_string = "Test"
        for question in serializable_questions:
            quiz_string += '\n\n Question:' + question["question"] + '\n\n' + '\n'.join(question["choices"])
            quiz_string+='\n\n' + "Correct Answer: " +  question['answer']
        return quiz_string