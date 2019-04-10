from django.shortcuts import render
import os
import face_recognition
import cv2
import numpy as np
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from facerecognition.models import User

# Create your views here.


@api_view(["GET", "POST"])


def newuser(request):
    official_email = request.data['official_email']
    name = request.data['name']
    image_url = request.data['image_url']
    user = User(official_email=official_email, name=name,image_url=image_url)
    user.save()




def index(request):
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, 'facerecognition')
        # images = os.listdir('')
        # make a list of all the available images
        images = MEDIA_ROOT + "/karan.jpg"

        cam = cv2.VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()
        if s:    # frame captured without any errors
            cv2.namedWindow("cam-test")
            cv2.imshow("cam-test", img)
            # cv2.waitKey(0)
            cv2.destroyWindow("cam-test")
            cv2.imwrite("filename.jpg", img)

        # load your image
        image_to_be_matched = face_recognition.load_image_file("filename.jpg")

        # encoded the loaded image into a feature vector
        image_to_be_matched_encoded = face_recognition.face_encodings(
            image_to_be_matched)[0]

        current_image = face_recognition.load_image_file(images)
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
        return Response(data={"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
