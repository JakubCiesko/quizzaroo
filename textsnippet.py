from textcontainer import TextContainer

class TextSnippet(TextContainer):
    def __init__(self, text_snippet_string):
        super().__init__(text_snippet_string)
        self._location = ()
    
    def set_location(self, location):
        self._location = location
    
    def get_location(self):
        return self._location
    
    def __eq__(self, other) -> bool:
        if type(other) == TextSnippet:
            self._text_string == other._text_string
            return True
        return False
    

    
    

