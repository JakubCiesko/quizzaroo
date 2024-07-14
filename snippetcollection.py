from textsnippet import TextSnippet
from text_utils import check_argument_types

class SnippetCollection:
    def __init__(self):
        self._snippet_collection = []
    
    def set_snippets(self, snippets):
        self._snippet_collection = snippets
    
    def get_snippets(self):
        return self._snippet_collection
    
    def add_snippet(self, snippet):
        self._snippet_collection.append(snippet)

    def pop_snippet(self, snippet):
        self.get_snippets().remove(snippet)

    def pop(self):
        self.get_snippets().pop()

    def pop_index(self, index):
        self.get_snippets().pop(index)

    def __repr__(self):
        snippets = self.get_snippets()
        return "\n".join([str(snippet) for snippet in snippets])
    
    def __iter__(self):
        return iter(self.get_snippets())

    def __getitem__(self, index):
        return self._snippet_collection[index]

    def __setitem__(self, index, value):
        self._snippet_collection[index] = value

