from django.db import models
from django.urls import reverse


class Book(models.Model):
    isbn = models.BigIntegerField(primary_key=True)
    issued = models.DateTimeField(blank=True, null=True)
    authors = models.TextField(blank=True, null=True)  # This is a list of authors
    publishers = models.TextField(blank=True, null=True)  # This is a list of publishers. Usually there's just one.
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # HTML text to display
    average_rating = models.IntegerField(blank=True, null=True)
    popularity = models.BigIntegerField(blank=True, null=True)
    report_score = models.IntegerField(blank=True, null=True)
    cover_url = models.TextField(blank=True, null=True)  # Link where cover is stored
    topic = models.TextField(blank=True, null=True)  # This is a tag that distinguishes the book from other books

    def get_absolute_url(self):
        return reverse('books:book_detail', args=[self.isbn])

    class Meta:
        db_table = 'Books'
        ordering = ('-issued',)

    def __str__(self):
        return self.title


def get_courses_by_module(module, year):
    if module is None or year is None:
        return Course.objects.all()
    if module == 'er':
        return Course.objects.all().filter(er=True)
    elif module == 'si':
        return Course.objects.all().filter(simingod__lte=year)
    elif module == 'ir':
        return Course.objects.all().filter(irmingod__lte=year)
    elif module == 'os':
        return Course.objects.all().filter(osmingod__lte=year)
    elif module == 'ot':
        return Course.objects.all().filter(otmingod__lte=year)
    elif module == 'og':
        return Course.objects.all().filter(ogmingod__lte=year)
    elif module == 'of':
        return Course.objects.all().filter(ofmingod__lte=year)
    elif module == 'oe':
        return Course.objects.all().filter(oemingod__lte=year)
    else:
        return Course.objects.all()


class Course(models.Model):
    CHOICES = (
        ('o', 'Obavezan'),
        ('i', 'Izboran'),
    )
    id = models.IntegerField(primary_key=True)
    kurs = models.TextField(db_column='Kurs')  # Field name made lowercase.
    o_i = models.CharField(db_column='o/i', blank=True,
                           null=True, choices=CHOICES,
                           default='i')  # Field renamed to remove unsuitable characters.
    er = models.BooleanField(db_column='ER', blank=True, null=True)  # Field name made lowercase.
    simingod = models.IntegerField(db_column='SIMinGod', blank=True, null=True)  # Field name made lowercase.
    irmingod = models.IntegerField(db_column='IRMinGod', blank=True, null=True)  # Field name made lowercase.
    osmingod = models.IntegerField(db_column='OSMinGod', blank=True, null=True)  # Field name made lowercase.
    otmingod = models.IntegerField(db_column='OTMinGod', blank=True, null=True)  # Field name made lowercase.
    ogmingod = models.IntegerField(db_column='OGMinGod', blank=True, null=True)  # Field name made lowercase.
    ofmingod = models.IntegerField(db_column='OFMinGod', blank=True, null=True)  # Field name made lowercase.
    oemingod = models.IntegerField(db_column='OEMinGod', blank=True, null=True)  # Field name made lowercase.
    topics = models.TextField(db_column='Topics', blank=True,
                              null=True)  # Field name made lowercase. This is a list of tags that represent the course.

    def get_topics_dict(self):
        tags = {}
        for topic in self.topics:
            vals = topic.split(':')
            tags.update({vals[0]: vals[1]})
        return tags

    def get_absolute_url(self):
        return reverse('books:course_detail', args=[self.kurs])

    def __str__(self):
        return self.kurs

    class Meta:
        db_table = 'Courses'
