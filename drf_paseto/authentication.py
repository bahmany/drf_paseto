# drf_paseto/authentication.py

import paseto
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

# Secret key for PASETO (must be kept safe)
SECRET_KEY = settings.SECRET_KEY.encode()  # Ensure this key is securely stored

class PasetoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            # Verify the PASETO token
            payload = paseto.parse(key=SECRET_KEY, purpose='local', token=token)
            username = payload.get('sub')
            if not username:
                raise AuthenticationFailed('Invalid token payload')

            # Fetch the user from the database
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise AuthenticationFailed('No such user')

            return (user, None)

        except paseto.PasetoException as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

    @staticmethod
    def generate_token(user):
        # Generate a PASETO token for the authenticated user
        payload = {
            'sub': user.username,
            'exp': (datetime.utcnow() + timedelta(hours=24)).isoformat()  # Token expiry set to 24 hours
        }
        token = paseto.create(key=SECRET_KEY, purpose='local', claims=payload)
        return token
