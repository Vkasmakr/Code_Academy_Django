from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField  # ikelia redaktoriu ir priemones texto formatavimui. Very cool

# Create your models here.


class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Iveskite knygos zanra')

    def __str__(self):
        return self.name

    # Pakeicia suanglinima frameworke i musu pasirinktus isvedimus
    class Meta:
        verbose_name = "Zanras"
        verbose_name_plural = "Zanrai"


class Book(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    # susirisa autoriai su savo knygomis
    # related name - sukuria kintamojo rysi, kuri bus galima naudoti kitoje, suristoje klaseje
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='books')
    summary = models.TextField('Aprasymas', max_length=1000, help_text='Trumpas knygos aprasymas')
    isbn = models.CharField('ISBN', max_length=13)
    # Rysys daug su daug
    genre = models.ManyToManyField(Genre, help_text='Isrinkite zanra knygai')

    # Sukuriame papildoma lauka paveiksliuku patalpinimui
    cover = models.ImageField('Virselis', upload_to='covers', null=True, blank=True)
    # NOTE: jeigu ikeliant paveiksliuka admino lange meta errora, admin.py faile istrinti atitinkamus readonlyfields

    # Skirta ispakuoti genre elementus, kad galetume atvaizduoti
    def display_genre(self):
        return '; '.join([genre.name for genre in self.genre.all()])
    # .join nera butinas atvaizdavimui, taciau tai yra saugiau, kadangi isvedamas string, o ne listas

    # Pervadiname isvesti framerworke. Vietoje Display Genre, bus rodoma 'Zanras'
    display_genre.short_description = 'Zanras'

    def __str__(self):
        return f'{self.title}'

    # Gauname linka
    def absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    # Pakeicia suanglinima frameworke i musu pasirinktus isvedimus
    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus knygos kopijos ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)
    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Status'
    )

    # Sukuriame vartotojui sasaja. Vienas vartotojas gales skolintis daug knygu, todel kuriame ForeignKey
    # User importuotas is django bibliotekos django.contrib.auth.models
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # papildomas parametras, kuris tikrins ar knyga jau turejo buti grazinta

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False

    # nustatomas rykiavimas pagal (due back)
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} {self.book.title}'


class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavarde', max_length=100)
    # description = models.TextField('Aprasymas', max_length=2000, default='Biografija')

    description = HTMLField()

    # Skirta ispakuoti Author elementus, kad galetume atvaizduoti
    # Jungiasi su klaseje Book, kintamajame 'author' sukurtame "related_name='books'"
    def display_books(self):
        return ', '.join([book.title for book in self.books.all()[:3]])

    display_books.short_description = "Knygos"

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

    # sulinkinimas i konkrecia objekto eilute. Reversu suformuoja rysi su pavadinimu 'author-detail' ir argumentu
    # args=[str(self.id)]
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'



# pabaigus komanda terminale: python manage.py makemigrations
# python manage.py migrate