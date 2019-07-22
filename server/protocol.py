def validate_request(data):
    if 'action' in data and 'time' in data:
        return True
    else:
        return False

def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code
    }