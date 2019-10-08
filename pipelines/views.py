from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry

from .forms import *
from .models import *
from .extra_logic import *


# Create your views here.


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def index(request):
    return render(request, 'index.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def ReportList(request):
    # form = SurveyDateForm(request)
    user = request.user
    try:
        client_id = request.user.client_id_fk
    except:
        client_id = 0
    report_list = []
    if user.is_superuser == True:
        reports = SurveyDate.objects.all()
    else:
        reports = SurveyDate.objects.filter(client_id_fk=client_id)
    for report in reports:
        if report.geometry_type == "PIPELINE":
            site_name = report.pipe_id_fk
        elif report.geometry_type == "SITE":
            site_name = report.inf_id_fk
        else:
            site_name = 'NA'
        report_list.append(
            {"name": site_name, "date": report.survey_date, "id": report.id, "company": report.client_id_fk})

    context = {'report_list': report_list}
    # form.fields['pipe_id_fk'].queryset = SurveyDate.objects.filter(client_id_fk=client_id)

    return render(request, 'report-list.html', context)


def MapView(request, survey_id):
    # This is where we pull information from the URL using a parameter get request.
    survey = SurveyDate.objects.get(pk=survey_id)
    print(survey.pipe_id_fk.id)
    points = SurveyPoint.objects.all()
    geoms = []

    for point in points:
        GasReading = point.gas_value
        print(GasReading)
        xcoord = point.gas_geom.coords[0]
        ycoord = point.gas_geom.coords[1]
        geoms.append((GasReading, xcoord, ycoord))

    if survey.geometry_type == "PIPELINE":
        pipeline = Pipeline.objects.get(pk=survey.pipe_id_fk.id)
        name = pipeline.pipe_name
        allcoords = [[coord[0], coord[1]] for coord in pipeline.pipe_geom.coords]
        context = {'points': geoms, 'name': name, 'linecoords': allcoords, 'infcoords': []}
    elif survey.geometry_type == "SITE":
        site = Infrastructure.objects.get(pk=survey.inf_id_fk_id)
        sitename = Infrastructure.inf_name
        infcoords = [[coord[0], coord[1]] for coord in site.inf_geom.coords]
        context = {'points': geoms, 'name': sitename, 'linecoords': [], 'infcoords': infcoords}
    else:
        pass

    return render(request, 'gas_survey.html', context)


def ReportView(request, survey_id):
    survey = SurveyDate.objects.get(pk=survey_id)
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    if user.client_id_fk == survey.client_id_fk or user.is_superuser == True:
        context = {}
        deficiencies = survey.surveydef.all()
        context['defs'] = deficiencies
        context['survey'] = survey
        points = SurveyPoint.objects.all()
        geoms = []

        for point in points:
            GasReading = point.gas_value
            xcoord = point.gas_geom.coords[0]
            ycoord = point.gas_geom.coords[1]
            geoms.append((GasReading, xcoord, ycoord))

        if survey.geometry_type == "PIPELINE":
            pipeline = Pipeline.objects.get(pk=survey.pipe_id_fk.id)
            name = survey.pipe_id_fk.pipe_name
            allcoords = [[coord[0], coord[1]] for coord in pipeline.pipe_geom.coords]
            context['points'] = geoms
            context['name'] = name
            context['linecoords'] = allcoords
            context['infcoords'] = []
        elif survey.geometry_type == "SITE":
            site = Infrastructure.objects.get(pk=survey.inf_id_fk_id)
            sitename = survey.inf_id_fk.inf_name
            coords = site.inf_geom.coords
            infcoords = [coords[0], coords[1]]
            context['points'] = geoms
            context['name'] = sitename
            context['linecoords'] = []
            context['infcoords'] = infcoords
        else:
            name = "Unknown Location"

        return render(request, 'report-view.html', context)
    else:
        return redirect('login')

def CreateReport(request):
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    if not user.is_superuser:
        return redirect('index')
    if request.method == 'POST':
        header_form = CreateReportForm(request.POST)
        if header_form.is_valid():
            new_survey = header_form.save()
            survey_id = new_survey.id
            return redirect('edit_report', survey_id=survey_id)
    else:
        header_form = CreateReportForm()
    return render(request, 'create-report.html', {'header_form': header_form})


def EditReport(request, survey_id):
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    if not user.is_superuser:
        return redirect('index')
    context = {'survey_id': survey_id}
    survey_obj = SurveyDate.objects.get(pk=survey_id)
    deficiencies = survey_obj.surveydef.all()
    context['defs'] = deficiencies
    if request.method == 'POST':
        header_form = CreateReportForm(request.POST, instance=survey_obj)
        if header_form.is_valid():
            header_form.save()
            now = datetime.datetime.now()
            messages.add_message(request, messages.INFO, 'Last saved at {}'.format(now.strftime("%H:%M:%S")))
            return redirect('edit_report', survey_id=survey_id)
    else:
        header_form = CreateReportForm(instance=survey_obj)

    context['header_form'] = header_form

    return render(request, 'edit-report.html', context)


def AddLeak(request, survey_id):
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    if not user.is_superuser:
        return redirect('index')
    context = {}

    if request.method == 'POST':
        form = LeakForm(request.POST, request.FILES, initial={'surveydate_id_fk': survey_id})
        if form.is_valid():
            form.save()
            return redirect('edit_report', survey_id=survey_id)
    else:
        form = LeakForm(initial={'surveydate_id_fk': survey_id})

    context['form'] = form

    return render(request, 'create-leak.html', context)


def DeleteLeak(request, survey_id, leak_id):
    user = request.user
    if not user.is_superuser:
        return redirect('index')

    leak = Deficiency.objects.get(pk=leak_id)
    leak.delete()

    return redirect('edit_report', survey_id=survey_id)