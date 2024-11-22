# backend/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse
import bcrypt, json
from .database.database import *
from .database.market_types import User

@api_view(['GET', 'POST'])
def test_connection(request):
    if request.method == 'GET':
        return Response({
            'status': 'connected',
            'method': 'GET',
            'message': 'Django and React are successfully connected!',
            'timestamp': datetime.now().isoformat(),  # Add current time
            'test_data': {
                'number': 42,
                'list': [1, 2, 3],
                'nested': {'key': 'value'}
            }
        })
    elif request.method == 'POST':
        data = request.data
        return Response({
            'status': 'received',
            'method': 'POST',
            'received_data': data,
            'message': 'Data successfully received by Django!'
        })
    
@api_view(['POST'])
def register(request):
    data = json.loads(request.body)

    # Get fields from register request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Hash password before storing in database
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    new_user = User(username, email, hash)
    if can_register(new_user):
        add_user(new_user)
        return HttpResponse(f"User successfully registered", status=201)
    else:
        return HttpResponse(f"Failed to register user", status=400)

    # Return a response
