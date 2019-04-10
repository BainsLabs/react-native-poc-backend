
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employee.models import EmployeeDetails
from facerecognition.models  import User
import json
# Create your views here.

@api_view(["GET"])
def employeeList(request):
    try:
        employees = EmployeeDetails.objects.all()
        # employeeObject = {
        #         "official_email":employees.official_email,
        #         "Personal_email":employees.personal_email,
        #         "p_address":employees.p_address,
        #         "h_address":employees.h_address
        # }
        return Response(data=[employee.to_json for employee in employees],status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={"message":"No Data Found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def adminLogin(request):
    try:
        email = request.data["email"]
        password =request.data["password"]
        user_Data = User(official_email_id=email,password=password)

        if user_Data:
            user = User.objects.get(official_email_id=email)
            print(user.official_email_id)
        return Response(data={"message":user.to_json})
    except Exception as e:
        return Response(data={"message":"No user"})