from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('user/', include('facerecognition.urls')),
    path('admin/', admin.site.urls),
    path('employee/', include('employee.urls')),
]
