from datetime import datetime
from server.protocol import make_response
from server.database import Session
from server.base.models import Message
from server.auth.models import User
from server.decorators import logged

from functools import reduce


@logged
def server_date_controller(request):
    session = Session()
    response = Message(data=str(datetime.now().timestamp()), action='serverdate')
    session.add(response)
    session.commit()
    return make_response(request, 200, datetime.now().timestamp())



