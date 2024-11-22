# backend/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

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
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response({
            'status': 'success',
            'message': 'Login successful',
            'email': serializer.validated_data['email']
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)