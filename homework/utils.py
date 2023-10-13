from random import choice
from string import ascii_letters, digits


def gen_x_request_id():
    character_pool = ascii_letters + digits + '-_'
    return ''.join([choice(character_pool) for _ in range(20)])
