# backend/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import bcrypt, json
from .database.database import Database
from .database.database_types import TypeBase, User, Product, Transaction, Message

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

database = Database()

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
def homepage(request):
    products = database.get_homepage()
    data = {
        'products': products
    }
    return JsonResponse(data)

@api_view(['POST'])
def login(request):
    data = json.loads(request.body)

    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = data.get('email')
    password = data.get('password')

    user = database.can_login(email, password)
    if user is None:
        return Response("Login rejected by database", status=400)

    return Response({
        'status': 'success',
        'message': 'Login successful',
        'email': email
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
    if database.add_user(new_user) is not None:
        return HttpResponse(f"User successfully registered", status=201)
    else:
        return HttpResponse(f"Failed to register user - user already exists", status=400)
