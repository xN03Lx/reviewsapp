from django.db import models
from django.contrib.auth import get_user_model


GENDERS = (
    ('male', 'MALE'),
    ('female', 'FEMALE'),
    ('other', 'OTHER'),
)

JOBS = (
    ('director', 'DIRECTOR'),
    ('producer', 'PRODUCER'),
    ('actor', 'ACTOR'),
    ('writer', 'WRITER')
)


class Celebrity(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(max_length=1000, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDERS, null=True, blank=True)
    url_image = models.URLField(null=True, blank=True)
    principal_job = models.CharField(max_length=20, choices=JOBS, null=True, blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


    def __str__(self):
        return self.name
