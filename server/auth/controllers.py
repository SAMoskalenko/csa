import hmac
from datetime import datetime
from functools import reduce

from database import session_scope
from protocol import make_response

from .decorators import login_required
from .utils import authenticate, login
from .settings import SECRET_KEY
from .models import User, Session

from database import Session as sess

from decorators import logged


def registration_controller(request):
    errors = {}
    is_valid = True

    if not 'password' in request:
        errors.update({'password': 'Attribute is required'})
        is_valid = False

    if not 'login' in request:
        errors.update({'login': 'Attribute is required'})
        is_valid = False

    if not is_valid:
        return make_response(request, 400, {'errors': errors})

    hmac_obj = hmac.new(SECRET_KEY, request.get('password'))
    password_digest = hmac_obj.digest()

    with session_scope() as db_session:
        user = User(name=request.get('login'), password=password_digest)
        db_session.add(user)
        token = login(request, user)
        return make_response(request, 200, {'token': token})


def login_controller(request):
    errors = {}
    is_valid = True

    if not 'time' in request:
        errors.update({'time': 'Attribute is required'})
        is_valid = False

    if not 'password' in request:
        errors.update({'password': 'Attribute is required'})
        is_valid = False

    if not 'login' in request:
        errors.update({'login': 'Attribute is required'})
        is_valid = False

    if not is_valid:
        return make_response(request, 400, {'errors': errors})

    user = authenticate(request.get('login'), request.get('password'))

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
