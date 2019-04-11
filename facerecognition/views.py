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
from skimage import io
from rest_framework.parsers import JSONParser
from facerecognition.models import User
import json
import io
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

        images = io.imread(user.image_url)
        cam = cv2.VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()
        if s:    # frame captured without any errors
            cv2.namedWindow("cam-test")
            cv2.imshow("cam-test", img)
            # cv2.waitKey(0)
            cv2.destroyWindow("cam-test")
            cv2.imwrite("filename.jpg", img)

        # load your image
        image = face_recognition.load_image_file(
            io.BytesIO(base64.b64decode(request.data["img_base"])))

        # image_to_be_matched = face_recognition.load_image_file("filename.jpg")

        # encoded the loaded image into a feature vector
        image_to_be_matched_encoded = face_recognition.face_encodings(image)

        current_image = images
        # encode the loaded image into a feature vector
        current_image_encoded = face_recognition.face_encodings(current_image)[
            0]
    # match your image with the image and check if it matches
        result = face_recognition.compare_faces(
            [image_to_be_matched_encoded], current_image_encoded)
    # check if it was a match
        if result[0] == True:
            return Response(data={"status": 200})
        else:
            return Response(data={"status": 400})

    except Exception as e:
        print(e)
        return Response(data={"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
