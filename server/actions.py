'''
API echo actions
'''


from server.echo.controllers import echo_controller, get_echo_messages_controller

'''
Connecting actionnames with controllers
- Example:

        {'action':'actionname', 'controller': 'controller'}
'''

actionnames = [
    {'action': 'echo', 'controller': echo_controller},
    {'action': 'get_echo', 'controller': get_echo_messages_controller}
]
