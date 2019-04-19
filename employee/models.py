from django.db import models

# Create your models here.


class EmployeeDetails(models.Model):
    official_email = models.EmailField(
        ('email address'), unique=True, blank=False)
    personal_email = models.EmailField(
        ('email address'), unique=True, blank=True)
    employee_id = models.CharField(max_length=100, null=False, blank=False)
    p_address = models.CharField(max_length=200, null=False, blank=False)
    c_address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.official_email

    @property
    def to_json(self):
        return {"official_email": self.official_email, "employee_id": self.employee_id, "p_address": self.p_address, "c_address": self.c_address}
