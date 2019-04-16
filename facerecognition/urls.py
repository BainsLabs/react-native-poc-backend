from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="face"),
    path('usercheck', views.userExist,name="usercheck"),
    path('employeedetail', views.employeDetail, name="employeedetails")
]
