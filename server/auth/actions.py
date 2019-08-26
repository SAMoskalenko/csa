from .controllers import user_controller, get_user_controller, update_user_controller, delete_user_controller

actionnames = [{
    'action': 'user',
    'controller': user_controller
},
    {
        'action': 'get_user',
        'controller': get_user_controller
    },
    {
        'action': 'update_user',
        'controller': update_user_controller
    },
    {
        'action': 'delete_user',
        'controller': delete_user_controller
    },
]
