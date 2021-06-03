from django.db import models
from django.contrib.auth import get_user_model

from .models import Genre

class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class Filmable(models.Model):
    LANGUAGE_CHOICES = (
        ('spanish', 'SPANISH'),
        ('english' , 'ENGLISH'),
        ('german' , 'GERMAN'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.URLField()
    original_language = models.CharField(choices=LANGUAGE_CHOICES , max_length=10)
    trailer = models.URLField()
    genre = models.ManyToManyField(Genre)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


    class Meta:
        abstract = True


    def __str__(self):
        return self.title

