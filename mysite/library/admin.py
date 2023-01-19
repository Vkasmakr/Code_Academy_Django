from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


# Sukuriamas naujas BookInstance klases laukas, kuri bus galima inkorporuoti i kitos klases isvedama vaizda
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # ivedimo eilutes, nurodome, kad nekurtu papildomu
    # readonly_fields = ('id',)  # nurodome, kad ID laukas bus tik matomas, bet nekeiciamas
    # can_delete = False  # isimamas istrynimo laukas


# Nurodome papildomai kaip bus rodomi objektai is Book klases
class BookAdmin(admin.ModelAdmin):  # paveldi is ModelAdmin
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]  # prijungiamas BookInstance klases laukas sukurtas auksciau
# display_genre - funkcija klaseje Books, kadangi tai yra rysys ManyToMany


# Nurodome papildomai kaip bus rodomi objektai is Author klases
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name','display_books',)
# display_books - funkcija klaseje Author, kadangi tai yra rysys ManyToMany


# Sukuriame vaizdavimo elementus BookInstance klasei
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')  # kokius laukus norime matyti
    list_filter = ('status', 'due_back')  # sukuriamas filtras
    # ikeliamas paiesko laukas
    search_fields = ('id', 'book__title')  # book - tevine klase, __- nurodo, kad nukreipiame, title - nukreipiam i titl
    # Ikeliami laukeliai redagavimui tiesiai is pagrindinio lango
    list_editable = ('due_back', 'status')
    fieldsets = (
        ('General', {'fields': ('id', 'book')}),  # BookInstance klaseje bus sukurtas laukas su id, book ivestimis
        ('Availability', {'fields': ('status', 'due_back')})  # laukas su status, due_back ivestimis
    )


# Register your models here.
admin.site.register(Author, AuthorAdmin)  # surisame Author ir AuthorAdmin
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)  # surisame Book ir BookAdmin
admin.site.register(BookInstance, BookInstanceAdmin)  # surisame BookInstance ir BookInstanceAdmin
# po registracijas: python manage.py createsuperuser

