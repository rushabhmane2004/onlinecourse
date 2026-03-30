from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # <--- Change 'register' to 'urls'
    path('onlinecourse/', include('onlinecourse.urls')),
]