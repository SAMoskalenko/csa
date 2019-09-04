from .controllers import echo_controller, get_echo_messages_controller

actionnames = [
    {'action': 'echo', 'controller': echo_controller},
    {'action': 'get_echo', 'controller': get_echo_messages_controller}
]
