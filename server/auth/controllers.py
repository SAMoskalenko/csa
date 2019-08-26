from protocol import make_response
from decorators import logged
from database import Session
from auth.models import User
from functools import reduce


@logged
def user_controller(request):
    name = request.get('name')
    password = request.get('password')
    session = Session()
    response = User(name=name, password=password)
    session.add(response)
    session.commit()
    return make_response(request, 200, f'User {name} create')


@logged
def get_user_controller(request):
    session = Session()
    users = reduce(
        lambda value, item: value + [{'user': item.user}],
        session.query(User).all(),
        []
    )

    return make_response(request, 200, users)


@logged
def update_user_controller(request):
    id_el = request.get('id_el')
    password = request.get('password')
    session = Session()
    message = session.query(User).filter(User.id == int(id_el)).first()
    message.password = password
    session.add(message)
    session.commit()
    return make_response(request, 200, 'Password changed ')


@logged
def delete_user_controller(request):
    id_el = request.get('id_el')
    session = Session()
    message = session.query(User).filter(User.id == int(id_el)).first()
    session.delete(message)
    session.commit()
    return make_response(request, 200)
