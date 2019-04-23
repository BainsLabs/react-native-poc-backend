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
            # images = os.listdir('')
            # make a list of all the available images

            images = skimage.io.imread(user.image_url)
            # cam = cv2.VideoCapture(0)   # 0 -> index of camera
            # s, img = cam.read()
            # if s:    # frame captured without any errors
            #     cv2.namedWindow("cam-test")
            #     cv2.imshow("cam-test", img)
            #     # cv2.waitKey(0)
            #     cv2.destroyWindow("cam-test")
            #     cv2.imwrite("filename.jpg", img)

            # load your image
            image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(request.data["img_base"])))

            # image = face_recognition.load_image_file("filename.jpg")

            # encoded the loaded image into a feature vector
            image_to_be_matched_encoded = face_recognition.face_encodings(image)[0]

            current_image = images
            # encode the loaded image into a feature vector
            current_image_encoded = face_recognition.face_encodings(current_image)[0]
        # match your image with the image and check if it matches
            # print("texst1")
            result = face_recognition.compare_faces(
                [image_to_be_matched_encoded], current_image_encoded)
        # check if it was a match
            # print("texst2", result)

            if result[0]:
                now = datetime.datetime.now()
                emp = EmployeeDetails.objects.get(official_email=user.official_email_id)
                usertimings = Employeetime.objects.filter(employee_email=emp.official_email,current_day=now.day)
                usertimings = usertimings.first()
                if not usertimings:
                    now = datetime.datetime.now()
                    EmployeeTimings = Employeetime(employee_id=emp.employee_id,employee_email=emp.official_email,employee_login_time=datetime.datetime.now(tz=timezone.utc),current_date=datetime.date.today(), current_day=now.day)
                    EmployeeTimings.save()
                    print(usertimings, "testing1")
                elif request.data['punch_type'] == 'punch-out' and usertimings.employee_login_time is not None and usertimings.employee_break_out_time is None:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break_out_time = []
                    reason = []
                    if usertimings.employee_break_out_time is None and usertimings.break_reason is None:
                        print(usertimings.employee_break_out_time, "testing")
                        break_in_timings.append(current_time)
                        reason.append(request.data['note'])
                    else:
                        previoustime = usertimings.employee_break_out_time.replace("[","").replace("]","")
                        previousreason = usertimings.reason_break.replace("[","").replace("]","")
                        print(usertimings.reason_break)
                        # mystring
                        break_out_time.extend((previoustime,current_time))
                        reason.append((previousreason,request.data['note']))
                    Employeetime.objects.filter(employee_email=emp.official_email).update(employee_break_out_time=break_out_time,break_reason=reason)
                    return Response(data={"status":200,"message":"Break out Time","break_out_time":break_out_time,"reason":reason})
                elif request.data['punch_type'] == 'punch-in' and usertimings.employee_login_time is not None and usertimings.employee_break_out_time is not None:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break_in_timings = []
                        # break_in_timings['timings'] = current_time
                    if usertimings.employee_break_in_time is None:
                        print(current_time, "testing")

                        break_in_timings.append(current_time)
                    else:

                        previoustime = usertimings.employee_break_in_time.replace("[","").replace("]","")
                        print(usertimings.employee_break_in_time )
                        # mystring
                        break_in_timings.extend((previoustime,current_time))

                    Employeetime.objects.filter(employee_email=emp.official_email).update(employee_break_in_time=break_in_timings)
                    return Response(data={"status":200,"message":"Break in Time","break_in_time":break_in_timings})
                return Response(data={"status": 200,"employee_profile":emp.to_json,"user":user.to_json,"login_time":usertimings.employee_login_time},status=status.HTTP_200_OK)
            # else:
            #     return Response(data={"status": 400,"message":"Not Matched"},status=status.HTTP_400_BAD_REQUEST)



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

@api_view(["POST"])
def employeeTimings(request):
    try:
        if request.data['is_superuser']:
          emplpoyeetime = Employeetime.objects.get(employee_email=request.data['email'])
          print(emplpoyeetime)
          return Response(data={"employee_time":emplpoyeetime.to_json}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"You are not Authorized for this view"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(e)
        return Response(data={"message":"No Employee Found"},status=status.HTTP_404_NOT_FOUND)