## Installation Guide for `drf-paseto-auth`

`drf-paseto-auth` is a Django REST Framework authentication backend that uses PASETO (Platform-Agnostic Security Tokens) for secure authentication.

### Step 1: Install the Package

First, you need to install the package. If the package is published on PyPI, you can install it using `pip`. Otherwise, if you're installing it from a local build, follow the steps below.

```bash
pip install drf-paseto-auth
```

If you are installing it from a local repository, clone the repository and install it:

```bash
git clone https://github.com/yourusername/drf-paseto-auth.git
cd drf-paseto-auth
pip install .
```

### Step 2: Add the Package to Your Installed Apps

Add `drf_paseto_auth` to the `INSTALLED_APPS` in your Django project's `settings.py` file:

```python
INSTALLED_APPS = [
    ...
    'drf_paseto_auth',
    ...
]
```

### Step 3: Update Django REST Framework Authentication Settings

Update the `REST_FRAMEWORK` settings in your `settings.py` file to use `PasetoAuthentication` as the default authentication class:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drf_paseto_auth.authentication.PasetoAuthentication',
    ),
}
```

### Step 4: Set Your PASETO Secret Key

Ensure that you have a secure secret key set up in your `settings.py` file. This key will be used to sign and verify the PASETO tokens.

```python
SECRET_KEY = 'your-very-secure-and-random-secret-key'
```

You should replace `'your-very-secure-and-random-secret-key'` with a secure, randomly generated string. 

### Step 5: Create a Login View to Generate PASETO Tokens

Create a new view in your Django app to authenticate users and generate PASETO tokens. Add the following code to your `views.py`:

```python
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_paseto_auth.authentication import PasetoAuthentication

class LoginView(APIView):
    authentication_classes = []  # No authentication needed for login

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token = PasetoAuthentication.generate_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
```

### Step 6: Add URLs for the Login View

Add a URL pattern to your `urls.py` file to expose the login view:

```python
from django.urls import path
from .views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
```

### Step 7: Protect Your API Endpoints

To protect your API endpoints with PASETO authentication, use the `IsAuthenticated` permission class. The custom `PasetoAuthentication` class will handle token verification.

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'This is a protected view.'})
```

### Step 8: Test the Setup

1. **Start the Django development server**:

    ```bash
    python manage.py runserver
    ```

2. **Login to get a PASETO token**:

   Send a `POST` request to the `/login/` endpoint with a valid `username` and `password`. You will receive a PASETO token in the response.

3. **Access Protected Endpoints**:

   Use the received token to access protected endpoints by including it in the `Authorization` header as a Bearer token:

   ```
   Authorization: Bearer <your-paseto-token>
   ```

### Conclusion

By following these steps, you have successfully installed and configured `drf-paseto-auth` for PASETO-based authentication in your Django REST Framework project. This setup ensures a more secure token-based authentication mechanism compared to JWT.

