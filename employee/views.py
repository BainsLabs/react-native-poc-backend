from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employee.models import EmployeeDetails
from facerecognition.models import User
from utils.imageUpload import imageUpload
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.


@api_view(["GET", "POST"])
def newEmployee(request):
    try:
        fs = FileSystemStorage()
        official_email = request.data['official_email']
        personal_email = request.data['personal_email']
        employee_id = request.data['employee_id']
        p_address = request.data['p_address']
        c_address = request.data['c_address']
        img = request.FILES['user_image']
        imagename = fs.save(img.name,img)
        uploaded_image = fs.url(imagename)
        name = request.data['name']
        image_url = imageUpload(uploaded_image)
        if(image_url):
            fs.delete(uploaded_image)
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

@api_view(["GET"])
def allEmployeeList(request):
    try:
        is_superuser = request.GET['is_superuser',False]
        employees = EmployeeDetails.objects.all()
        if is_superuser:
            return Response(data={"employeeslist":employees.to_json},status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={"message":"Error Occured"},status=status.HTTP_400_BAD_REQUEST)