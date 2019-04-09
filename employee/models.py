from django.db import models

# Create your models here.


class Employee(models.Model):
    official_email = models.ForeignKey(
        'facerecognition.User', to_field='official_email', on_delete=models.CASCADE)
    personal_email = models.EmailField(
        ('email address'), unique=True, blank=False)
    employee_id = models.CharField(max_length=100, null=False, blank=False)
    p_address = models.CharField(max_length=200, null=False, blank=False)
    c_address = models.CharField(max_length=200, null=False, blank=False)
    login_otp = models.CharField(max_length=100)
    exp_otp = models.CharField(max_length=100)

    def __str__(self):
        return self.official_email
