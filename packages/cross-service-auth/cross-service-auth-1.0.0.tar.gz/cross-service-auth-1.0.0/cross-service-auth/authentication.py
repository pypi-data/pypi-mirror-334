from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken

class RequestUser:
    """
    A class for dynamically creating a user based on data from JWT.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class CrossServiceJWTAuthentication(JWTAuthentication):
    """
    A custom JWT authentication class for authenticating users between microservices.
    """

    def authenticate(self, request):
        token = self._get_token_from_header(request)
        validated_token = self._validate_token(token)
        user_data = self._extract_user_data(validated_token)

        user = RequestUser(**user_data)

        return user, validated_token

    @staticmethod
    def _get_token_from_header(request):
        """
        Get the token from the Authorization header.
        """
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthenticationFailed('Authorization header missing')

        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Authorization header must start with Bearer')

        return auth_header.split(' ')[1]

    @staticmethod
    def _validate_token(token):
        """
        Validate the token.
        """
        try:
            return UntypedToken(token)
        except Exception as e:
            raise AuthenticationFailed(f'Token is invalid: {str(e)}')

    @staticmethod
    def _extract_user_data(validated_token):
        """
        Extract data from the validated token.
        """
        user_data = validated_token.payload
        return {
            'subscription_service_id': user_data.get('subscription_service_id'),
            'roles': user_data.get('roles', []),
            'email': user_data.get('email', ''),
            'is_authenticated': True
        }
