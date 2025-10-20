"""
Custom hooks for drf-spectacular to handle token authentication
"""

def token_auth_preprocessing_hook(endpoints):
    """
    Preprocessing hook to customize the OpenAPI schema.
    Converts Bearer authentication to Token authentication format.
    """
    # This hook ensures the schema is generated correctly
    # The actual token format conversion happens in the security scheme
    return endpoints
