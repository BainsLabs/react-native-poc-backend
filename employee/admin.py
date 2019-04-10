from django.contrib import admin
from employee.models import EmployeeDetails


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(EmployeeDetails, EmployeeAdmin)
# Register your models here.
