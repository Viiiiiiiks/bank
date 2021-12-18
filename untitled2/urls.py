"""untitled2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from bank import views
from bank.views import profile_upload
from django.conf import settings
from django.conf.urls.static import static


app_name = 'app_first_test'
"""
Цель: регистрация всех функций, запускающихся при вводе пользователя
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bank.urls')),
    path('upload-csv/', profile_upload, name="profile_upload"),
    url(r'^choises/', views.choises, name='choises'),
    url(r'^input_bank/', views.input_bank, name='input_bank'),
    url(r'^input_date/', views.input_date, name='input_date'),
    url(r'^graphic/', views.graphic, name='graphic'),
    url(r'^new_report/', views.new_report, name='new_report'),
    url(r'^my_image/', views.my_image, name='my_image'),
    url(r'^parser/', views.parser, name='parser'),
    url(r'^new_database/', views.new_database, name='new_database'),
    url(r'^list_of_banks/', views.list_of_banks, name='list_of_banks'),
]
