from django.urls import path
from . import views

urlpatterns = [
    path('allemployee', views.employeeList, name="employeelist"),
]
