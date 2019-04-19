from django.urls import path
from . import views

urlpatterns = [
    path('new_employee', views.newEmployee, name="newemployee")
]
