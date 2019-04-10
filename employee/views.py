from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employee.models import EmployeeDetails
from facerecognition.models import User

# Create your views here.


@api_view(["GET", "POST"])
def newEmployee(request):
    try:
        official_email = request.data['official_email']
        personal_email = request.data['personal_email']
        employee_id = request.data['employee_id']
        p_address = request.data['p_address']
        c_address = request.data['c_address']
        name = request.data['name']
        image_url = request.data['image_url']
        employee = EmployeeDetails(official_email=official_email, personal_email=personal_email,
                                   employee_id=employee_id, p_address=p_address, c_address=c_address)
        user = User(official_email_id=official_email,
                    name=name, image_url=image_url)

        employee.save()
        user.save()

        return Response(status=status.HTTP_200_OK, data={"message": "employee created"})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": e})
