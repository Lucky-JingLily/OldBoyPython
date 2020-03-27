import json

from django.db.models import Avg, Sum, Min, F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from blog.utils.authentication import UserAuthentication, MyAuthentication, BaseAuthentication
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning
from rest_framework.permissions import BasePermission
from rest_framework.parsers import JSONParser, FormParser

# Create your views here.
from django.urls import reverse
from rest_framework.views import APIView

from blog import models

# userList = []
from blog.models import Book
from blog.utils.permissions import LoginPermission
from blog.utils.throttling import UserThrottle, VistorThrottling
from blog.utils.version import ParamVersion
from blog.utils.serializers import UserInfoSerializer


def user_info(req):
    if req.method == "POST":
        username = req.POST.get("username", None)
        sex = req.POST.get("sex", None)
        email = req.POST.get("email", None)

        user = {"username": username, "sex": sex, "email": email}

        models.User.objects.create(
            username=username,
            sex=sex,
            email=email,
        )

        # userList.append(user)
    user_list = models.User.objects.all()

    # return render(req, "index.html", {"useList": user_list})
    # 需要本地变量的名字与待渲染的html页面{% 变量 %}变量名一致
    # "index.html"为模板文件，locals()表示context上下文
    return render(req, "index.html", locals())


def year_archive(req, year):
    return HttpResponse(year)


def year_mouth_archive(request, year, mouth):
    result = "{year}:{mouth}".format(year=year, mouth=mouth)
    return HttpResponse(result)


def year_mouth_archive_variable(request, year, mouth):
    result = "{year}:{mouth}".format(year=year, mouth=mouth)
    return HttpResponse(result)


def func_alias(req):
    # if req.method == "POST":
    #     username = req.POST.get("username")
    #     password = req.POST.get("password")
    #
    #     if username == "lipeijing" and password == "123":
    #         return HttpResponse("Login Success")
    # return render(req, "login.html")
    return reverse('alias')


def login(req):
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        if username == "lipeijing" and password == "123":
            return redirect("/home")
    return render(req, "login.html")


def home(req):
    return render(req, "home.html", {"username": "lipeijing"})


def template(req):
    tempDir = {"username": "alex"}
    tempList = [1, 2, 3]
    tempStr = "<a href=\"www.baidu.com\">baidu</a>"
    return render(req, "template.html", {"num": 5})


def ordered(request):
    return render(request, "ordered.html")


def shopping_car(request):
    return render(request, "shopping_car.html")


def data_ops(req):
    # 多对多 正向查询
    book = models.Book.objects.filter(id=1)[0]
    print(book.publisher.city)
    authors = models.Author.objects.filter(id__gt=2)  # id大于2
    # book.author.add(*authors)
    book.author.remove(*authors)
    # 方向查询
    author = models.Author.objects.filter(id=2)[0]
    books = models.Book.objects.filter(id__gt=2)
    author.book_set.add(books)

    publisher = models.Publish.objects.filter(name="lipeijing")[0]
    publisher.book_set.all().values("title").distinct()

    # 聚合查询
    models.Book.objects.all().aggregate(Avg("price"))
    # 分组查询
    models.Book.objects.values("authors__name").annotate(Sum("price"))
    models.Book.objects.values("publisher__name").annotate(Min("price"))

    models.Book.objects.filter(id=1).delete()

    models.Book.objects.filter(id=2).update(name="hello world")

    # F 查询，只能针对数
    models.Book.objects.all().update(price=F("price") + 20)[0]

    # Q 查询
    models.Book.objects.filter(Q(id=3) | Q(title="GO"))

    return HttpResponse("OK")


@method_decorator(csrf_exempt, "dispatch")
class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        print("before")
        return super(BaseView, self).dispatch(request, *args, **kwargs)


class Students(BaseView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("GET")

    def post(self, request, *args, **kwargs):
        return HttpResponse("POST")

    def put(self, request, *args, **kwargs):
        return HttpResponse("PUT")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("DELETE")


class Teachers(BaseView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("GET")

    def post(self, request, *args, **kwargs):
        return HttpResponse("POST")

    def put(self, request, *args, **kwargs):
        return HttpResponse("PUT")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("DELETE")


class OrdersView(APIView):
    authentication_classes = [MyAuthentication, ]

    def get(self, request, *args, **kwargs):
        self.dispatch
        return HttpResponse("GET")

    def post(self, request, *args, **kwargs):
        return HttpResponse("POST")

    def put(self, request, *args, **kwargs):
        return HttpResponse("PUT")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("DELETE")


def md5(user):
    import hashlib
    import time
    ctime = str(time.ctime())
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()


class AuthView(APIView):
    permission_classes = [LoginPermission, ]

    def post(self, request, *args, **kwargs):
        ret = {"code": 1000, "msg": None}
        try:
            user = request._request.POST.get("username")
            passwd = request._request.POST.get("password")

            obj = models.UserInfo.objects.filter(username=user, password=passwd).first()
            if not obj:
                ret["code"] = 1001
                ret["msg"] = "用户名密码错误"
            token = md5(user)
            models.UserToken.objects.update_or_create(user=obj, defaults={"token": token})
            ret["token"] = token
            ret["msg"] = "login success."
        except Exception as e:
            print(e)
        return JsonResponse(ret)


class UserView(APIView):
    authentication_classes = [UserAuthentication, ]
    throttle_classes = [UserThrottle, ]
    # versioning_class = ParamVersion
    # versioning_class = QueryParameterVersioning
    versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        # self.dispatch()
        print(request.version)
        ret = {"code": 1000, "msg": None}
        return JsonResponse({"code": 1000, "msg": request.user.username})

class UserInfoView(APIView):
    authentication_classes = [MyAuthentication, ]
    # throttle_classes = [UserThrottle, ]
    throttle_classes = []
    # versioning_class = ParamVersion
    # versioning_class = QueryParameterVersioning
    versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        # self.dispatch()

        users = models.UserInfo.objects.all()
        # ser = UserInfoSerializer(instance=users, many=True)
        ser = UserInfoSerializer(instance=users, many=True, context={'request': request})

        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

class GroupView(APIView):
    authentication_classes = [MyAuthentication, ]
    # throttle_classes = [UserThrottle, ]
    throttle_classes = []
    # versioning_class = ParamVersion
    # versioning_class = QueryParameterVersioning
    versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        # self.dispatch()

        group = models.UserGroup.objects.all()
        # ser = UserInfoSerializer(instance=users, many=True)
        ser = UserInfoSerializer(instance=group, many=False)

        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class ParserView(APIView):
    permission_classes = [LoginPermission, ]

    def post(self, request, *args, **kwargs):
        print(request.data)
        return HttpResponse("JSON测试")
