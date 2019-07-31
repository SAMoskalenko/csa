from protocol import make_response
from decorators import login_request

@login_request
def server_error_controller(request):
    raise Exception('Server error message')