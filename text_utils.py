from gptprocessor import OPENAI_MAX_PROMPT_LEN

def split_text_into_chunks(text_string, max_prompt_len=OPENAI_MAX_PROMPT_LEN):
    split_text = text_string.split()
    max_prompt_len = int(max_prompt_len)
    return [split_text[i:i+max_prompt_len] for i in range(0,len(split_text),max_prompt_len)]


def check_argument_types(*arg_types ):
    def decorator(func):
        def wrapper(*args , **kwargs ) :
            for arg, arg_type in zip(args, arg_types):
                if not isinstance(arg, arg_type):
                    raise TypeError(f"Expected {arg_type.__name__}, but got {type(arg).__name__} for argument {arg}")

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator