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
from django.urls import path
from . import views
from .extra_logic import *
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.ReportList, name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('reports/', views.ReportList, name='report_list'),
    path('mapview/<int:survey_id>/', views.MapView, name='map_view'),
    path('map/', TemplateView.as_view(template_name='gas_survey.html')),
    path('reportview/<int:survey_id>/', views.ReportView, name='report_view'),
    path('createreport/', views.CreateReport, name='create_report'),
    path('editreport/<survey_id>/', views.EditReport, name='edit_report'),
    path('editreport/<survey_id>/addleak', views.AddLeak, name='add_leak'),
    path('editreport/<survey_id>/<leak_id>/', views.DeleteLeak, name='delete_leak'),
    path('repair/<survey_id>/<leak_id>/', mark_repaired, name='mark_repaired'),
    path('undorepair/<survey_id>/<leak_id>/', mark_not_repaired, name='undo_repaired'),
    path('password/', views.change_password, name='change_pw'),
    path('gasupload/', views.GasUpload, name='gasupload'),
    path('gaspointAPI/', views.GasPointAPI.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

