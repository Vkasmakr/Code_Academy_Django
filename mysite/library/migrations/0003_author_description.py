# Generated by Django 4.1.1 on 2023-01-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_author_options_alter_book_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.TextField(default='Biografija', max_length=2000, verbose_name='Aprasymas'),
        ),
    ]
