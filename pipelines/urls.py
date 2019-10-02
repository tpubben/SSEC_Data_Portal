"""ssec_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from . import views
from django.views.generic.base import RedirectView, TemplateView
from djgeojson.views import GeoJSONLayerView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('reports/', views.ReportList, name='report_list'),
    path('mapview/<int:survey_id>/', views.MapView, name='map_view'),
    path('map/', TemplateView.as_view(template_name='map.html')),
    path('reportview/<int:survey_id>/', views.ReportView, name='report_view'),
    path('createreport/', views.CreateReport, name='create_report'),

]

