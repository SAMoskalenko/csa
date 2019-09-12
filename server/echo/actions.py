'''
API echo actions

Connecting actionnames with controllers
- Example:

        {'action':'actionname', 'controller': 'controller'}
'''

from .controllers import echo_controller, get_echo_messages_controller

actionnames = [
    {'action': 'echo', 'controller': echo_controller},
    {'action': 'get_echo', 'controller': get_echo_messages_controller}
]
