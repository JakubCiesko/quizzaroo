from gptprocessor import GPTProcessor


mark_summary_prompt_postfix = " Mark the summary out of 10. Return the marked value only."
class SummaryChecker(GPTProcessor):
    summary_system_role_prompt = "You are ReviewerGPT, a machine which takes two texts as its input and decides whether one of them is a good summary of the other." + mark_summary_prompt_postfix
    def __init__(self):
        self._original_text = None
        self._summary = None
    
    def set_original_text(self, text):
        self._original_text = text
    
    def get_original_text(self):
        return self._original_text 
    
    def set_summary(self, summary):
        self._summary = summary
    
    def get_summary(self):
        return self._summary
    
    def squeeze_texts_in_prompt(self):
        original_text = self.get_original_text()
        summary = self.get_summary()
        prompt = f"Original text: {original_text}\nSummary: {summary}"
        self.set_prompt(prompt)
        return prompt

    def check_summary(self):
        original_text = self.get_original_text()
        summary = self.get_summary()
        summary_check_response = ""
        if original_text and summary:    
            self.squeeze_texts_in_prompt()
            model = self.get_model()
            messages = self.create_messages(self.summary_system_role_prompt)
            summary_check_response = self.get_response(model, messages)  
        return summary_check_response
    
