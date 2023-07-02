# Generated by Django 4.2.2 on 2023-07-02 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smer', models.CharField(choices=[('er', 'Elektrotehnika i Racunarstvo'), ('si', 'Softversko inzenjerstvo'), ('ir', 'Racunarska tehnika i Informatika'), ('og', 'Energetika'), ('ot', 'Telekomunikacije i Informacione tehnologije'), ('oe', 'Elektronika i digitalni sistemi'), ('of', 'Fizicka elektrotnika')], max_length=250)),
                ('godina', models.SmallIntegerField(choices=[(1, 'Prva godina'), (2, 'Druga godina'), (3, 'Treca godina'), (4, 'Cetvrta godina')], default=1)),
                ('books', models.ManyToManyField(to='books.book')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GradedCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.SmallIntegerField(choices=[(1, 'One star'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars')], default=5)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.course')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
    ]