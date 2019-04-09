from django.shortcuts import render
import os
import face_recognition
import cv2
import numpy as np
from PIL import Image

# Create your views here.


def index(request):

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
        print("Matched: " + images)
    else:
        print("Not matched: " + images)

    # iterate over each image
    # for image in images:
    #     # load the image
