class TextContainer:
    def __init__(self, text_string=""):
        self._text_string = text_string
    
    def set_text_string(self, text_string):
        self._text_string = text_string
    
    def get_text_string(self):
        return self._text_string
    
    def __repr__(self):
        return self.get_text_string()