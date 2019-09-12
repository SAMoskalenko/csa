from functools import reduce

from server.protocol import make_response
from server.decorators import logged
from server.database import Session

from server.base.models import Message

'''
API echo controllers
'''

@logged
def echo_controller(request):
    '''
    echo controller

    Creating new echo message

    :param request:
        {'action': 'echo', 'data': ''}
    :return:
        {request, 200, data}
    '''
    data = request.get('data')
    session = Session()
    response = Message(data=data.get('data'), action='echo')
    session.add(response)
    session.commit()
    session.close()
    return make_response(request, 200, data)


@logged
def get_echo_messages_controller(request):
    '''
    get echo nmessages controller

    Getting a collection of messages where action 'echo'

    :param request:
        {'action': 'get_echo', 'data' = None}
    :return:
        All echo messages
    '''
    session = Session()
    messages = reduce(
        lambda value, item: value + [
            {'action': item.action, 'data': item.data, 'created': item.created.timestamp(), 'user_id': item.user_id}],
        session.query(Message).filter_by(action='echo').all(),
        []
    )
    return make_response(request, 200, messages)
