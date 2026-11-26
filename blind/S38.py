import ast

def parse_dict(text):
    result = ast.literal_eval(text)
    if not isinstance(result, dict):
        raise ValueError("Input must represent a dictionary")
    return result
