# Generated by Django 4.1.1 on 2023-01-16 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Autorius', 'verbose_name_plural': 'Autoriai'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Knyga', 'verbose_name_plural': 'Knygos'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Zanras', 'verbose_name_plural': 'Zanrai'},
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='library.author'),
        ),
    ]