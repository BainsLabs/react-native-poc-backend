from django.contrib import admin
from employeetimings.models import Employeetime
# Register your models here.


class EmployeeTime(admin.ModelAdmin):
    pass

admin.site.register(Employeetime, EmployeeTime)
