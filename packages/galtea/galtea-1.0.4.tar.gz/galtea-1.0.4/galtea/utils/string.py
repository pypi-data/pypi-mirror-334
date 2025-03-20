import random
import re
import string
import json

def sanitize_string(string: str) -> str:
    """
    Given the string, returns a sanitized version of it.
    """
    return re.sub(r"[\"<>:/.+\|\\?\*\[\]]+", "__", string)

def generate_random_string(length: int = 8) -> str:
    """
    Generates a random string of the given length.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def load_json(file_path: str, encoding: str = None) -> dict:
    """
    Loads a JSON file and returns the contents as a dictionary.
    """
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)

def build_query_params(**params):
    """
    Build a query string from given parameters, excluding any that are None.
    :param params: Dictionary of query parameters
    :return: A query string
    """
    query_parts = []
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, list):
            # Handle list values by repeating the key for each item
            query_parts.extend(f"{key}[]={item}" for item in value)
        else:
            query_parts.append(f"{key}={value}")
    return "&".join(query_parts)