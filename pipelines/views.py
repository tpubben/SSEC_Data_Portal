from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic
from django.template import loader

from .forms import CustomUserCreationForm
from .models import Pipeline
# Create your views here.


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def index(request):
    try:
        client_id = request.user.client_id_fk
    except:
        client_id = 0
    pipe_list = Pipeline.objects.filter(client_id_fk=client_id)
    context = {'pipe_list': pipe_list}

    return render(request, 'index.html', context)

