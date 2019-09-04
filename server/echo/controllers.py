from functools import reduce

from protocol import make_response
from decorators import logged
from database import Session

from base.models import Message



@logged
def echo_controller(request):
    data = request.get('data')
    session = Session()
    response = Message(data=data, action='echo', user_id=1)
    session.add(response)
    session.commit()
    session.close()
    return make_response(request, 200, data)


@logged
def get_echo_messages_controller(request):
    session = Session()
    messages = reduce(
        lambda value, item: value + [
            {'action': item.action, 'data': item.data, 'created': item.created.timestamp(), 'user_id': item.user_id}],
        session.query(Message).filter_by(action='echo').all(),
        []
    )
    return make_response(request, 200, messages)
