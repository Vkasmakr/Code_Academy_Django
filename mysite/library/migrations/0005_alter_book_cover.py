# Generated by Django 4.1.1 on 2023-01-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers', verbose_name='Virselis'),
        ),
    ]
