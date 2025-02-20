from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Użytkownik musi posiadać adres email'))
        if not email:
            raise ValueError(_('Użytkownik musi posiadać login'))
        user = self.model(
            username = username,
            email=self.normalize_email(email),
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False, verbose_name="Uczeń")
    is_teacher = models.BooleanField(default=False, verbose_name="Nauczyciel")

    objects = CustomUserManager()

class Klasa(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=10)  # Field name made lowercase.
    nazwa = models.CharField(max_length=10)
    opis = models.CharField(max_length=30, blank=True, null=True)
    id_wychowawcy = models.ForeignKey('Nauczyciel', models.DO_NOTHING, db_column='ID_wychowawcy', blank=True, null=True, verbose_name="Wychowawca")  # Field name made lowercase.
    rocznik = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'klasy'
        verbose_name_plural = "Klasy"

    def __str__(self):
        return self.id


class Nauczyciel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    imie = models.CharField(max_length=40)
    nazwisko = models.CharField(max_length=40)
    pesel = models.BigIntegerField(db_column='PESEL')  # Field name made lowercase.
    adres = models.CharField(max_length=30)
    numer_telefonu = models.CharField(max_length=13)

    def __str__(self):
        return " ".join([self.imie, self.nazwisko])

    class Meta:
        managed = True
        db_table = 'nauczyciele'
        verbose_name_plural = "Nauczyciele"


class Ocena(models.Model):
    id_ucznia = models.ForeignKey('Uczen', models.DO_NOTHING, db_column='ID_ucznia')  # Field name made lowercase.
    id_przedmiotu = models.ForeignKey('Przedmiot', models.DO_NOTHING, db_column='ID_przedmiotu')  # Field name made lowercase.
    ocena = models.CharField(max_length=3)
    waga = models.IntegerField()
    wynik = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'oceny'
        verbose_name_plural = "Oceny"


class Ogloszenie(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_nauczyciela = models.ForeignKey(Nauczyciel, models.DO_NOTHING, db_column='ID_nauczyciela')  # Field name made lowercase.
    id_przedmiotu = models.ForeignKey('Przedmiot', models.DO_NOTHING, db_column='ID_przedmiotu')  # Field name made lowercase.
    tresc = models.CharField(max_length=1000)

    class Meta:
        managed = True
        db_table = 'ogloszenia'
        verbose_name_plural = "Ogłoszenia"
    
    def __str__(self):
        return " - ".join([str(self.id_przedmiotu), self.tresc])


class Przedmiot(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nazwa = models.CharField(max_length=40)
    id_nauczyciela = models.ForeignKey(Nauczyciel, models.DO_NOTHING, db_column='ID_nauczyciela', blank=True, null=True, verbose_name="Nauczyciel")  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'przedmioty'
        verbose_name_plural = "Przedmioty"

    def __str__(self):
        return " ".join([self.nazwa, "(" + str(self.id) + ")"])


class Uczen(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pesel = models.BigIntegerField(db_column='PESEL')  # Field name made lowercase.
    imie = models.CharField(max_length=40)
    nazwisko = models.CharField(max_length=40)
    data_urodzenia = models.CharField(max_length=11)
    adres = models.CharField(max_length=30)
    klasa = models.ForeignKey(Klasa, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Klasa")

    class Meta:
        managed = True
        db_table = 'uczniowie'
        verbose_name_plural = "Uczniowie"
    
    def __str__(self):
        if self.klasa:
            return " ".join([self.imie, self.nazwisko, self.klasa.nazwa])
        else:
            return " ".join([self.imie, self.nazwisko])


class Zajecia(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_przedmiotu = models.ForeignKey(Przedmiot, models.DO_NOTHING, db_column='ID_przedmiotu', verbose_name="Przedmiot")  # Field name made lowercase.
    id_klasy = models.ForeignKey(Klasa, models.DO_NOTHING, db_column='ID_klasy', verbose_name="Klasa")  # Field name made lowercase.
    dzien = models.CharField(max_length=13, blank=True, null=True)
    godzina = models.TimeField(blank=True, null=True)
    sala = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'zajecia'
        verbose_name_plural = "Zajecia"

    def __str__(self):
        return " | ".join([self.id_klasy.id, self.id_przedmiotu.nazwa, self.dzien, str(self.godzina)])
