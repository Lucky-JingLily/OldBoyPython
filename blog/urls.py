from django.conf.urls import url
from django.urls import path, re_path, include
from blog import views

urlpatterns = [
    path("userinfo", views.user_info),
    # noname匹配
    re_path('articles/([0-9]{4})/$', views.year_archive),
    # re_path('^articles/([0-9]{4})/([0-9]{2})', views.year_mouth_archive),

    # name group (?P<name>pattern)
    # re_path("^articles/(?P<year>[0-9]{4})/(?P<mouth>[0-9]{2})", views.year_mouth_archive),

    # 命名变量
    # re_path("^articles/(?P<year>[0-9]{4})/(?P<mouth>[0-9]{2})", views.year_mouth_archive_variable,
    #         {"year": 2022, "mouth": 20}),

    # url别名
    url(r'func_alias', views.func_alias, name="alias"),
]