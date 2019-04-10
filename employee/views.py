from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employee.models import Employee

from .serializers import EmployeeSerializers

# Create your views here.


@api_view(["POST"])
def newEmployee(request):
    official_email = request.data['official_email_id']
    personal_email = request.data['personal_email']
    employee_id = request.data['employee_id']
    p_address = request.data['p_address']
    c_address = request.data['c_address']
    employee = Employee(official_email_id=official_email, personal_email=personal_email,
                        employee_id=employee_id, p_address=p_address, c_address=c_address)
    employee.save()

