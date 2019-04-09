from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employee.models import Employee

from .serializers import EmployeeSerializers

# Create your views here.


@api_view(["POST"])
def newEmployee(request):
    # try:
    #     data = dict()
    #     form = EmployeeForm(request.POST)
    #     if form.is_valid():
    #         employee = form.save()
    #         data['employee'] = model_to_dict(employee)
    #         return JsonResponse(data)
    #     else:
    #         data['error'] = "form not valid!"
    # except KeyError as e:
    #     return Response(data={"status": 406, "message": "parameter {e} missing".format(e=str(e))})
    print(request.data)
    # employee = request.data.get()

    # Create an article from the above data
    serializer = EmployeeSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        employee_save = serializer.save()
        return Response({"success": "Employee '{}' created successfully".format(employee_save)})
