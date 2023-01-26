from django.urls import path, include
from . import views
from unicodedata import name

# Sukuriame marsrutus
urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),

    # <int:author_id> - nurodome, kad nukreipimas marsruto bus papildomas argumentas su integer kintamuoju author_id
    # name: author-detail - paimamas is models, klases Author, funkcijos  "get_absolute_url"
    # views.author - funkcija bus aprasyta views faile
    # cia ivedus authors/(skaicius) gausime nauja langa, kuris nuves i autoriu, kurio klases id - (skaicius)
    path('authors/<int:author_id>', views.author, name='author-detail'),

    # views.BookListView - sukurta papildoma klase views faile
    path('books/', views.BookListView.as_view(), name='books'),

    # views.BookDetailView
    # <int:pk> - sujungimas per primary key
    # book-detail - reverse is Book klases models.py faile
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

    # sukuriamas paieskos lauko marsutas. Funkcionalumas aprasomas bus views.py 'search' funkcijoje
    path('search/', views.search, name='search'),

    # Kuriame useriu prisijungima
    # djangocontrib.auth.urls - vienas is django jau paruostu marsrutu, leidzia prijungti urls is 'auth'
    path("accounts/", include("django.contrib.auth.urls")),

    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('mybooks/new', views.BookByUserCreateView.as_view(), name='my-borrowed-new'),
    path('mybooks/<uuid:pk>', views.BookByUserDetailView.as_view(), name='my-book'),
    path('mybooks/<uuid:pk>/update', views.BookByUserUpdateView.as_view(), name='my-book-update'),
    path('mybooks/<uuid:pk>/delete', views.BookByUserDeleteView.as_view(), name='my-book-delete')
]