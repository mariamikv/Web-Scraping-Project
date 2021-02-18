
from django.contrib import admin
from django.urls import path, include
from Web import views

urlpatterns = [
    path('', include('Web.urls')),
    path('admin/', admin.site.urls),
]
