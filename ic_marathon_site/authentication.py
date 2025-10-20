"""
Custom authentication class to handle both Token and Bearer prefixes
"""
from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication that accepts both 'Token' and 'Bearer' prefixes.
    This allows Swagger UI to use 'Bearer <token>' while maintaining compatibility
    with 'Token <token>' format.
    """
    keyword = ['Token', 'Bearer']
    
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if not auth or auth[0].lower() not in [k.lower() for k in self.keyword]:
            return None
        
        if len(auth) == 1:
            return None
        elif len(auth) > 2:
            return None
        
        # Use the token (second part) regardless of prefix
        return self.authenticate_credentials(auth[1])
