#\website\migrations\0001_initial.py

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utworzono', models.DateTimeField(auto_now_add=True)),
                ('imie', models.CharField(max_length=50)),
                ('nazwisko', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('nr_telefonu', models.CharField(max_length=15)),
                ('adres', models.CharField(max_length=100)),
                ('miasto', models.CharField(max_length=50)),
                ('wojewodztwo', models.CharField(max_length=50)),
                ('kod_pocztowy', models.CharField(max_length=20)),
            ],
        ),
    ]
