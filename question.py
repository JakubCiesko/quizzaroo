class Question:
    def __init__(self):
        self._question_wording = ""
        self._answer = None
        self._choices = None
    
    def set_question_wording(self, question_wording:str):
        self._question_wording = question_wording
    
    def get_question_wording(self):
        return self._question_wording

    def get_answer(self):
        return self._answer
    
    def set_answer(self, answer):
        self._answer = answer
    
    def set_choices(self, choices):
        self._choices = choices 
    
    def get_choices(self):
        return self._choices

    def __repr__(self):
        return self.get_question_wording()
    
    def to_dict(self):
        return {"question": self._question_wording, "answer": self._answer, "choices": self._choices}



    