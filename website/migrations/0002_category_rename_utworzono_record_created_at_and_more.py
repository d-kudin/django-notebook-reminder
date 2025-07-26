import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='record',
            old_name='utworzono',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='record',
            name='adres',
        ),
        migrations.RemoveField(
            model_name='record',
            name='email',
        ),
        migrations.RemoveField(
            model_name='record',
            name='imie',
        ),
        migrations.RemoveField(
            model_name='record',
            name='kod_pocztowy',
        ),
        migrations.RemoveField(
            model_name='record',
            name='miasto',
        ),
        migrations.RemoveField(
            model_name='record',
            name='nazwisko',
        ),
        migrations.RemoveField(
            model_name='record',
            name='nr_telefonu',
        ),
        migrations.RemoveField(
            model_name='record',
            name='wojewodztwo',
        ),
        migrations.AddField(
            model_name='record',
            name='content',
            field=models.TextField(default='Brak treści'),
        ),
        migrations.AddField(
            model_name='record',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='is_priority',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='record',
            name='reminder',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='status_color',
            field=models.CharField(choices=[('gray', 'Nieukończona'), ('green', 'Ukończona'), ('yellow', 'W toku'), ('red', 'Ważna')], default='gray', max_length=20),
        ),
        migrations.AddField(
            model_name='record',
            name='title',
            field=models.CharField(default='Nowa notatka', max_length=200),
        ),
        migrations.AddField(
            model_name='record',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='record',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.category'),
        ),
    ]
