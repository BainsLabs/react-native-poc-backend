from rest_framework import serializers
from employee.models import Employee


class EmployeeSerializers(serializers.Serializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
