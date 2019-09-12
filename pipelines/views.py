from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import CustomUserCreationForm, SurveyDateForm
from .models import *


# Create your views here.


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


'''
class SurveyView(generic.FormView):
    form_class = SurveyDateForm
    template_name = 'report_view.html'
'''


def index(request):
    return render(request, 'index.html')


def PipelineView(request):
    try:
        client_id = request.user.client_id_fk
    except:
        client_id = 0
    pipe_list = Pipeline.objects.filter(client_id_fk=client_id)
    context = {'pipe_list': pipe_list}

    return render(request, 'pipelines.html', context)


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


def MapView(request):
    # This is where we pull information from the URL using a parameter get request.
    map_id = request.GET.get('q', '')

    if map_id != '':
        company_slug = map_id.split('_')[0]  # Company Name
        pipe_slug = map_id.split('_')[1]  # pipe name preserving spaces
        pipe_comp = pipe_slug.split()[0] + pipe_slug.split()[
            1]  # pipe name eliminating spaces to allow for pass through to JS
        date_slug = map_id.split('_')[2]  # date format in yyyy-mm-dd
    else:
        company_slug, pipe_slug, date_slug = '', '', ''

    print("the mapid is: ", map_id)

    context = {'company_slug': company_slug, 'pipe_slug': pipe_slug, 'date_slug': date_slug, 'survey_name': map_id,
               'pipe_comp': pipe_comp}

    return render(request, 'gas_survey.html', context)


class GetPipelineData(APIView):

    def get(self, request, format=None):
        pipeline_objects = Pipeline.objects.all()
        pipe_data = {}
        for object in pipeline_objects:
            header = {"type": "FeatureCollection", "name": object.pipe_name,
                      "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}},
                      "features": [{"type": "Feature", "properties": {"name": object.pipe_name},
                                    "geometry": {"type": "MultiLineString", "coordinates": [[point for point in object.pipe_geom]]}}]}

            pipe_data[object.pipe_name] = object.pipe_geom

        return Response(header)

def MapView(request):
    return render(request, 'map.html')