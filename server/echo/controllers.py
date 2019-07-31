from protocol import make_response
from decorators import logged


@logged
def echo_controller(request):
    data = request.get('data')
    print('data = ', data)
    print(type(data))
    return make_response(request, 200, data)
