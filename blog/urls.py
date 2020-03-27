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
    path("users", views.UserView.as_view()),

    re_path(r'^(?P<version>[v1|v2]+)/users/$', views.UserView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/parserview/$', views.ParserView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/userinfos/$', views.UserInfoView.as_view()),
    re_path('^(?P<version>[v1|v2]+)/usergroup/(?P<group>\d+)', views.UserInfoView.as_view(),name='gp'),
    re_path('^(?P<version>[v1|v2]+)/usergroup/(\d+)', views.GroupView.as_view()),

]
