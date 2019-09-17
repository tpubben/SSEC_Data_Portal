from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry

from .forms import CustomUserCreationForm, SurveyDateForm
from .models import *


# Create your views here.


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def index(request):
    return render(request, 'index.html')


def ReportView(request):
    # form = SurveyDateForm(request)
    try:
        client_id = request.user.client_id_fk
    except:
        client_id = 0
    report_list = SurveyDate.objects.filter(client_id_fk=client_id)
    context = {'report_list': report_list}
    # form.fields['pipe_id_fk'].queryset = SurveyDate.objects.filter(client_id_fk=client_id)

    return render(request, 'report_view.html', context)


def MapView(request, survey_id):

    # This is where we pull information from the URL using a parameter get request.
    survey = SurveyDate.objects.get(pk=survey_id)
    print(survey.pipe_id_fk.id)
    points = SurveyPoint.objects.all()
    geoms = []

    for point in points:
        GasReading = point.gas_value
        xcoord = point.gas_geom.coords[0]
        ycoord = point.gas_geom.coords[1]
        geoms.append((GasReading, xcoord, ycoord))

    if survey.geometry_type == "PIPELINE":
        pipeline = Pipeline.objects.get(pk=survey.pipe_id_fk.id)
        name = pipeline.pipe_name
        allcoords = [[coord[0], coord[1]] for coord in pipeline.pipe_geom.coords]
        context = {'points': geoms, 'name': name, 'linecoords': allcoords, 'infcoords': []}









    return render(request, 'gas_survey.html', context)



