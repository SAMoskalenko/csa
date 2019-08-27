import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_MODULES = [
    'base',
    'auth',
    'echo',
    'empty',
    'serverdate',
    'servererrors',
]

CONNECTION_STRING = 'sqlite:///chat.db'
