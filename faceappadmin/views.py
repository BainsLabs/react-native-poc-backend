
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from employee.models import EmployeeDetails
from facerecognition.models import User
from employeetimings.models import Employeetime
import json
from rest_framework.exceptions import APIException

# Create your views here.


@api_view(["POST"])
def employeeList(request):
    try:
        is_superuser = request.data['is_admin']
        employees = EmployeeDetails.objects.all().values("official_email","employee_id","p_address","c_address")
        employeeList = list(employees)
        # userdetails = []
        for employee in employees:
            # print(employee)
            user = User.objects.get(official_email_id=employee['official_email'])
            timings = Employeetime.objects.get(employee_email=employee['official_email'])
            username = user.name
            employee['name'] =username
            employee['timings'] = timings.to_json
        if is_superuser:
            # print("testing")
            return Response(data={"employeelist":employeeList},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(data={"message":"Error Occured"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def adminLogin(request):
    try:
        email = request.data["email"]
        password = request.data["password"]
        user_Data = User.objects.get(official_email_id=email, password=password)

        if user_Data:
            user = User.objects.get(official_email_id=email)
            hashed_email = make_password(user.official_email_id, salt=None)
            userObject = {
                "email": user.official_email_id,
                "isAdmin": user.is_superuser,
                "hash": hashed_email
            }

        return Response(data={"user":userObject,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={"message": "You are not registered with us! :(","status":status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
