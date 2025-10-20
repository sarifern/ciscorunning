"""
Custom authentication views for Strava OAuth integration
"""
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    summary="Authenticate with Strava OAuth token",
    description="""
    Exchange a Strava access token for a Django REST Framework token.
    
    **Authentication Flow:**
    1. Frontend completes Strava OAuth flow and receives access token
    2. Frontend sends access token to this endpoint
    3. Backend validates token with Strava API
    4. Backend creates/retrieves user using Strava username and returns Django token
    
    **What happens:**
    - Token is validated by calling Strava's `/api/v3/athlete` endpoint
    - Username is automatically extracted from Strava athlete data
    - New users are automatically created with Strava profile data
    - Strava account is linked to Django user via SocialAccount
    - Existing users are matched by Strava ID
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'strava_access_token': {
                    'type': 'string',
                    'description': 'Access token received from Strava OAuth',
                    'example': 'a1b2c3d4e5f6...'
                }
            },
            'required': ['strava_access_token']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'token': {'type': 'string', 'example': '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'},
                'user': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'username': {'type': 'string'},
                        'email': {'type': 'string'},
                        'first_name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'strava_id': {'type': 'string'}
                    }
                },
                'created': {'type': 'boolean', 'description': 'True if new user was created'}
            }
        },
        400: {'description': 'Missing required fields'},
        401: {'description': 'Invalid Strava token'},
        403: {'description': 'Strava account mismatch'},
        503: {'description': 'Failed to communicate with Strava API'}
    },
    examples=[
        OpenApiExample(
            'Successful Authentication',
            value={
                'token': '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b',
                'user': {
                    'id': 1,
                    'username': 'johndoe',
                    'email': 'john@example.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'strava_id': '12345678'
                },
                'created': False
            },
            response_only=True,
            status_codes=['200']
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def strava_token_auth(request):
    """
    Authenticate user with Strava access token.
    
    Frontend sends Strava access token after OAuth flow.
    Backend validates token with Strava API, extracts username from Strava data,
    and returns Django token.
    
    Request Body:
    {
        "strava_access_token": "abc123..."
    }
    
    Response:
    {
        "token": "django-token-here",
        "user": {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "strava_id": "12345678"
        }
    }
    """
    strava_access_token = request.data.get('strava_access_token')
    
    if not strava_access_token:
        return Response({
            'error': 'strava_access_token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate Strava token by calling Strava API
    try:
        strava_response = requests.get(
            'https://www.strava.com/api/v3/athlete',
            headers={'Authorization': f'Bearer {strava_access_token}'},
            timeout=10
        )
        
        if strava_response.status_code != 200:
            return Response({
                'error': 'Invalid Strava access token',
                'detail': 'Token validation failed with Strava API'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        strava_user_data = strava_response.json()
        strava_id = str(strava_user_data.get('id'))
        
        # Extract username from Strava data, fallback to strava_ID if no username
        username = strava_user_data.get('username') or f'strava_{strava_id}'
        
    except requests.RequestException as e:
        return Response({
            'error': 'Failed to validate Strava token',
            'detail': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Find or create user by Strava ID first (more reliable than username)
    try:
        # Try to find existing user by Strava ID
        social_account = SocialAccount.objects.get(provider='strava', uid=strava_id)
        user = social_account.user
        
        # Update user info from Strava in case it changed
        user.email = strava_user_data.get('email', user.email)
        user.first_name = strava_user_data.get('firstname', user.first_name)
        user.last_name = strava_user_data.get('lastname', user.last_name)
        user.save()
        
        # Update extra_data in SocialAccount
        social_account.extra_data = strava_user_data
        social_account.save()
            
    except SocialAccount.DoesNotExist:
        # No existing Strava account found, create new user
        # Ensure username is unique
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{base_username}{counter}'
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=strava_user_data.get('email', f'{username}@strava.user'),
            first_name=strava_user_data.get('firstname', ''),
            last_name=strava_user_data.get('lastname', '')
        )
        
        # Link Strava account
        SocialAccount.objects.create(
            user=user,
            provider='strava',
            uid=strava_id,
            extra_data=strava_user_data
        )
    
    # Get or create Django REST Framework token
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'strava_id': strava_id
        },
        'created': created  # True if new user was created
    }, status=status.HTTP_200_OK)
