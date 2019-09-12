import hmac
from datetime import datetime
from functools import reduce

from server.database import session_scope
from server.protocol import make_response

from .decorators import login_required
from .utils import authenticate, login
from .settings import SECRET_KEY
from .models import User, Session

from server.database import Session as sess

from server.decorators import logged


def registration_controller(request):
    errors = {}
    is_valid = True
    data = request.get('data')

    if not 'password' in data:
        errors.update({'password': 'Attribute is required'})
        is_valid = False

    if not 'login' in data:
        errors.update({'login': 'Attribute is required'})
        is_valid = False

    if not is_valid:
        return make_response(request, 400, {'errors': errors})

    hmac_obj = hmac.new(SECRET_KEY.encode(), data.get('password').encode())
    password_digest = hmac_obj.hexdigest()

    with session_scope() as db_session:
        user = User(name=data.get('login'), password=password_digest)
        db_session.add(user)
    token = login(request, user)
    return make_response(request, 200, {'token': token})


def login_controller(request):
    errors = {}
    is_valid = True
    data = request.get('data')


    if not 'time' in request:
        errors.update({'time': 'Attribute is required'})
        is_valid = False

    if not 'password' in data:
        errors.update({'password': 'Attribute is required'})
        is_valid = False

    if not 'login' in data:
        errors.update({'login': 'Attribute is required'})
        is_valid = False

    if not is_valid:
        return make_response(request, 400, {'errors': errors})

    user = authenticate(data.get('login'), data.get('password'))

    if user:
        token = login(request, user)
        return make_response(request, 200, {'token': token})

    return make_response(request, 400, 'Enter correct login or password')


@login_required
def logout_controller(request):
    with session_scope() as db_session:
        user_session = db_session.query(Session).filter_by(token=request.get('token')).first()
        user_session.closed = datetime.now()
        return make_response(request, 200, 'Session closed')


@logged
def get_user_controller(request):
    session = sess()
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
    session = sess()
    message = session.query(User).filter(User.id == int(id_el)).first()
    message.password = password
    session.add(message)
    session.commit()
    return make_response(request, 200, 'Password changed ')


@logged
def delete_user_controller(request):
    id_el = request.get('id_el')
    session = sess()
    message = session.query(User).filter(User.id == int(id_el)).first()
    session.delete(message)
    session.commit()
    return make_response(request, 200)
