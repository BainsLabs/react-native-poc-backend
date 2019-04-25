from rest_framework import serializers
from employee.models import EmployeeDetails


class EmployeeSerializer(serializers.ModelSerializer):
  def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
  class Meta:
      model = EmployeeDetails
      fields = ('id','official_email','personal_email','employee_id','p_address','c_address')
