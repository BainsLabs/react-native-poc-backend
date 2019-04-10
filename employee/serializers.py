from rest_framework import serializers
from employee.models import Employee


class EmployeeSerializers(serializers.Serializer):
    class Meta:
        model = Employee
        fields = (
            "official_email_id"
            "personal_email"
            "employee_id"
            "p_address"
            "c_address"
        )

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
