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
from ast import literal_eval
from django.utils import timezone

# Create your views here.


@api_view(["POST"])
def index(request):
    try:
        users = User.objects.all()
        result = None
        for user in users:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MEDIA_ROOT = os.path.join(BASE_DIR, 'facerecognition')

            images = skimage.io.imread(user.image_url)

            image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(request.data["img_base"])))

            image_to_be_matched_encoded = face_recognition.face_encodings(image)[0]

            current_image = images
            current_image_encoded = face_recognition.face_encodings(current_image)[0]

            result = face_recognition.compare_faces(
                [image_to_be_matched_encoded], current_image_encoded)

            if result[0]:
                now = datetime.datetime.now()
                time = str(now.time())
                date = str(now.date())
                emp = EmployeeDetails.objects.get(official_email=user.official_email_id)
                usertimings = Employeetime.objects.filter(employee_email=emp.official_email,current_day=now.day)
                usertimings = usertimings.last()
                if not usertimings:
                    now = datetime.datetime.now()
                    EmployeeTimings = Employeetime(employee_id=emp.employee_id,employee_email=emp.official_email,employee_login_time=time,current_date=date, current_day=now.day)
                    EmployeeTimings.save()
                    return Response(data={"status": 200,"employee_profile":emp.to_json,"user":user.to_json,"login_time":time},status=status.HTTP_200_OK)

                elif request.data['punch_type'] == 'punch-out' and usertimings.employee_login_time and usertimings.employee_break_out_time == "":
                    breakouttime = str(datetime.datetime.now().time())
                    Employeetime.objects.filter(employee_email=emp.official_email).update(employee_break_out_time=time,break_reason=request.data['note'])
                    return Response(data={"status":200,"message":"Break out Time","break_out_time":time,"reason":request.data['note'],"employee_profile":emp.to_json,"user":user.to_json},status=status.HTTP_200_OK)
                elif request.data['punch_type'] == 'punch-in' and usertimings.employee_break_out_time !="" and usertimings.employee_break_in_time == "":
                    Employeetime.objects.filter(employee_email=emp.official_email).update(employee_break_in_time=time)
                    return Response(data={"status":200,"message":"Break out Time","break_in_time":time,"employee_profile":emp.to_json,"user":user.to_json},status=status.HTTP_200_OK)
                elif request.data['punch_type'] == 'punch-out' and usertimings.employee_login_time and usertimings.employee_break_out_time != "" and usertimings.employee_break_in_time != "":
                    print(usertimings.employee_login_time,"testt4")
                    EmployeeTimings = Employeetime(employee_id=emp.employee_id,employee_email=emp.official_email,employee_login_time=usertimings.employee_login_time,employee_break_out_time=time,current_date=date, current_day=now.day)
                    EmployeeTimings.save()
                    return Response(data={"status": 200,"employee_profile":emp.to_json,"user":user.to_json,"login_time":usertimings.employee_login_time,"break_out_time":time},status=status.HTTP_200_OK)
                else:
                    return Response(data={"message":"Nothing Found"},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(data={"message": "not found"}, status=status.HTTP_404_NOT_FOUND)

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

@api_view(["POST"])
def employeeTimings(request):
    try:
        if request.data['is_superuser']:
          emplpoyeetime = Employeetime.objects.filter(employee_email=request.data['email']).values("employee_email", "employee_login_time", "employee_logout_time","employee_break_in_time", "employee_break_out_time","break_reason","current_date")
          timings = list(emplpoyeetime)
          return Response(data={"employee_time":timings}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"You are not Authorized for this view"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response(data={"status":status.HTTP_404_NOT_FOUND,"message":"No timing Avalibale in Database for this User"},status=status.HTTP_404_NOT_FOUND)