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
import json
import base64

# Create your views here.


@api_view(["POST"])
def index(request):
    try:
        user = User.objects.get(official_email_id=request.data['email'])

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
        current_image_encoded = face_recognition.face_encodings(current_image)[
            0]
    # match your image with the image and check if it matches
        # print("texst1")
        result = face_recognition.compare_faces(
            [image_to_be_matched_encoded], current_image_encoded)
    # check if it was a match
        # print("texst2", result)
        emplpoyee = EmployeeDetails.objects.get(official_email=request.data['email'])

        if result[0]:
            return Response(data={"status": 200,"employee_profile":emplpoyee.to_json,"user":user.to_json},status=status.HTTP_200_OK)
        else:
            return Response(data={"status": 400,"message":"Not Matched"},status=status.HTTP_400_BAD_REQUEST)



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
        if user.official_email_id:
            emplpoyee = EmployeeDetails.objects.get(official_email=request.data['email'])
            return Response(data={"employee":emplpoyee.to_json,"user":user.to_json}, status=status.HTTP_200_OK)
            print(user.official_email_id)
    except Exception as e:
        return Response(data={"message":"No Employee Found"},status=status.HTTP_404_NOT_FOUND)