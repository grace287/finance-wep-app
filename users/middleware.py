from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.middleware import get_user

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.get_jwt_user(request))
        return self.get_response(request)

    def get_jwt_user(self, request):
        user = get_user(request)
        if user.is_authenticated:
            return user
            
        # 쿠키에서 토큰 추출
        access_token = request.COOKIES.get('access_token')
        if access_token:
            # 헤더에 토큰 추가
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            
            # JWT 인증
            auth = JWTAuthentication()
            try:
                validated_token = auth.get_validated_token(access_token)
                user = auth.get_user(validated_token)
                return user
            except:
                pass
                
        return user