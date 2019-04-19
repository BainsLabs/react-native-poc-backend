from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employee.models import EmployeeDetails
from facerecognition.models import User
from utils.imageUpload import imageUpload
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
import os

# Create your views here.


@api_view(["GET", "POST"])
def newEmployee(request):
    parser_classes = (MultiPartParser, FormParser)
    try:
        print(request.data)
        fs = FileSystemStorage()
        official_email = request.data['official_email']
        personal_email = request.data['personal_email']
        employee_id = request.data['employee_id']
        p_address = request.data['p_address']
        c_address = request.data['c_address']
        img = request.FILES['user_image']
        print(img)
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
        return Response(data={"message": "Employee created"},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(data={"message": "Not Save"},status=status.HTTP_400_BAD_REQUEST)

