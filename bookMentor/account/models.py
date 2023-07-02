from django.db import models
from django.contrib.auth.models import User
from books.models import Book, Course


class Profile(models.Model):
    SMER_COICES = (
        ('er', 'Elektrotehnika i Racunarstvo'),
        ('si', 'Softversko inzenjerstvo'),
        ('ir', 'Racunarska tehnika i Informatika'),
        ('og', 'Energetika'),
        ('ot', 'Telekomunikacije i Informacione tehnologije'),
        ('oe', 'Elektronika i digitalni sistemi'),
        ('of', 'Fizicka elektrotnika')
    )

    PRVA_GODINA = 1
    DRUGA_GODINA = 2
    TRECA_GODINA = 3
    CETVRTA_GODINA = 4
    GODINA_CHOICES = (
        (PRVA_GODINA, 'Prva godina'),
        (DRUGA_GODINA, 'Druga godina'),
        (TRECA_GODINA, 'Treca godina'),
        (CETVRTA_GODINA, 'Cetvrta godina')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    smer = models.CharField(max_length=250, choices=SMER_COICES, blank=False, null=False)
    godina = models.SmallIntegerField(choices=GODINA_CHOICES, default=PRVA_GODINA)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return 'Profile for ' + self.user.first_name


class GradedCourse(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    GRADE_CHOICE = (
        (ONE, 'One star'),
        (TWO, 'Two stars'),
        (THREE, 'Three stars'),
        (FOUR, 'Four stars'),
        (FIVE, 'Five stars')
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    grade = models.SmallIntegerField(choices=GRADE_CHOICE, default=FIVE, blank=False, null=False)
