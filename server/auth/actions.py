from .controllers import registration_controller, login_controller, logout_controller, get_user_controller, \
    update_user_controller, delete_user_controller

actionnames = [
    {'action': 'registrate','controller': registration_controller},
    {'action': 'login', 'controller': login_controller},
    {'action': 'logout', 'controller': logout_controller},
    {'action': 'get_user', 'controller': get_user_controller},
    {'action': 'update_user', 'controller': update_user_controller},
    {'action': 'delete_user', 'controller': delete_user_controller},
]
