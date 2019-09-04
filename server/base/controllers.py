from protocol import make_response
from decorators import logged
from database import Session
from base.models import Message


@logged
def update_messages_controller(request):
    id_el = request.get('id_el')
    data = request.get('data')
    session = Session()
    message = session.query(Message).filter(Message.id == int(id_el)).first()
    message.data = data
    session.add(message)
    session.commit()
    session.close()
    return make_response(request, 200, data)


@logged
def delete_messages_controller(request):
    id_el = request.get('id_el')
    session = Session()
    message = session.query(Message).filter(Message.id == int(id_el)).first()
    session.delete(message)
    session.commit()
    session.close()
    return make_response(request, 200)
