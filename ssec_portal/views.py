from django.shortcuts import redirect

# Create your views here.

# redirects to pipelines app
def index_redirect(request):
    response = redirect('/pipelines/')

    return response