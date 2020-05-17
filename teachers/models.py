from django.db import models

# # Create your models here.
# class Klasy(models.Model):
#     id = models.CharField(db_column='ID', primary_key=True, max_length=10)  # Field name made lowercase.
#     nazwa = models.CharField(max_length=10)
#     opis = models.CharField(max_length=30, blank=True, null=True)
#     id_wychowawcy = models.ForeignKey('Nauczyciele', models.DO_NOTHING, db_column='ID_wychowawcy', blank=True, null=True)  # Field name made lowercase.
#     rocznik = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'klasy'


# class Nauczyciele(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     imie = models.CharField(max_length=40)
#     nazwisko = models.CharField(max_length=40)
#     pesel = models.BigIntegerField(db_column='PESEL')  # Field name made lowercase.
#     adres = models.CharField(max_length=30)
#     email = models.CharField(max_length=40)
#     numer_telefonu = models.CharField(max_length=13)

#     class Meta:
#         managed = False
#         db_table = 'nauczyciele'


# class Oceny(models.Model):
#     id_ucznia = models.ForeignKey('Uczniowie', models.DO_NOTHING, db_column='ID_ucznia')  # Field name made lowercase.
#     id_przedmiotu = models.ForeignKey('Przedmioty', models.DO_NOTHING, db_column='ID_przedmiotu')  # Field name made lowercase.
#     ocena = models.CharField(max_length=3)
#     waga = models.IntegerField()
#     wynik = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'oceny'


# class Ogloszenia(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     id_nauczyciela = models.ForeignKey(Nauczyciele, models.DO_NOTHING, db_column='ID_nauczyciela')  # Field name made lowercase.
#     id_przedmiotu = models.ForeignKey('Przedmioty', models.DO_NOTHING, db_column='ID_przedmiotu')  # Field name made lowercase.
#     tresc = models.CharField(max_length=1000)

#     class Meta:
#         managed = False
#         db_table = 'ogloszenia'


# class Przedmioty(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     nazwa = models.CharField(max_length=40)
#     id_nauczyciela = models.ForeignKey(Nauczyciele, models.DO_NOTHING, db_column='ID_nauczyciela', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'przedmioty'


# class Uczniowie(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     pesel = models.BigIntegerField(db_column='PESEL')  # Field name made lowercase.
#     imie = models.CharField(max_length=40)
#     nazwisko = models.CharField(max_length=40)
#     data_urodzenia = models.CharField(max_length=11)
#     adres = models.CharField(max_length=30)
#     email = models.CharField(max_length=40)
#     klasa = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'uczniowie'


# class Zajecia(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     id_przedmiotu = models.ForeignKey(Przedmioty, models.DO_NOTHING, db_column='ID_przedmiotu')  # Field name made lowercase.
#     id_klasy = models.ForeignKey(Klasy, models.DO_NOTHING, db_column='ID_klasy')  # Field name made lowercase.
#     czas = models.CharField(max_length=40, blank=True, null=True)
#     sala = models.CharField(max_length=5, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'zajecia'
