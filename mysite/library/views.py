# Views - koduojame ka mes rodysime vartotojui (frontend)
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic  # suteikia jau is anksto paruostas Django klases
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm, UserBookCreateForm
from django.contrib.auth.decorators import login_required


def index(request):  # request - uzklausa atejusi is kliento. request taip pat saugo uzklausu informacija
    # count uzklausos
    num_books = Book.objects.all().count()  # is models.py, Book klases
    num_authors = Author.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Filtruojame is kintamojo status 'g' reiksme
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    # Skaiciuojam vartotojo apsilankymus (informacija saugoma Django duomenu bazeje db.sqlite3):
    num_visits = request.session.get('num_visits', 1)  # kai apsilankys pirma karta - bus 1
    request.session['num_visits'] = num_visits + 1  # kai apsilankys dar karta + 1

    context = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors,
               'num_visits': num_visits}
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


class BookDetailView(FormMixin, generic.DetailView):
    model = Book  # automatiskai sukuriamas kintamasis Book -> book
    template_name = 'book_detail_styled.html'  # nurodome is kur ims apipavidalinima internete
    form_class = BookReviewForm

    # nustatome settings
    class Meta:
        ordering = ['title']

    # Nukreipimas po sekmingo komentaro parasymo atgal i knygos langa
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)


def search(request):
    # 'query' (ne query as variable) gaus informacija is base.html input tage. t.y. getting input, kuris pavadintas taip
    query = request.GET.get('query')
    # search_results - nurodome kur paieskos resultatai bus priimti ir kur bus ieskoma
    search_results = Book.objects.filter(
                        Q(title__icontains=query) | # title - kuriama Books lauke ieskos, icontains panasu i .ilike(% %)
                        Q(summary__icontains=query)
    )
    return render(request, 'search.html', {"books": search_results, "query": query})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):  # Paveldime is dvieju klasiu!
    model = BookInstance  # gausime context={'bookinstance_list': BookInstance}
    template_name = 'user_books.html'

    # perrasome metoda get_queryset is klases generic.ListView. Child klases metodas veiks kreipiantis per Child klase
    # filter(reader=self.request.user) - isrenka useri
    # filter(status_exact='p') - isrenka BookInstance statusus su 'p' raktu
    # order_by('due_back') - surusiuoja pagal data
    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).filter(status__exact='p').order_by('due_back')


@csrf_protect
def register(request):
    if request.method == 'POST':  # sitas ivyks, kai bus ivykdyta "post" komanda su mygtukais is register.html -->
        # <form method="post">

        # pasiimame reiksmes is register.html lauku
        # ...Vartotojo vardas</label><input name="username"...
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():  # tikriname ar yra jau toks username
                messages.error(request, f'Vartotojo vardas {username} yra uzimtas')
                return redirect('register')  # grazinama i register puslapi
            else:
                if User.objects.filter(email=email).exists():  # tikriname ar yra jau toks email
                    messages.error(request, f'Emailas {email} yra uzimtas kito vartotojo')
                    return redirect('register')
                else:  # jeigu viskas gerai, kuriame nauja vartotoja
                    User.objects.create_user(username=username, email=email, password=password1)
                    messages.info(request, f'Vartotojas {username} sekmingai uzregistruotas')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptazodzia nesutampa')
            return redirect('register')

    return render(request, 'register.html')


# Profilio lango konfiguracija
@login_required
def profilis(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, "Profilis sekmingai atnaujintas")
            return redirect('profilis')
    else:  # kai bus request.method == "GET"
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profilis.html', context=context)


# Leis sukurti knygos vieneta
class BookByUserCreateView(LoginRequiredMixin, CreateView):
    model = BookInstance
    # fields = '__all__'  # rodo visus modelio laukus, bet jeigu nori isskirti ka rodysime, turime daryti kaip zemiau
    # fields = ('book', 'due_back', 'status')  - Prijungsime laukus is forms.py todel sitie nereikalingi
    success_url = '/library/mybooks/'  # kur nukreipsime po sekmingo posto
    template_name = 'user_book_form.html'
    form_class = UserBookCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)


class BookByUserDetailView(LoginRequiredMixin, BookDetailView):
    model = BookInstance
    template_name = 'user_book.html'


# LogisRequiredMixin - kas tik isilogines galetu daryt dalykus
# UserPassesTestMixin - kad isilogines useris negaletu keisti dalyku kitu useriu vardu
# Update View - kad useris galetu keisti dalykus
class BookByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BookInstance
    fields = ('book', 'due_back', 'status')
    success_url = '/library/mybooks/'  # kur nukreipsime po sekmingo keitimo
    template_name = 'user_book_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bookinstance = self.get_object()
        return self.request.user == bookinstance.reader  # testas ar prisijunges useris atitinka to instance, kuri
        # norime keisti "savininka". Cia, kad kitas useris nekeistu kito userio pakeitimu.


class BookByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookInstance
    success_url = '/library/mybooks/'
    template_name = 'user_book_delete.html'

    def test_func(self):
        bookinstance = self.get_object()
        return self.request.user == bookinstance.reader

