# Generated by Django 2.2.12 on 2020-05-17 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20200517_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klasa',
            name='id_wychowawcy',
            field=models.ForeignKey(blank=True, db_column='ID_wychowawcy', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='database.Nauczyciel', verbose_name='Wychowawca'),
        ),
        migrations.AlterField(
            model_name='przedmiot',
            name='id',
            field=models.AutoField(db_column='ID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='przedmiot',
            name='id_nauczyciela',
            field=models.ForeignKey(blank=True, db_column='ID_nauczyciela', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='database.Nauczyciel', verbose_name='Nauczyciel'),
        ),
        migrations.AlterField(
            model_name='uczen',
            name='klasa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.Klasa'),
        ),
    ]