from django.shortcuts import render
import os
import face_recognition
import cv2
import numpy as np
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import urllib.request
import io
import skimage
from rest_framework.parsers import JSONParser
from facerecognition.models import User
from employee.models import EmployeeDetails
from employeetimings.models import Employeetime
import datetime
import json
import base64

# Create your views here.


@api_view(["POST"])
def index(request):
    try:
        users = User.objects.all()
        for user in users:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MEDIA_ROOT = os.path.join(BASE_DIR, 'facerecognition')

            images = skimage.io.imread(user.image_url)

            image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(request.data["img_base"])))

            image_to_be_matched_encoded = face_recognition.face_encodings(image)[0]

            current_image = images
            current_image_encoded = face_recognition.face_encodings(current_image)[
                0]

            result = face_recognition.compare_faces(
                [image_to_be_matched_encoded], current_image_encoded)

            if result[0]:
                now = datetime.datetime.now()
                usertimings = Employeetime.objects.filter(employee_email=user.official_email_id,current_date=datetime.date.today())
                emplpoyee = EmployeeDetails.objects.get(official_email=user.official_email_id)
                if usertimings.employee_login_time == NULL:
                    now = datetime.datetime.now()
                    EmployeeTimings = Employeetime(employee_id=employee_id,employee_email=user.official_email_id,employee_login_time=datetime.time.now(),current_date=datetime.date.today(), current_day=now.day)
                    EmployeeTimings.save()
                elif request.data['punch_out']:
                    Employeetime.objects.filter(employee_id=user.official_email_id).update(employee_break_out_time=datetime.time.now(),break_reason=request.data['note'])
                else:
                    Employeetime.objects.filter(employee_id=user.official_email_id).update(employee_break_in_time=datetime.time.now())

                return Response(data={"status": 200,"employee_profile":emplpoyee.to_json,"user":user.to_json,"login_time":datetime.time.now()},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(data={"message": "not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def userExist(request):
    try:
        print(request.data['email'])
        user = User.objects.get(official_email_id=request.data['email'])

        if user:
            return Response(data={"status":200},status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={"status":404},status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def employeDetail(request):
    try:
        user= User.objects.get(official_email_id=request.data['email'])
        if user.is_superuser:
          emplpoyee = EmployeeDetails.objects.get(official_email=request.data['email'])
          return Response(data={"employee":emplpoyee.to_json,"user":user.to_json}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"You are not Authorized for this view"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(data={"message":"No Employee Found"},status=status.HTTP_404_NOT_FOUND)