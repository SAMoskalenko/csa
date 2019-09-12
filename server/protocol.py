'''
Protocol API documentation
'''


def validate_request(data):
    '''
    function for validate simple client request
    :param data: raw client request
    :return: bool value -validation solutions

    - Example:

        {'action':'echo', 'time': ''}
    '''

    if 'action' in data and 'time' in data:
        return True
    return False


def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code
    }
