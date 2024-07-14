from gptprocessor import OPENAI_MAX_PROMPT_LEN
from textcontainer import TextContainer
from textsnippet import TextSnippet
from snippetcollection import SnippetCollection
from text_utils import split_text_into_chunks

class Text(TextContainer):

    def __init__(self, text_string=""):
        super().__init__(text_string)

    def split_into_snippets(self, snippet_size=OPENAI_MAX_PROMPT_LEN):
        snippet_collection = SnippetCollection()
        text_string = self.get_text_string()
        snippets_strings = split_text_into_chunks(text_string, snippet_size)
        snippets = [TextSnippet(" ".join(snippet_string)) for snippet_string in snippets_strings]
        snippet_collection.set_snippets(snippets)
        return snippet_collection
    
    def split_into_snippets_on_char(self, char):
        snippet_collection = SnippetCollection()
        text_string = self.get_text_string()
        snippets_strings = text_string.split(sep=char)
        snippets = [TextSnippet(" ".join(snippet_string)) for snippet_string in snippets_strings]
        snippet_collection.set_snippets(snippets)
        return snippet_collection


        
