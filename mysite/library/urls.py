from django.urls import path, include
from . import views

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
    path('books/', views.BookListView.as_view(), name='books')
]