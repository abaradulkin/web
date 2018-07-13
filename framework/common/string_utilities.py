import string
from random import choice


def get_random_string(lenght=8):
    return ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(lenght))
