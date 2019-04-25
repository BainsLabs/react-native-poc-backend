from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    username = None
    name = models.CharField(max_length=100, null=False, blank=False)

    official_email = models.ForeignKey(
        'employee.EmployeeDetails', to_field='official_email', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=200, null=False, blank=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.official_email

    @property
    def to_json(self):
        return {"id":self.id,"official_email_id": self.official_email_id, "image_url": self.image_url, "name": self.name}
    def save(self, *args, **kwargs):
        if self.official_email_id:
            self.official_email_id = self.official_email_id.strip().lower()
        super(User, self).save(*args, **kwargs)