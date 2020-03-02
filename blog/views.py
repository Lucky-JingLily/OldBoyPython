from django.db.models import Avg, Sum, Min, F, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from blog import models

# userList = []
from blog.models import Book


def user_info(req):
    if req.method == "POST":
        username = req.POST.get("username", None)
        sex = req.POST.get("sex", None)
        email = req.POST.get("email", None)

        user = {"username": username, "sex": sex, "email": email}
        print(user)

        models.UserInfo.objects.create(
            username=username,
            sex=sex,
            email=email,
        )

        # userList.append(user)
    user_list = models.UserInfo.objects.all()

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
