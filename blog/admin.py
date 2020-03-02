from django.contrib import admin
from blog.models import *
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "publisher")
    search_fields = ("title",)
    list_filter = ("title",)
    ordering = ("-id", )

admin.site.register(Book, BookAdmin)
admin.site.register(Publish)
admin.site.register(Author)
