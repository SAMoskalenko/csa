from protocol import make_response


def echo_controller(request):
    data = request.get('data')
    print('data = ', data)
    print(type(data))
    return make_response(request, 200, data)
