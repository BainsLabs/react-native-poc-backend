from rest_framework import serializers
from facerecognition.models import User


class UserSerializer(serializers.ModelSerializer):
  def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
  class Meta:
      model = User
      fields = ('id','name','official_email','image_url','is_superuser','password')
