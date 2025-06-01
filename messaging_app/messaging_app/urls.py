# messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messaging.urls')), # Include your app's URLs under 'api/'
    # Add other project-level URL patterns here
]