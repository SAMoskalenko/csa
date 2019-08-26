from .controllers import echo_controller, get_echo_messages_controller, update_messages_controller, \
    delete_messages_controller

actionnames = [{
    'action': 'echo',
    'controller': echo_controller
},
    {
        'action': 'get_echo',
        'controller': get_echo_messages_controller
    },
    {
        'action': 'update_message',
        'controller': update_messages_controller
    },
    {
        'action': 'delete_message',
        'controller': delete_messages_controller
    },
]
