from django.db import models

# Create your models here.


class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Iveskite knygos zanra')

    def __str__(self):
        return self.name

