# my_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('investment/', include('investment.urls')),
    # Add other app URLs as needed
]
