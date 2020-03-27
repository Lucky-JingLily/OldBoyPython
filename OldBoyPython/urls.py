"""OldBoyPython URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login", views.login),
    path("home", views.home),

    path("template", views.template),

    re_path(r"^blog/", include("blog.urls")),
    # path("userinfo", views.user_info),
    # noname匹配
    # re_path('^articles/([0-9]{4})/$', views.year_archive),
    # re_path('^articles/([0-9]{4})/([0-9]{2})', views.year_mouth_archive),

    # name group (?P<name>pattern)
    # re_path("^articles/(?P<year>[0-9]{4})/(?P<mouth>[0-9]{2})", views.year_mouth_archive),

    # 命名变量
    # re_path("^articles/(?P<year>[0-9]{4})/(?P<mouth>[0-9]{2})", views.year_mouth_archive_variable,
    #         {"year": 2022, "mouth": 20}),

    # url别名
    # url(r'^func_alias', views.func_alias, name="alias"),

    path("ordered", views.ordered),
    path("shopping_car", views.shopping_car),

    path("students", views.Students.as_view()),
    path("teachers", views.Teachers.as_view()),

    path("orders", views.OrdersView.as_view()),

    path("api/v1/auth", views.AuthView.as_view()),
    path("api/v1/user", views.UserView.as_view()),
]
