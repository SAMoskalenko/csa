from .controllers import update_messages_controller, delete_messages_controller

actionnames = [{
        'action': 'update_message',
        'controller': update_messages_controller
    },
    {
        'action': 'delete_message',
        'controller': delete_messages_controller
    },
]
