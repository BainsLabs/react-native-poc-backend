from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="face"),
    path('newuser',views.newuser, name="newuser")
]
