from datetime import datetime
from protocol import make_response
from database import Session
from echo.models import Message
from auth.models import User


def server_date_controller(request):
    session = Session()
    response = Message(data=str(datetime.now().timestamp()), action='serverdate')
    session.add(response)
    session.commit()
    return make_response(request, 200, datetime.now().timestamp())
