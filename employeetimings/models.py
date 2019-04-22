from django.db import models

# Create your models here.

class Employeetime(models.Model):
    employee_id = models.CharField(max_length=200)
    employee_email = models.EmailField(unique=True, blank=False)
    employee_login_time = models.DateTimeField(auto_now=False)
    employee_logout_time = models.DateTimeField(auto_now=False)
    employee_break_in_time = models.CharField(max_length=255)
    employee_break_out_time = models.CharField(max_length=255)
    employee_extra_time = models.CharField(max_length=100)
    current_day = models.CharField(max_length=200)
    current_date = models.DateTimeField(auto_now=True)
    break_reason = models.CharField(max_length=200)

    @property
    def to_json():
      return {"employee_id":self.employee_id,"employee_email":self.employee_email,"employee_login_time":self.employee_login_time,"employee_logout_time":self.employee_logout_time,"employee_break_time":self.employee_break_time}
