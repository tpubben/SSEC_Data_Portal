from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.serializers import serialize
import datetime

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
            return redirect('index')
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
        # Check to see if there are any leaks
        leaks = report.surveydef.all()
        leak = 'none'
        leak_check = 0
        # check to see if there are any leaks. If so, assume repaired. If not repaired set variable to indicate leak.
        if len(leaks) > 0:
            leak = 'repd'
            for item in leaks:
                if item.deficiency_repaired == False:
                    leak_check += 1
        if leak_check > 0:
            leak = 'leak'
        complete = report.survey_complete
        if report.geometry_type == "PIPELINE":
            site_name = report.pipe_id_fk
        elif report.geometry_type == "SITE":
            site_name = report.inf_id_fk
        else:
            site_name = 'NA'
        report_list.append(
            {"name": site_name, "date": report.survey_date, "id": report.id, "company": report.client_id_fk,
             'complete': complete, 'leak': leak})

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
        geoms = []

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
            context['inf_image'] = site.inf_tile_url
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
    request.session['survey_id'] = survey_id
    survey_obj = SurveyDate.objects.get(pk=survey_id)
    context["survey"] = survey_obj
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

def GasUpload(request):
    from django.core.files.storage import FileSystemStorage
    from django.contrib.gis.geos import MultiPoint, Point
    import os
    survey_id = request.session['survey_id']
    survey = SurveyDate.objects.get(pk=survey_id)
    if request.method == "POST" and request.FILES['gasfile']:
        gasfile = request.FILES['gasfile']
        fs = FileSystemStorage()
        filename = fs.save(gasfile.name, gasfile)
        filename = os.path.join("media/", filename)
        with open (filename, 'r') as gas:
            gas = gas.readlines()
            gasdata = []
            for line in gas:
                if not line.startswith("L"):
                    line = line.strip().split(",")
                    lat, long, gasvalue = line[0], line[1], line[2]
                    gas_point = Point(x=float(long), y=float(lat), z=float(gasvalue))
                    gasdata.append(gas_point)
                else:
                    continue

            gas_mp = MultiPoint(gasdata)
            survey.survey_gas_point_geom = gas_mp
            survey.save()

        return redirect("edit_report", survey_id=survey_id)


    return render(request, "gasupload.html")


def UploadJSON(request):
    import os
    from django.core.files.storage import FileSystemStorage
    survey_id = request.session['survey_id']
    survey = SurveyDate.objects.get(pk=survey_id)
    if request.method == "POST" and request.FILES['jsonfile']:
        JSONfile = request.FILES['jsonfile']
        fs = FileSystemStorage()
        filename = fs.save(JSONfile.name, JSONfile)
        filename = os.path.join("media/", filename)
        with open (filename, 'r') as contours:
            contours = contours.readlines()
            contour_lines = ""
            for line in contours:
                line = line.strip()
                contour_lines += line

            survey.survey_contour_geom = contour_lines
            survey.save()
            print (survey.survey_contour_geom)

        return redirect("edit_report", survey_id=survey_id)


    return render(request, "JSONupload.html")


def EditSite(request, inf_id):
    from django.core.files.storage import FileSystemStorage
    from django.contrib.gis.geos import MultiPoint, Point
    import os, zipfile
    inf = Infrastructure.objects.get(pk=inf_id)
    if request.method == "POST" and request.FILES['tilefile']:
        tilefile = request.FILES['tilefile']
        fs = FileSystemStorage()
        tilename = fs.save(tilefile.name, tilefile)
        tilename = os.path.join("media/", tilename)
        unique_id = inf.inf_name.replace(" ", "")
        inf.inf_tile_url = 'media/tiles/{}'.format(unique_id)
        inf.save()

        with zipfile.ZipFile(tilename, 'r') as file:
            file.extractall(path='media/tiles/{}'.format(unique_id))
        return redirect('index')
    return render(request, "editsite.html")


def ListInfrastructure(request):
    all_infs = Infrastructure.objects.all()
    context = {"inf_list": Infrastructure.objects.all()}
    return render(request, "inf_list.html", context)



class GasPointAPI(APIView):

    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        survey_id = request.session['survey_id']
        survey = SurveyDate.objects.get(pk=survey_id)
        survey_mp = survey.survey_gas_point_geom.coords
        filtered_points = []
        for point in survey_mp:
            if point[2] < 100:
                continue
            else:
                filtered_points.append(point)

        return JsonResponse(filtered_points, safe=False)


