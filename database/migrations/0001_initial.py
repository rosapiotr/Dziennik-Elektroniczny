# Generated by Django 2.2.12 on 2020-05-27 17:51

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False, verbose_name='Uczeń')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='Nauczyciel')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Klasa',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=10, primary_key=True, serialize=False)),
                ('nazwa', models.CharField(max_length=10)),
                ('opis', models.CharField(blank=True, max_length=30, null=True)),
                ('rocznik', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Klasy',
                'db_table': 'klasy',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Nauczyciel',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('imie', models.CharField(max_length=40)),
                ('nazwisko', models.CharField(max_length=40)),
                ('pesel', models.BigIntegerField(db_column='PESEL')),
                ('adres', models.CharField(max_length=30)),
                ('numer_telefonu', models.CharField(max_length=13)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Nauczyciele',
                'db_table': 'nauczyciele',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Przedmiot',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nazwa', models.CharField(max_length=40)),
                ('id_nauczyciela', models.ForeignKey(blank=True, db_column='ID_nauczyciela', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='database.Nauczyciel', verbose_name='Nauczyciel')),
            ],
            options={
                'verbose_name_plural': 'Przedmioty',
                'db_table': 'przedmioty',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Zajecia',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('dzien', models.CharField(blank=True, max_length=13, null=True)),
                ('godzina', models.TimeField(blank=True, null=True)),
                ('sala', models.CharField(blank=True, max_length=5, null=True)),
                ('id_klasy', models.ForeignKey(db_column='ID_klasy', on_delete=django.db.models.deletion.DO_NOTHING, to='database.Klasa', verbose_name='Klasa')),
                ('id_przedmiotu', models.ForeignKey(db_column='ID_przedmiotu', on_delete=django.db.models.deletion.DO_NOTHING, to='database.Przedmiot', verbose_name='Przedmiot')),
            ],
            options={
                'verbose_name_plural': 'Zajecia',
                'db_table': 'zajecia',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Uczen',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('pesel', models.BigIntegerField(db_column='PESEL')),
                ('imie', models.CharField(max_length=40)),
                ('nazwisko', models.CharField(max_length=40)),
                ('data_urodzenia', models.CharField(max_length=11)),
                ('adres', models.CharField(max_length=30)),
                ('klasa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='database.Klasa', verbose_name='Klasa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Uczniowie',
                'db_table': 'uczniowie',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ogloszenie',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('tresc', models.CharField(max_length=1000)),
                ('id_nauczyciela', models.ForeignKey(db_column='ID_nauczyciela', on_delete=django.db.models.deletion.DO_NOTHING, to='database.Nauczyciel')),
                ('id_przedmiotu', models.ForeignKey(db_column='ID_przedmiotu', on_delete=django.db.models.deletion.DO_NOTHING, to='database.Przedmiot')),
            ],
            options={
                'verbose_name_plural': 'Ogłoszenia',
                'db_table': 'ogloszenia',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ocena',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocena', models.CharField(max_length=3)),
                ('waga', models.IntegerField()),
                ('wynik', models.CharField(blank=True, max_length=100, null=True)),
                ('id_przedmiotu', models.ForeignKey(db_column='ID_przedmiotu', on_delete=django.db.models.deletion.DO_NOTHING, to='database.Przedmiot')),
                ('id_ucznia', models.ForeignKey(db_column='ID_ucznia', on_delete=django.db.models.deletion.DO_NOTHING, to='database.Uczen')),
            ],
            options={
                'verbose_name_plural': 'Oceny',
                'db_table': 'oceny',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='klasa',
            name='id_wychowawcy',
            field=models.ForeignKey(blank=True, db_column='ID_wychowawcy', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='database.Nauczyciel', verbose_name='Wychowawca'),
        ),
    ]
