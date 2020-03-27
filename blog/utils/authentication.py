from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from blog import models


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return ("lipeijing", None)

    def authenticate_header(self, request):
        pass


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get("token")
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise AuthenticationFailed("认证失败")
        return (token_obj.user, token_obj)
