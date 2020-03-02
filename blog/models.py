from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=64)
    sex = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=64, verbose_name="书名")
    price = models.IntegerField(verbose_name="价格")
    color = models.CharField(max_length=64, verbose_name="颜色")
    page_num = models.IntegerField(null=True, verbose_name="页数")
    publisher = models.ForeignKey("Publish", on_delete=models.CASCADE, default=None, verbose_name="出版社")  # 一对多关系 foreignKey

    author = models.ManyToManyField("Author", verbose_name="作者")

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
