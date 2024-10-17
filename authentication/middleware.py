# middleware.py
from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import login

User = get_user_model()

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем JWT токен в сессии
        jwt_token = request.session.get('jwt_token')
        
        if jwt_token and not request.user.is_authenticated:
            try:
                # Проверяем валидность токена
                token = AccessToken(jwt_token)
                user_id = token.payload.get('user_id')
                user = User.objects.get(id=user_id)
                login(request, user)
            except Exception:
                if 'jwt_token' in request.session:
                    del request.session['jwt_token']

        response = self.get_response(request)
        return response