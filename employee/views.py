from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from employee.models import EmployeeDetails
from facerecognition.models import User
from utils.imageUpload import imageUpload
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
from employee.serializers import EmployeeSerializer
from employee.utility import NewEmployee
import os

# Create your views here.
class Registration(GenericAPIView):
    serializer_class = EmployeeSerializer

    def post(self,request):
        try:
            official_email = request.data['official_email']
            personal_email = request.data['personal_email']
            employee_id = request.data['employee_id']
            p_address = request.data['p_address']
            c_address = request.data['c_address']
            image_url = request.FILES['user_image']
            name = request.data['name']
        except KeyError as e:
            return Response(data={"status":406,"message":"parameter {e} missing".format(e=str(e))},status=status.HTTP_400_BAD_REQUEST)

        addemployee = NewEmployee(request.data)
        if addemployee.status:
            return Response(data={"status":200,"message":addemployee.message}, status=status.HTTP_200_OK)
        else:
            return Response(data={"status":200,"message":addemployee.message},status=status.HTTP_400_BAD_REQUEST)






