from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="face"),
    path('employeetime', views.employeeTimings, name="employeetime")
]
