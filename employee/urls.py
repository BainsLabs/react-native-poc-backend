from django.urls import path
from employee.views import NewEmployee

urlpatterns = [
    path('employee', NewEmployee.as_view() , name="newemployee")
]
