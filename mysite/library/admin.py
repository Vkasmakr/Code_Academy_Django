from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


# Nurodome papildomai kaip bus rodomi objektai is Book klases
class BookAdmin(admin.ModelAdmin):  # paveldi is ModelAdmin
    list_display = ('title', 'author', 'display_genre')
# display_genre - funkcija klaseje Books, kadangi tai yra rysys ManyToMany


# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)  # surisame Book ir BookAdmin
admin.site.register(BookInstance)
# po registracijas: python manage.py createsuperuser

