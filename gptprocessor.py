import openai

OPENAI_MAX_PROMPT_LEN = 2048/2      # input + output expected size sum (tokens)

class GPTProcessor:
    def __init__(self) -> None:
        self._api_key = ""
        self._prompt = "Who are you?"
        self._model = "gpt-3.5-turbo"
        self._logger_fn = None 
        self._update_fn = None

    def set_api_key(self, api_key: str):
        """
        Sets openai api key to the given api_key

        :param api_key: open ai api key
        :type api_key: str
        :return: None
        """
        openai.api_key = api_key
        self._api_key = api_key

    def get_api_key(self) -> str:
        """
        Returns set openai api key

        :return: str
        """
        return self._api_key
    
    def set_prompt(self, prompt: str):
        """
        Sets prompt to given prompt str value.

        :param prompt: ChatGPT prompt
        :type prompt: str
        :return: None
        """
        self._prompt = prompt 

    def get_prompt(self) -> str:
        """
        Return set ChatGPT prompt.

        :return: str
        """
        return self._prompt
    
    def set_model(self, model: str):
        """
        Sets OpenAI model
        """
        self._model = model 
    
    def get_model(self) -> str:
        """
        Returns set OpenAI model
        """
        return self._model
    """
    def get_update_fn(self):
        if self._update_fn:
            return self._update_fn
        return None
    
    def set_update_fn(self, fn):
        self._update_fn = fn
    
    def get_logger_fn(self):
        if self._logger_fn:
            return self._logger_fn
        return None
    
    def set_logger_fn(self, logger_fn):
        self._logger_fn = logger_fn
    """
    def __eq__(self, other) -> bool:
        if isinstance(other, GPTProcessor):
            return self._api_key == other._api_key
        else: 
            return False 
        
    def send_prompt_request(self, pre_messages="", post_messages="", system_role_message="You are a helpful assistant.") -> str:
        """
        Sends prompt request to ChatGPT, returns response string.

        :param pre_messages:
        :type pre_messages: list
        :return: str
        """
        model = self.get_model()
        if pre_messages:
            messages = [
                {"role": "system", "content": system_role_message},
                *pre_messages, 
                {"role": "user", "content": self.get_prompt()}
                ]
        elif post_messages:
            messages = [
                {"role": "system", "content": system_role_message},
                {"role": "user", "content": self.get_prompt()},
                *post_messages
                ]
        else:
            messages = [
                {"role": "system", "content": system_role_message},
                {"role": "user", "content": self.get_prompt()}
                ] 
                    #Flatten + :limit
        if len((self.get_prompt() + " " + str(pre_messages) + " " + str(post_messages)).split()) > OPENAI_MAX_PROMPT_LEN:      #ADD REITERATION 
            raise ValueError(f'The prompt is too long, the maximum length is: {OPENAI_MAX_PROMPT_LEN}, yours is: {len(self.get_prompt())}')
        response = self.get_response(model, messages).strip()
        return response

    def get_chat_completion(self, model, messages):
        chat = openai.ChatCompletion.create(
            model=model,
            messages=messages)
        response = chat.choices[0].message.content
        return response 

    def get_completion(self, model, messages):
        message_token_len_percentage = 1.2 
        messages = " ".join([message["content"] for message in messages])
        token_limit = int(message_token_len_percentage*len(messages))
        response = openai.Completion.create( model=model, prompt=messages, max_tokens=token_limit)
        response = response.choices[0].text
        return response

    def get_response(self, model, messages):
        open_ai_model_function_table = {
            "gpt-3.5-turbo": self.get_chat_completion,
            "gpt-4": self.get_chat_completion,
            "text-davinci-003": self.get_completion
        }
        response = ""
        """
        try: 
            
        except Exception as e:
            tb = str(e) + "\n" + traceback.format_exc() 
            print(tb)
            logger.error(str(e))
        """
        response = open_ai_model_function_table[model](model, messages)
        return response
    
    def create_messages(self, system_role_message="You are a helpful assistant."):
        messages = [
                {"role": "system", "content": system_role_message},
                {"role": "user", "content": "The text: " + self.get_prompt()}
        ]
        return messages
