# Generated by Django 2.2.12 on 2020-05-17 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uczen',
            name='email',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_student',
            field=models.BooleanField(default=False, verbose_name='Uczeń'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='Nauczyciel'),
        ),
    ]