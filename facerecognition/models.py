from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    username = None
    name = models.CharField(max_length=100, null=False, blank=False)

    official_email = models. ForeignKey(
        'employee.EmployeeDetails', to_field='official_email', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=200, null=False, blank=False)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.official_email
