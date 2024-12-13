# backend/api/views.py
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import bcrypt, json, logging
from .database.database import Database
from .database.database_types import TypeBase, User, Product, Transaction, Message

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import LoginSerializer
from .session_manager import SessionManager

database = Database()
session_manager = SessionManager(database)

logger = logging.getLogger(__name__)

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

@api_view(['GET'])
def homepage(request):
    products = database.get_homepage()
    product_array = []
    for product in products:
        product_array.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'owner_id': product.owner_id
        })
    return JsonResponse({'products': product_array})

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

    token = session_manager.add_authorized_user(user.id, user.email)

    return Response({
        'status': 'success',
        'message': 'Login successful',
        'username': user.username,
        'email': email,
        'token': token
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
    if database.add_user(new_user) is None:
        return HttpResponse(f"Failed to register user - user already exists", status=400)

    token = session_manager.add_authorized_user(new_user.id, email)

    return Response({
        'status': 'success',
        'message': 'Registration successful',
        'username': username,
        'email': email,
        'token': token
    })

@api_view(['POST'])
def add_product(request):
    user = session_manager.get_authorized_user(request)
    if user is None:
        return Response("Access denied", status=400)
    
    data = json.loads(request.body)

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    availability = data.get('availability')

    product = Product(name, description, price, user.id)
    database.add_product(product)

    return JsonResponse({
        'product_id': product.id
    })

@api_view(['GET'])
def get_products(request):

    user = session_manager.get_authorized_user(request)
    if user is None:
        return Response("Access denied", status=400)

    products = database.list_products(user.id)
    products_json = []
    for product in products:
        products_json.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'owner_id': product.owner_id
        })

    return JsonResponse({'products': products_json})

@api_view(['POST'])
def delete_product(request):
    user = session_manager.get_authorized_user(request)
    if user is None:
        return Response("Access denied", status=400)

    data = json.loads(request.body)
    id = data.get('id')

    if database.delete_product(id):
        return Response({'status': 'success', 'message': 'Successfully deleted product'})
    else:
        return Response("Failed to delete product", status=400)


@api_view(['GET'])
def search(request):
    query = request.GET.get('query')

    # TODO
    return Response({
        'status': 'success',
        'message': 'Backend received request to search. Search not yet implemented.'
    })
