from rest_framework.throttling import SimpleRateThrottle

class VistorThrottling(SimpleRateThrottle):
    scope = "Vistor"

    def get_cache_key(self, request, view):
        # 唯一表示是IP
        return self.get_ident(request)

class UserThrottle(SimpleRateThrottle):
    scope = "User"
    def get_cache_key(self, request, view):
        # 唯一表示是用户名
        return request.user.username