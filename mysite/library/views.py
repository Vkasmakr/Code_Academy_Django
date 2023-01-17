# Views - koduojame ka mes rodysime vartotojui (frontend)
from django.shortcuts import render, get_object_or_404
from django.views import generic  # suteikia jau is anksto paruostas Django klases
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre


def index(request):  # request - uzklausa atejusi is kliento
    # count uzklausos
    num_books = Book.objects.all().count()  # is models.py, Book klases
    num_authors = Author.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Filtruojame is kintamojo status 'g' reiksme
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    context = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors}
    return render(request, 'index.html', context=context)


# Sukuriame nauja langa, imame html apipavidalinima is authors.html
def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)  # pk - primary key
    return render(request, 'author.html', {'author': single_author})  # {'author':single_author] - context


class BookListView(generic.ListView):  # paveldejimas is generic.ListView klases
    model = Book  # book_list perduodamas i sablona, kuri Django suformuoja automatiskai
    template_name = 'book_list.html'
    # context_object_name = 'my_book_list' - pakeicia modelio listo pavadinima "book_list" i "my_book_list"
