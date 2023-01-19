# Views - koduojame ka mes rodysime vartotojui (frontend)
from django.shortcuts import render, get_object_or_404
from django.views import generic  # suteikia jau is anksto paruostas Django klases
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from django.core.paginator import Paginator
from django.db.models import Q


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
    # authors = Author.objects.all()  Sitas jau nebereikalingas jeigu naudojam Paginator klase, kadangi ji pati pasiima

    # Naudojame Paginator klase, kad supuslapiuoti puslapi
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)

    context = {
        'authors': paged_authors  # anksciau buvo 'authors' bet dabar naudojame Paginator, todel ir jo reiksme idedame
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)  # pk - primary key
    return render(request, 'author.html', {'author': single_author})  # {'author':single_author] - context


class BookListView(generic.ListView):  # paveldejimas is generic.ListView klases
    model = Book  # book_list perduodamas i sablona, kuri Django suformuoja automatiskai

    # paginate_by - puslapiavimas (t.y. idedam funkcija tampe paciame puslapyje tureti keleta puslapiu)
    paginate_by = 2

    template_name = 'book_list.html'
    # context_object_name = 'my_book_list' - pakeicia modelio listo pavadinima is "book_list" i "my_book_list"


class BookDetailView(generic.DetailView):
    model = Book  # automatiskai sukuriamas kintamasis Book -> book
    template_name = 'book_detail_styled.html'  # nurodome is kur ims apipavidalinima internete


def search(request):
    # 'query' (ne query as variable) gaus informacija is base.html input tage. t.y. getting input, kuris pavadintas taip
    query = request.GET.get('query')
    # search_results - nurodome kur paieskos resultatai bus priimti ir kur bus ieskoma
    search_results = Book.objects.filter(
                        Q(title__icontains=query)  # title - kuriama Books lauke ieskos, icontains panasu i .ilike(% %)
    )
    return render(request, 'search.html', {"books": search_results, "query": query})
