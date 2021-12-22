"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from covid_tracker.views import RegisterUserView, RegisterAdminUserView, SelfAssessmentView, UpdateCovidResultView, \
    GetZoneInfoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register-user/', RegisterUserView.as_view(), name='register-user'),
    path('register-admin/', RegisterAdminUserView.as_view(), name='register-admin'),
    path('self-assessment/', SelfAssessmentView.as_view(), name='self-assessment'),
    path('update-covid-status/', UpdateCovidResultView.as_view(), name='update-covid-status'),
    path('get-zone-info/', GetZoneInfoView.as_view(), name='get-zone-info'),
]
