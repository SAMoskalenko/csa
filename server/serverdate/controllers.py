from datetime import datetime
from protocol import make_response
from database import Session
from base.models import Message
from auth.models import User
from decorators import logged

from functools import reduce


@logged
def server_date_controller(request):
    session = Session()
    response = Message(data=str(datetime.now().timestamp()), action='serverdate')
    session.add(response)
    session.commit()
    return make_response(request, 200, datetime.now().timestamp())


@logged
def get_echo_messages_controller(request):
    session = Session()
    messages = reduce(
        lambda value, item: value + [
            {'action': item.action, 'data': item.data, 'created': item.created.timestamp(), 'user_id': item.user_id}],
        session.query(Message).filter_by(action='serverdate').all(),
        []
    )
    return make_response(request, 200, messages)
