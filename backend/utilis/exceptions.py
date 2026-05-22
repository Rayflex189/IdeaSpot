import re

def validate_username(value):
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValueError('Invalid username')
    return value
