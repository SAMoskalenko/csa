from protocol import make_response
from decorators import logged
from database import Session
from echo.models import Message
from auth.models import User
from functools import reduce


@logged
def echo_controller(request):
    data = request.get('data')
    session = Session()
    response = Message(data=data, action='echo', user_id=1)
    session.add(response)
    session.commit()
    return make_response(request, 200, data)


@logged
def get_echo_messages_controller(request):
    session = Session()
    messages = reduce(
        lambda value, item: value + [
            {'action': item.action, 'data': item.data, 'created': item.created, 'user_id': item.user_id, }],
        # session.query(Message).filter(Message.action == 'echo').all(),
        session.query(Message).all(),
        []
    )
    return make_response(request, 200, messages)


@logged
def update_messages_controller(request):
    id_el = request.get('id_el')
    data = request.get('data')
    session = Session()
    message = session.query(Message).filter(Message.id == int(id_el)).first()
    message.data = data
    session.add(message)
    session.commit()
    return make_response(request, 200, data)


@logged
def delete_messages_controller(request):
    id_el = request.get('id_el')
    session = Session()
    message = session.query(Message).filter(Message.id == int(id_el)).first()
    session.delete(message)
    session.commit()
    return make_response(request, 200)
